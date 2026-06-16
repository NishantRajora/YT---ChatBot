````markdown
# 🎥 YouTube Transcript AI Assistant

> FastAPI + LangChain + Ollama + FAISS + RAG

An AI-powered assistant that enables users to load a YouTube video's transcript into a vector database and ask natural language questions about its content.

The application automatically fetches transcripts, generates embeddings, stores them in a FAISS vector index, retrieves relevant context, and produces grounded responses using a local Large Language Model (LLM) running through Ollama.

---

## 🚀 Features

- Extract transcripts directly from YouTube videos
- Automatic transcript chunking
- Vector embeddings using Ollama
- FAISS vector database integration
- Retrieval-Augmented Generation (RAG)
- Semantic search over video content
- FastAPI backend API
- Modern web interface
- Local LLM execution (No OpenAI API required)
- Transcript caching for faster repeated queries

---

## 🏗️ Architecture

```text
YouTube Video
      ↓
Transcript Extraction
      ↓
Text Chunking
      ↓
Ollama Embeddings
      ↓
FAISS Vector Store
      ↓
Semantic Retrieval
      ↓
Context Injection
      ↓
ChatOllama
      ↓
Answer Generation
```

---

## 📋 Workflow

### Step 1: Load Video

User provides a YouTube URL.

Example:

```text
https://www.youtube.com/watch?v=VIDEO_ID
```

The system:

- Extracts the video ID
- Downloads the transcript
- Splits transcript into chunks
- Creates embeddings
- Stores vectors in FAISS

---

### Step 2: Ask Questions

Examples:

```text
What is the main topic of this video?

Summarize the video.

What technologies were discussed?

Explain the key concepts mentioned.
```

The assistant retrieves the most relevant transcript chunks and generates answers grounded in the video's content.

---

## 🛠️ Technologies Used

### Backend

- FastAPI
- Python
- Pydantic

### AI Stack

- LangChain
- Ollama
- ChatOllama
- Ollama Embeddings
- FAISS

### Data Processing

- YouTube Transcript API
- Recursive Character Text Splitter

### Frontend

- HTML
- CSS
- JavaScript

---

## 📂 Project Structure

```text
YT-Transcript-AI-Assistant/

│
├── main.py
├── requirements.txt
│
├── frontend/
│   └── index.html
│
├── vector_store/
│
└── README.md
```

---

## 🔗 API Endpoints

### Load Transcript

```http
POST /load-video
```

Request:

```json
{
  "videolink": "https://www.youtube.com/watch?v=xxxxx"
}
```

Response:

```json
{
  "message": "Video transcript loaded into FAISS.",
  "video_id": "xxxxx",
  "chunks": 25
}
```

---

### Ask Question

```http
POST /ask-assistant
```

Request:

```json
{
  "videolink": "https://www.youtube.com/watch?v=xxxxx",
  "target_question": "What is the video about?"
}
```

Response:

```json
{
  "answer": "Generated answer from transcript context"
}
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/yt-transcript-ai-assistant.git

cd yt-transcript-ai-assistant
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Ollama

Download and install Ollama:

https://ollama.com

Pull the required model:

```bash
ollama pull qwen2.5-coder:3b
```

---

## ▶️ Run Backend

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

---

## 🌐 Run Frontend

Open:

```text
index.html
```

Or use VS Code Live Server.

---

## 💡 Use Cases

- Summarize YouTube lectures
- Learn from technical tutorials
- Extract key concepts from educational videos
- Create video knowledge bases
- Research and content analysis
- AI-powered learning assistant

---

## 🔮 Future Improvements

- Multi-video knowledge base
- Persistent vector storage
- Conversation memory
- PDF summary export
- Playlist support
- Streaming responses
- Authentication system
- Docker deployment

---

## 👨‍💻 Author

### Nishant Rajora

Data Science • AI Engineering • FastAPI • Machine Learning • RAG Systems

---

## ⭐ Support

If you found this project useful, consider starring the repository.
````
