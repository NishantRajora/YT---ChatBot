videolink=input("Enter the video Link")
#videolink="https://www.youtube.com/watch?v=qHtmXTO34_w"
target_question= input("Enter your question about the video: ")
#target_question = "what si this video all about"


video_id = videolink.split("v=")[-1].split("&")[0]  
#print(f"Extracted Video ID: {video_id}")

import langchain_ollama
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter

try:
    #Connecting to YouTube to retrieve captions
    yt_api = YouTubeTranscriptApi()
    
    # Modern object-oriented call strategy to retrieve captions array
    raw_transcript = yt_api.fetch(video_id, languages=["en"])
    
    # Extract structural text strings via object properties (.text)
    transcript = " ".join(segment.text for segment in raw_transcript)


except TranscriptsDisabled:
    print("Error: Transcripts are disabled for this specific YouTube video.")


splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.create_documents([transcript])

#
#print(transcript)

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama


# Initialize local embedding vectors using your Qwen local runner setup
embeddings = OllamaEmbeddings(model="qwen2.5-coder:3b")

# Initialize local Chat generation LLM instance using your Qwen local runner setup
llm = ChatOllama(model="qwen2.5-coder:3b", temperature=0.2)

# Compile your pieces directly into a local FAISS DB instance
#print("Generating context vectors and building local FAISS storage matrix...")
vector_store = FAISS.from_documents(chunks, embeddings)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
#print("Local database indexing sequence finished successfully!")

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser


def format_docs(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs)


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

parallel_context_chain = RunnableParallel({
    "context": retriever | RunnableLambda(format_docs),
    "question": RunnablePassthrough()
})

rag_pipeline = (
    RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })
    | prompt 
    | llm 
    | StrOutputParser()
)





system_response = rag_pipeline.invoke(target_question)

print("Local Qwen Assistant Response:")
print("-" * 50)
print(system_response)
print("-" * 50)