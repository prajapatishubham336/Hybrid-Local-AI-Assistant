# Hybrid-Local-AI-Assistant
Hybrid Local AI Assistant is a privacy-focused AI chatbot that supports general conversations and document-based Q&amp;A. It uses Ollama, Llama 3.2, Nomic Embeddings, ChromaDB, and RAG to process documents locally. Users can upload PDF, DOCX, and TXT files and ask questions without using paid cloud APIs.


# 🤖 Hybrid Local AI Assistant

A privacy-first **Local AI Assistant** built with **Python, Streamlit, Ollama, Llama 3.2, Nomic Embeddings and ChromaDB**.

The application supports both:

* 💬 General AI conversations
* 📚 Question answering from uploaded PDF/DOCX/TXT documents
* 🔎 Semantic document search using vector embeddings
* 🔐 Local/private AI processing without OpenAI or Gemini APIs

---

## 🚀 Project Overview

The **Hybrid Local AI Assistant** combines a general-purpose local Large Language Model with a private document-based RAG (Retrieval-Augmented Generation) system.

Users can simply ask general questions, or upload their own documents and ask questions related to those documents.

The uploaded documents are converted into text chunks, embedded using a local embedding model, and stored in **ChromaDB**.

When the user asks a question, the application searches the vector database for relevant information and provides the retrieved context to the local LLM.

---

## ✨ Features

### 1. 💬 General AI Chat

Users can ask normal/general questions without uploading any document.

The application uses:

**Llama 3.2**

through **Ollama** to generate the response.

---

### 2. 📚 Document-Based Question Answering

Users can upload:

* PDF
* DOCX
* TXT

documents.

The application extracts the document content and converts it into smaller chunks.

These chunks are then stored in ChromaDB using vector embeddings.

---

### 3. 🔎 Semantic Search

The application uses:

**Nomic Embed Text**

to generate embeddings for document chunks.

When a user asks a question, the application performs similarity search in ChromaDB and retrieves the top 3 relevant chunks.

```text
User Question
      ↓
Embedding
      ↓
ChromaDB Similarity Search
      ↓
Top 3 Relevant Chunks
      ↓
Llama 3.2
      ↓
Final Answer
```

---

### 4. 🔀 Hybrid AI Mode

The application supports two modes automatically.

#### Document Context Available

If relevant document results are available:

```text
Question
   ↓
ChromaDB
   ↓
Relevant Documents
   ↓
Context + Question
   ↓
Llama 3.2
   ↓
Answer
```

#### No Document Context

If there are no documents in the knowledge base, the application directly asks Llama 3.2.

```text
Question
   ↓
Llama 3.2
   ↓
General Knowledge Answer
```

---

### 5. 🔐 Privacy First

This project is designed for local/private AI usage.

No OpenAI API key or Gemini API key is required.

The LLM and embedding model run through **Ollama** on the local machine.

Uploaded documents are stored locally.

This makes the project useful for private documents and offline/local AI experiments.

---

### 6. 🗑️ Clear Knowledge Base

The sidebar contains:

**Clear Knowledge Base**

This removes:

* Stored vector data
* Uploaded files
* Chat history

from the application.

---

## 🛠️ Tech Stack

| Technology       | Purpose              |
| ---------------- | -------------------- |
| Python           | Programming language |
| Streamlit        | Web application UI   |
| Ollama           | Local LLM execution  |
| Llama 3.2        | Local language model |
| Nomic Embed Text | Text embeddings      |
| ChromaDB         | Vector database      |
| LangChain        | LLM/RAG framework    |
| PyPDF            | PDF processing       |
| Docx2txt         | DOCX processing      |

---

## 📂 Project Structure

```text
Hybrid-Local-AI-Assistant/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   └── .gitkeep
│
└── vectorstore/
    └── chroma_db/
        └── .gitkeep
```

---

## 📄 File Description

### `app.py`

Main Streamlit application.

It contains:

* Document loading
* Text splitting
* Embedding generation
* ChromaDB configuration
* RAG retrieval
* Llama 3.2 integration
* Chat interface
* File upload
* Knowledge base clearing

---

### `requirements.txt`

Contains all required Python libraries.

Example:

```text
streamlit
langchain
langchain-community
langchain-core
langchain-text-splitters
langchain-ollama
langchain-chroma
chromadb
pypdf
docx2txt
```

---

### `data/`

Uploaded documents are stored here.

Supported file types:

```text
.pdf
.docx
.txt
```

Example:

```text
data/
├── medical_book.pdf
├── notes.docx
└── information.txt
```

---

### `vectorstore/chroma_db/`

This directory contains the locally persisted ChromaDB vector database.

It stores embeddings and metadata generated from uploaded documents.

---

## ⚙️ Installation

### Step 1: Clone the Project

```bash
git clone https://github.com/prajapatishubham336/Hybrid Local AI Assistant.git
```

Or simply open the project folder locally.

---

### Step 2: Create Virtual Environment

Using Conda:

```bash
conda create -n hybrid-ai python=3.11
```

Activate it:

```bash
conda activate hybrid-ai
```

Or using Python virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

---

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

# 🦙 Install Ollama

Download and install Ollama on your computer.

After installation, verify it:

```bash
ollama --version
```

---

## 📥 Download Llama 3.2

Run:

```bash
ollama pull llama3.2
```

Check the installed models:

```bash
ollama list
```

You should see:

```text
llama3.2
```

---

## 📥 Download Nomic Embedding Model

Run:

```bash
ollama pull nomic-embed-text
```

Verify:

```bash
ollama list
```

You should see:

```text
llama3.2
nomic-embed-text
```

---

# ▶️ Run the Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

Usually:

```text
http://localhost:8501
```

---

# 🧪 How to Use

## Step 1: Start the Application

```bash
streamlit run app.py
```

---

## Step 2: Upload a Document

Use:

**Upload documents (Optional - PDF, DOCX, TXT)**

Select one or multiple files.

For example:

```text
medical.pdf
research.pdf
notes.docx
```

---

## Step 3: Index Documents

Click:

**Index Uploaded Documents**

The application will:

```text
Document
   ↓
Text Extraction
   ↓
Text Splitting
   ↓
Embedding Generation
   ↓
ChromaDB
```

---

## Step 4: Ask Questions

Example:

```text
What is machine learning?
```

or, if a medical PDF is uploaded:

```text
What is diabetes?
```

The application searches the uploaded documents and provides an answer.

---

# 🧠 RAG Architecture

The project follows this architecture:

```text
                 USER
                  │
                  ▼
           Streamlit UI
                  │
                  ▼
             User Query
                  │
                  ▼
          Ollama Embeddings
                  │
                  ▼
             ChromaDB
                  │
          Similarity Search
                  │
            Top 3 Chunks
                  │
                  ▼
           Context + Query
                  │
                  ▼
             Llama 3.2
                  │
                  ▼
             AI Response
```

---

# 📚 Document Processing Pipeline

Uploaded documents follow this pipeline:

```text
PDF / DOCX / TXT
       │
       ▼
Document Loader
       │
       ▼
Text Extraction
       │
       ▼
Recursive Character Text Splitter
       │
       ▼
Text Chunks
       │
       ▼
Nomic Embeddings
       │
       ▼
ChromaDB
```

The current configuration uses:

```python
chunk_size = 800
chunk_overlap = 120
```

---

# 🔍 Retrieval Configuration

The application retrieves the top 3 relevant chunks:

```python
results = db.similarity_search(question, k=3)
```

These chunks are passed to Llama 3.2 as context.

---

# 🤖 Models

## LLM

```text
llama3.2
```

Used for:

* General chat
* Question answering
* RAG responses

---

## Embedding Model

```text
nomic-embed-text
```

Used for:

* Creating document embeddings
* Creating query embeddings
* Semantic similarity search

---

# 🔒 Privacy

One of the major goals of this project is local/private AI.

The application does not require:

```text
OpenAI API
Google Gemini API
OpenAI API Key
Gemini API Key
```

The main AI processing is performed locally through Ollama.

Therefore, sensitive documents can remain on the local machine.

> Note: "Local" privacy depends on your own machine, Ollama configuration, operating system, and network environment.

---

# 🧹 Clearing the Knowledge Base

To remove stored documents and reset the application:

1. Open the sidebar.
2. Click:

```text
🗑️ Clear Knowledge Base
```

The application clears the stored knowledge base and uploaded files.

---

# ⚠️ Common Errors

## Ollama is not running

If you receive an Ollama connection error, make sure Ollama is installed and running.

You can test:

```bash
ollama list
```

---

## Model not found

If Llama 3.2 is unavailable:

```bash
ollama pull llama3.2
```

For embeddings:

```bash
ollama pull nomic-embed-text
```

---

## Streamlit command not found

Install Streamlit:

```bash
pip install streamlit
```

Then:

```bash
streamlit run app.py
```

---

## ChromaDB error

Make sure the required packages are installed:

```bash
pip install chromadb langchain-chroma
```

---

# 🔮 Future Improvements

Possible future improvements include:

* 🔐 User authentication
* 📑 Support for more document formats
* 🧠 Conversation memory
* 📊 RAG evaluation
* 🔎 Better relevance scoring
* 📌 Citation with document page numbers
* 🗂️ Multiple knowledge bases
* 🌐 LAN deployment
* 🎤 Voice input
* 🔊 Text-to-speech
* 🖥️ Fully offline deployment
* ⚡ Streaming LLM responses
* 📈 RAG performance monitoring

---

# 🎯 Use Cases

This project can be used for:

* 📚 Personal knowledge assistant
* 🏢 Private company documents
* 🎓 Study assistant
* 📖 Research papers
* 🏥 Medical document Q&A
* 📋 Business documents
* 📑 Legal document search
* 🧑‍💻 Technical documentation
* 🔒 Sensitive/private information

---

# 👨‍💻 Author

**Shubham Prajapati**

AI / Data Science / Generative AI Project

---

# ⭐ Project Summary

**Hybrid Local AI Assistant** is a privacy-focused AI application that combines a local LLM with RAG-based document retrieval.

It allows users to:

```text
Chat with AI
     +
Search Private Documents
     +
Generate Answers
     +
Run Locally
```

The project demonstrates practical implementation of:

**LLM + Embeddings + Vector Database + RAG + Streamlit + Local AI**
