from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

# ---- LANGCHAIN & YOUTUBE IMPORTS ----
import langchain_ollama
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# 1. Initialize FastAPI
app = FastAPI()
app.state.video_store_cache = {}
app.state.chat_sessions = {}

# Enable CORS so your local HTML file can talk to the server safely
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r".*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Define the expected request payload structure
class VideoPayload(BaseModel):
    videolink: str
    session_id: Optional[str] = None


class QuestionPayload(BaseModel):
    videolink: str
    target_question: str
    session_id: Optional[str] = None


class ChatMessagePayload(BaseModel):
    videolink: str
    message: str
    session_id: Optional[str] = None

# Helper function to format documents
def format_docs(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs)


def ensure_session_id(session_id: Optional[str]) -> str:
    return session_id or str(uuid4())


def get_session_key(video_id: str, session_id: str) -> str:
    return f"{video_id}:{session_id}"


def ensure_chat_session(video_id: str, session_id: str) -> dict:
    session_key = get_session_key(video_id, session_id)
    if session_key not in app.state.chat_sessions:
        app.state.chat_sessions[session_key] = {
            "video_id": video_id,
            "session_id": session_id,
            "messages": [],
        }
    return app.state.chat_sessions[session_key]


def append_chat_message(video_id: str, session_id: str, role: str, content: str) -> None:
    session = ensure_chat_session(video_id, session_id)
    session["messages"].append({"role": role, "content": content})
    session["messages"] = session["messages"][-12:]


def format_history(messages: List[dict]) -> str:
    if not messages:
        return "No previous conversation."

    return "\n".join(f"{message['role'].upper()}: {message['content']}" for message in messages)


def extract_video_id(videolink: str) -> str:
    try:
        return videolink.split("v=")[-1].split("&")[0]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid YouTube link format.")


def build_vector_store_from_video(video_id: str):
    try:
        yt_api = YouTubeTranscriptApi()
        raw_transcript = yt_api.fetch(video_id, languages=["en"])
        transcript = " ".join(segment.text for segment in raw_transcript)
    except TranscriptsDisabled:
        raise HTTPException(status_code=400, detail="Transcripts are disabled for this specific YouTube video.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch transcript: {str(e)}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])

    embeddings = OllamaEmbeddings(model="qwen2.5-coder:3b")
    vector_store = FAISS.from_documents(chunks, embeddings)

    return vector_store, len(chunks)


def rewrite_question_with_history(target_question: str, conversation_history: str) -> str:
    llm = ChatOllama(model="qwen2.5-coder:3b", temperature=0.0)

    rewrite_prompt = PromptTemplate(
        template="""
Rewrite the follow-up question so it is fully standalone for transcript retrieval.
Use the conversation history only to resolve references like it, this, that, they, he, she, and the previous point.
Return only the rewritten question.

Conversation history:
{history}

Follow-up question:
{question}
""",
        input_variables=["history", "question"],
    )

    rewrite_chain = rewrite_prompt | llm | StrOutputParser()
    rewritten_question = rewrite_chain.invoke({"history": conversation_history, "question": target_question})
    return rewritten_question.strip() or target_question


def answer_from_vector_store(vector_store, target_question: str, conversation_history: str) -> str:
    llm = ChatOllama(model="qwen2.5-coder:3b", temperature=0.2)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    rewritten_question = rewrite_question_with_history(target_question, conversation_history)

    prompt = PromptTemplate(
        template="""
You are a ChatGPT-style assistant discussing one YouTube video.
Use the transcript context and recent conversation history.
Answer only from the transcript and conversation context.
If the transcript does not support the answer, say you do not know.
Do not invent facts or use outside knowledge.

Recent conversation history:
{history}

Transcript context:
{context}

Question:
{question}
        """,
        input_variables=['context', 'question', 'history']
    )

    context_docs = retriever.invoke(rewritten_question)
    context_text = format_docs(context_docs)

    answer_chain = prompt | llm | StrOutputParser()
    return answer_chain.invoke({
        "context": context_text,
        "question": rewritten_question,
        "history": conversation_history,
    })

# 3. Create the FastAPI POST endpoints
@app.post("/load-video")
async def load_video(data: VideoPayload):
    video_id = extract_video_id(data.videolink)
    session_id = ensure_session_id(data.session_id)
    session = ensure_chat_session(video_id, session_id)

    if video_id in app.state.video_store_cache:
        return {
            "message": "Video already loaded into FAISS.",
            "video_id": video_id,
            "cached": True,
            "session_id": session_id,
            "messages": session["messages"],
        }

    vector_store, chunk_count = build_vector_store_from_video(video_id)
    app.state.video_store_cache[video_id] = vector_store

    return {
        "message": "Video transcript loaded into FAISS.",
        "video_id": video_id,
        "cached": False,
        "chunks": chunk_count,
        "session_id": session_id,
        "messages": session["messages"],
    }


@app.post("/ask-assistant")
async def ask_assistant(data: QuestionPayload):
    video_id = extract_video_id(data.videolink)
    session_id = ensure_session_id(data.session_id)

    vector_store = app.state.video_store_cache.get(video_id)
    if vector_store is None:
        raise HTTPException(status_code=400, detail="Load this video first so the transcript is available in FAISS.")

    session = ensure_chat_session(video_id, session_id)
    conversation_history = format_history(session["messages"])
    append_chat_message(video_id, session_id, "user", data.target_question)

    system_response = answer_from_vector_store(vector_store, data.target_question, conversation_history)
    append_chat_message(video_id, session_id, "assistant", system_response)

    return {
        "answer": system_response,
        "video_id": video_id,
        "session_id": session_id,
        "messages": session["messages"],
    }


@app.post("/chat")
async def chat_with_assistant(data: ChatMessagePayload):
    video_id = extract_video_id(data.videolink)
    session_id = ensure_session_id(data.session_id)

    vector_store = app.state.video_store_cache.get(video_id)
    if vector_store is None:
        raise HTTPException(status_code=400, detail="Load this video first so the transcript is available in FAISS.")

    session = ensure_chat_session(video_id, session_id)
    conversation_history = format_history(session["messages"])
    append_chat_message(video_id, session_id, "user", data.message)

    system_response = answer_from_vector_store(vector_store, data.message, conversation_history)
    append_chat_message(video_id, session_id, "assistant", system_response)

    return {
        "answer": system_response,
        "video_id": video_id,
        "session_id": session_id,
        "messages": session["messages"],
    }


@app.post("/clear-chat")
async def clear_chat(data: ChatMessagePayload):
    video_id = extract_video_id(data.videolink)
    session_id = ensure_session_id(data.session_id)
    session_key = get_session_key(video_id, session_id)
    app.state.chat_sessions.pop(session_key, None)

    return {"message": "Chat history cleared.", "video_id": video_id, "session_id": session_id}