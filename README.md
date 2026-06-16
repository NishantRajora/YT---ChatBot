# 🎥 YouTube Transcript AI Assistant

<div align="center">

### Ask Questions About Any YouTube Video Using AI

**FastAPI • LangChain • Ollama • FAISS • RAG**

Turn any YouTube video into an intelligent knowledge base and chat with its content.

</div>

---

## 🚀 Overview

YouTube videos contain valuable information, but finding specific insights often requires watching hours of content.

This project solves that problem by combining:

* YouTube Transcript Extraction
* Retrieval-Augmented Generation (RAG)
* FAISS Vector Search
* Ollama Local LLMs
* FastAPI Backend

Users can load a YouTube video's transcript into a vector database and ask natural language questions about the video's content.

The system retrieves relevant transcript segments and generates context-aware answers using a local LLM.

---

## ✨ Features

### 📺 YouTube Transcript Processing

* Automatic transcript extraction
* Support for English transcripts
* Transcript chunking for efficient retrieval

### 🧠 AI-Powered Question Answering

* Retrieval-Augmented Generation (RAG)
* Context-aware responses
* Grounded answers from transcript content
* Hallucination reduction through retrieval

### ⚡ Fast Semantic Search

* FAISS Vector Database
* Embedding-based similarity search
* Relevant transcript retrieval

### 🤖 Local AI Inference

* Powered by Ollama
* No OpenAI API required
* Fully local execution

### 🌐 Modern Web Interface

* Clean responsive UI
* Real-time interaction
* FastAPI REST endpoints

---

## 🏗️ System Architecture

```text
YouTube Video
      │
      ▼
Transcript Extraction
      │
      ▼
Text Chunking
      │
      ▼
Ollama Embeddings
      │
      ▼
FAISS Vector Store
      │
      ▼
Similarity Search
      │
      ▼
Relevant Context
      │
      ▼
ChatOllama (LLM)
      │
      ▼
Generated Answer
```

---

## ⚙️ Tech Stack

### Backend

* FastAPI
* Python
* Pydantic

### AI & RAG

* LangChain
* Ollama
* ChatOllama
* Ollama Embeddings
* FAISS

### Data Processing

* YouTube Transcript API
* Recursive Character Text Splitter

### Frontend

* HTML
* CSS
* JavaScript

---

## 📂 Project Structure

```text
YT-Transcript-AI-Assistant/

├── main.py
├── requirements.txt
├── index.html
├── README.md
└── assets/
```

---

## 🔌 API Endpoints

### Load Video Transcript

```http
POST /load-video
```

#### Request

```json
{
  "videolink": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

#### Response

```json
{
  "message": "Video transcript loaded into FAISS.",
  "video_id": "VIDEO_ID",
  "cached": false,
  "chunks": 32
}
```

---

### Ask Assistant

```http
POST /ask-assistant
```

#### Request

```json
{
  "videolink": "https://www.youtube.com/watch?v=VIDEO_ID",
  "target_question": "What is the video about?"
}
```

#### Response

```json
{
  "answer": "Generated answer from transcript context"
}
```

---

## 🛠 Installation

### Clone Repository

```bash
git clone https://github.com/your-username/yt-transcript-ai-assistant.git

cd yt-transcript-ai-assistant
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🤖 Install Ollama

Download:

```text
https://ollama.com
```

Pull the model:

```bash
ollama pull qwen2.5-coder:3b
```

Verify:

```bash
ollama list
```

---

## ▶️ Run the Backend

```bash
uvicorn main:app --reload
```

Server starts at:

```text
http://127.0.0.1:8000
```

---

## 🌐 Run the Frontend

Open:

```text
index.html
```

Or use:

* VS Code Live Server
* Python HTTP Server

```bash
python -m http.server 5500
```

---

## 💡 Example Questions

```text
Summarize this video.

What are the key points discussed?

Explain the main concept.

What technologies were mentioned?

Give me a short overview.

What are the speaker's conclusions?
```

---

## 🎯 Use Cases

* Educational video summarization
* Technical tutorial analysis
* Lecture understanding
* Research assistance
* Knowledge extraction
* Content review
* Personal learning assistant

---

## 🔮 Future Improvements

* Multi-video knowledge base
* Playlist ingestion
* Persistent vector storage
* Chat memory
* Streaming responses
* PDF summary export
* User authentication
* Docker deployment
* Multi-language support

---

## 👨‍💻 Author

### Nishant Rajora

---

## ⭐ Support

If you found this project useful:

* Star the repository
* Fork the project
* Share feedback
* Contribute improvements

---

<div align="center">

Built with ❤️ using FastAPI, LangChain, Ollama and FAISS

</div>
