from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

# Enable CORS so your local HTML file can talk to the server safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Define the expected request payload structure
class VideoPayload(BaseModel):
    videolink: str


class QuestionPayload(BaseModel):
    videolink: str
    target_question: str

# Helper function to format documents
def format_docs(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs)


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


def answer_from_vector_store(vector_store, target_question: str) -> str:
    llm = ChatOllama(model="qwen2.5-coder:3b", temperature=0.2)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    prompt = PromptTemplate(
        template="""
          You are a helpful assistant.
          Answer ONLY from the provided transcript context.
          If the context is insufficient, just say you don't know.

          {context}
          Question: {question}
        """,
        input_variables=['context', 'question']
    )

    rag_pipeline = (
        RunnableParallel({
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        })
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_pipeline.invoke(target_question)

# 3. Create the FastAPI POST endpoints
@app.post("/load-video")
async def load_video(data: VideoPayload):
    video_id = extract_video_id(data.videolink)

    if video_id in app.state.video_store_cache:
        return {"message": "Video already loaded into FAISS.", "video_id": video_id, "cached": True}

    vector_store, chunk_count = build_vector_store_from_video(video_id)
    app.state.video_store_cache[video_id] = vector_store

    return {
        "message": "Video transcript loaded into FAISS.",
        "video_id": video_id,
        "cached": False,
        "chunks": chunk_count,
    }


@app.post("/ask-assistant")
async def ask_assistant(data: QuestionPayload):
    video_id = extract_video_id(data.videolink)

    vector_store = app.state.video_store_cache.get(video_id)
    if vector_store is None:
        raise HTTPException(status_code=400, detail="Load this video first so the transcript is available in FAISS.")

    system_response = answer_from_vector_store(vector_store, data.target_question)
    return {"answer": system_response, "video_id": video_id}