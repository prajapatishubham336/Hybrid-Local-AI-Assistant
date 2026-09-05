import os
import streamlit as st
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "vectorstore" / "chroma_db"

DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_DIR.parent.mkdir(parents=True, exist_ok=True)

OLLAMA_MODEL = "llama3.2"
EMBED_MODEL = "nomic-embed-text"

st.set_page_config(page_title="Hybrid Local AI Assistant", layout="wide")

st.title("🤖 Hybrid Local AI Assistant (General Chat + PDF RAG)")

def load_file(path):
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return PyPDFLoader(str(path)).load()
    if suffix == ".txt":
        return TextLoader(str(path), encoding="utf-8").load()
    if suffix == ".docx":
        return Docx2txtLoader(str(path)).load()
    return []

def get_embeddings():
    return OllamaEmbeddings(model=EMBED_MODEL)

def get_db():
    return Chroma(
        collection_name="private_knowledge_base",
        persist_directory=str(DB_DIR),
        embedding_function=get_embeddings()
    )

def add_documents(uploaded_files):
    all_docs = []
    for uploaded in uploaded_files:
        target = DATA_DIR / uploaded.name
        target.write_bytes(uploaded.getbuffer())
        docs = load_file(target)
        for d in docs:
            d.metadata["source_file"] = uploaded.name
        all_docs.extend(docs)

    if not all_docs:
        return 0

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_documents(all_docs)
    db = get_db()
    db.add_documents(chunks)
    return len(chunks)

def ask_question(question):
    db = get_db()
    
    # 1. Similarity Search in Vector DB
    results = db.similarity_search(question, k=3)
    
    # 2. Check if relevant context is found in uploaded PDFs
    context_found = False
    context = ""
    
    if results:
        # Simple relevance check based on content existence
        context = "\n\n---\n\n".join(
            f"Source: {d.metadata.get('source_file', 'Unknown')}\n{d.page_content}"
            for d in results
        )
        context_found = True

    llm = ChatOllama(model=OLLAMA_MODEL, temperature=0.7)

    # Hybrid Logic Prompt
    if context_found:
        prompt = ChatPromptTemplate.from_template("""
        You are an intelligent assistant.
        First, try to answer the user's question using the provided PDF CONTEXT below.
        If the answer is NOT present in the PDF context, answer the question using your general knowledge, but clearly state at the beginning: "[General Knowledge Answer]"

        CONTEXT FROM UPLOADED DOCUMENTS:
        {context}

        QUESTION:
        {question}
        """)
        chain = prompt | llm
        response = chain.invoke({"context": context, "question": question})
        return response.content, results
    else:
        # If no documents exist in Vector DB, answer directly via General LLM
        prompt = ChatPromptTemplate.from_template("""
        You are a helpful AI assistant. Answer the user's question clearly and accurately.

        QUESTION:
        {question}
        """)
        chain = prompt | llm
        response = chain.invoke({"question": question})
        return response.content, []

# Sidebar Controls
with st.sidebar:
    st.header("Settings")
    st.write(f"**Model:** `{OLLAMA_MODEL}`")
    st.write(f"**Mode:** `Hybrid (General AI + PDF Search)`")

    if st.button("🗑️ Clear Knowledge Base", use_container_width=True):
        try:
            db = get_db()
            db.reset_collection()
            if DATA_DIR.exists():
                for p in DATA_DIR.iterdir():
                    if p.is_file():
                        p.unlink()
            st.session_state.messages = []
            st.success("Knowledge base cleared.")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("sources"):
            with st.expander("📚 PDF Sources"):
                for source in msg["sources"]:
                    st.write(source)

st.divider()

# Upload File Input above Chat
uploaded_files = st.file_uploader(
    "Upload documents (Optional - PDF, DOCX, TXT):",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    if st.button("Index Uploaded Documents"):
        with st.spinner("Processing documents..."):
            try:
                count = add_documents(uploaded_files)
                st.success(f"Indexed {count} text chunks from PDF.")
            except Exception as e:
                st.error(f"Error: {e}")

question = st.chat_input("Ask anything (General question or about uploaded PDF)...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer, docs = ask_question(question)
                sources = []
                seen = set()
                
                for d in docs:
                    name = d.metadata.get("source_file", "Unknown")
                    page = d.metadata.get("page")
                    label = f"{name}" + (f" — page {page + 1}" if isinstance(page, int) else "")
                    if label not in seen:
                        sources.append(label)
                        seen.add(label)

                st.write(answer)
                if sources:
                    with st.expander("📚 PDF Sources"):
                        for source in sources:
                            st.write(source)
                            
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
            except Exception as e:
                st.error(f"Error answering question: {e}")