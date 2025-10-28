import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Correctly import from langchain_community
from langchain_community.document_loaders import (
    PyPDFLoader,
    # UnstructuredWordDocumentLoader,  # Temporarily commented out
    # YoutubeLoader,  # Temporarily commented out
)
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables from .env file
load_dotenv()

# --- 1. Initialize FastAPI App ---
app = FastAPI()

# --- 2. CORS Configuration ---
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:3000",  # In case of different dev server
    "http://127.0.0.1:3000",
    "*"  # Allow all origins for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. Define Constants & Load Models ---
DATA_PATH = "data"
DB_PATH = "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Ensure data directory exists
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

# Load the embedding model once when the server starts
try:
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
except Exception as e:
    print(f"Error loading embedding model: {e}")
    embeddings = None

# Initialize the Gemini LLM
try:
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
except Exception as e:
    print(f"Error initializing Gemini LLM: {e}")
    llm = None
    
# --- Helper functions (previously in ingest.py) ---
def load_documents_from_path(data_path):
    documents = []
    print(f"Loading documents from: {data_path}")
    for filename in os.listdir(data_path):
        file_path = os.path.join(data_path, filename)
        if os.path.isfile(file_path):
            try:
                if file_path.endswith(".pdf"):
                    loader = PyPDFLoader(file_path)
                    documents.extend(loader.load())
                # elif file_path.endswith(".docx") or file_path.endswith(".doc"):
                #     loader = UnstructuredWordDocumentLoader(file_path)
                #     documents.extend(loader.load())
                else:
                    print(f"Skipping unsupported file type: {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return documents

def load_youtube_videos_from_urls(urls):
    documents = []
    # Temporarily disabled YouTube functionality
    # for url in urls:
    #     try:
    #         loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
    #         documents.extend(loader.load())
    #     except Exception as e:
    #         print(f"Error loading YouTube URL {url}: {e}")
    print("YouTube functionality temporarily disabled")
    return documents

def process_and_store_documents(documents):
    if not documents:
        print("No documents to process.")
        return
    print(f"Processing {len(documents)} document(s)...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    
    if not chunks:
        print("Could not create chunks from documents.")
        return

    print(f"Creating vector store with {len(chunks)} chunks...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    print("Data successfully ingested and stored.")

# --- 4. Pydantic Models for Request Bodies ---
class ChatRequest(BaseModel):
    question: str

class LoginRequest(BaseModel):
    email: str
    password: str

# --- 5. API Endpoints ---

@app.get("/")
def health_check():
    """
    A simple health check endpoint to confirm the server is running.
    """
    return {"status": "ok", "message": "Backend is running!"}

@app.get("/test")
def test_endpoint():
    """
    Test endpoint to check CORS and connectivity
    """
    embeddings_status = "OK" if embeddings else "FAILED"
    llm_status = "OK" if llm else "FAILED"
    return {
        "status": "success", 
        "message": "Connection test successful!", 
        "data_path": DATA_PATH, 
        "db_path": DB_PATH,
        "embeddings_status": embeddings_status,
        "llm_status": llm_status
    }

@app.post("/login")
def login(request: LoginRequest):
    if request.email == "admin@example.com" and request.password == "password":
        return {"token": "mock-jwt-token"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/v1/data/upload")
async def upload_data(files: List[UploadFile] = File(default=[]), youtube_url: Optional[str] = Form(None)):
    print(f"Upload request received: {len(files)} files, youtube_url: {youtube_url}")
    saved_files_paths = []
    
    # First, save all files
    try:
        if files:
            for file in files:
                if not file.filename:
                    continue
                print(f"Processing file: {file.filename}")
                file_path = os.path.join(DATA_PATH, file.filename)
                with open(file_path, "wb") as f:
                    content = await file.read()
                    f.write(content)
                    print(f"Saved file: {file.filename} ({len(content)} bytes)")
                saved_files_paths.append(file_path)
        
        if not saved_files_paths and not youtube_url:
            raise HTTPException(status_code=400, detail="No valid files to process.")
        
        # Return success immediately to avoid frontend timeout
        # Process documents in background or let it run
        print("Files saved successfully, starting background processing...")
        
        # Do the heavy processing
        all_documents = []
        if saved_files_paths:
            print(f"Loading {len(saved_files_paths)} files from {DATA_PATH}...")
            all_documents.extend(load_documents_from_path(DATA_PATH))
        if youtube_url:
            print(f"YouTube URL provided but functionality is temporarily disabled: {youtube_url}")
            
        if all_documents:
            process_and_store_documents(all_documents)
            print("Successfully processed and stored documents")
        
        return {"status": "success", "message": f"Successfully uploaded {len(saved_files_paths)} file(s) and processed {len(all_documents)} document(s)"}

    except Exception as e:
        print(f"An error occurred during upload: {e}")
        import traceback
        traceback.print_exc()
        
        # Clean up any partially saved files on error
        for path in saved_files_paths:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass
        
        raise HTTPException(status_code=500, detail=f"Failed to process and ingest data: {str(e)}")

@app.get("/api/v1/data/sources")
def get_data_sources():
    """
    Get list of all uploaded documents and their status
    """
    print(f"Fetching sources from: {DATA_PATH}")
    sources = []
    if os.path.exists(DATA_PATH):
        print(f"Data path exists, listing files...")
        files_in_dir = os.listdir(DATA_PATH)
        print(f"Files found: {files_in_dir}")
        
        for filename in files_in_dir:
            file_path = os.path.join(DATA_PATH, filename)
            if os.path.isfile(file_path):
                print(f"Processing file: {filename}")
                file_stats = os.stat(file_path)
                file_size = f"{file_stats.st_size / 1024:.1f} KB"
                file_type = "pdf" if filename.endswith(".pdf") else "docx" if filename.endswith((".docx", ".doc")) else "unknown"
                
                # Format date properly
                from datetime import datetime
                date_added = datetime.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                
                source_item = {
                    "id": filename,
                    "name": filename,
                    "type": file_type,
                    "status": "indexed",
                    "dateAdded": date_added,
                    "size": file_size
                }
                sources.append(source_item)
                print(f"Added source: {source_item}")
    else:
        print(f"Data path does not exist: {DATA_PATH}")
    
    print(f"Returning {len(sources)} sources")
    return {"sources": sources}

@app.delete("/api/v1/data/sources/{source_id}")
def delete_data_source(source_id: str):
    """
    Delete a specific document from the knowledge base
    """
    try:
        file_path = os.path.join(DATA_PATH, source_id)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {source_id}")
            return {"status": "success", "message": f"Successfully deleted {source_id}"}
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        print(f"Error deleting file {source_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

@app.post("/api/v1/chat")
def chat(request: ChatRequest):
    if not embeddings or not llm:
        raise HTTPException(status_code=500, detail="Backend models not initialized.")

    vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={'k': 3})
    
    template = """
    You are a helpful assistant. Use the following pieces of context from the uploaded documents to answer the user's question.
    If you don't know the answer from the context provided, just say that you don't know. Do not try to make up an answer.
    Keep the answer concise and directly related to the context.

    Context: {context}

    Question: {question}

    Helpful Answer:
    """
    prompt = PromptTemplate.from_template(template)
    
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    try:
        response = rag_chain.invoke(request.question)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during RAG chain invocation: {e}")

# --- 6. Run the Server ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)