import os
import uvicorn
import hashlib
import uuid
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import PyPDF2
import google.generativeai as genai
from dotenv import load_dotenv
import io

# Try to import Supabase (optional dependency)
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

# Load environment variables
load_dotenv()

# Configure Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    print("✓ Google Gemini API configured")
else:
    print("✗ Warning: GOOGLE_API_KEY not found in environment variables")

# Configure Supabase (optional)
supabase = None
if SUPABASE_AVAILABLE:
    SUPABASE_URL = "https://kfekhrbilvrobunqwgzd.supabase.co"
    SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
    
    if SUPABASE_KEY:
        try:
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            print("✓ Supabase client configured")
        except Exception as e:
            print(f"✗ Warning: Supabase configuration failed: {e}")
            supabase = None
    else:
        print("✗ Warning: SUPABASE_ANON_KEY not found - using in-memory storage only")
else:
    print("✗ Warning: Supabase not installed - using in-memory storage only")

# Initialize FastAPI
app = FastAPI(title="AI Chatbot API - Hybrid Mode", version="2.1.0")

# CORS Configuration
FRONTEND_URLS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080", 
    "https://ai-chatbot-app-j7o8.onrender.com",
    "https://*.onrender.com",
    "*"  # Allow all origins for demo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_URLS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (primary) + Supabase backup (if available)
documents_store = {}
documents_metadata = []

class ChatRequest(BaseModel):
    question: str

class LoginRequest(BaseModel):
    email: str
    password: str

def extract_text_from_pdf_bytes(file_content: bytes):
    """Extract text from PDF bytes (in-memory processing)"""
    try:
        text = ""
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

def get_text_hash(text: str) -> str:
    """Generate a hash for text content"""
    return hashlib.sha256(text.encode()).hexdigest()

async def store_in_supabase(filename: str, file_content: bytes, text_content: str):
    """Store document in Supabase (optional backup)"""
    if not supabase:
        return None
    
    try:
        # Store file in Supabase storage
        file_path = f"uploads/{uuid.uuid4()}_{filename}"
        storage_result = supabase.storage.from_("documents").upload(file_path, file_content)
        
        # Create document record
        document_data = {
            "filename": filename,
            "original_filename": filename,
            "file_type": "pdf",
            "file_size": len(file_content),
            "content_preview": text_content[:500] + "..." if len(text_content) > 500 else text_content,
            "status": "processing",
            "storage_path": file_path,
        }
        
        doc_result = supabase.table("documents").insert(document_data).execute()
        document_id = doc_result.data[0]["id"]
        
        # Split content into chunks and store
        chunks = chunk_text(text_content)
        chunk_data = []
        
        for i, chunk in enumerate(chunks):
            chunk_data.append({
                "document_id": document_id,
                "chunk_index": i,
                "content": chunk,
                "content_length": len(chunk),
                "chunk_hash": get_text_hash(chunk)
            })
        
        # Batch insert chunks
        if chunk_data:
            supabase.table("document_chunks").insert(chunk_data).execute()
        
        # Update document status
        supabase.table("documents").update({
            "status": "indexed",
            "processed_date": datetime.now().isoformat()
        }).eq("id", document_id).execute()
        
        print(f"✅ Stored in Supabase: {filename}")
        return document_id
        
    except Exception as e:
        print(f"❌ Supabase storage error: {e}")
        return None

async def search_supabase_documents(query: str) -> List[str]:
    """Search documents in Supabase using full-text search"""
    if not supabase:
        return []
    
    try:
        # Use PostgreSQL full-text search
        result = supabase.table("document_chunks").select("content").text_search(
            "content", query, type="websearch", config="english"
        ).limit(5).execute()
        
        return [row["content"] for row in result.data]
        
    except Exception as e:
        print(f"❌ Supabase search error: {e}")
        return []

def search_documents(query, threshold=0.1):
    """Enhanced document search: in-memory + Supabase"""
    # First, search in-memory storage
    memory_docs = []
    if documents_store:
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        relevant_docs = []
        
        for doc_id, content in documents_store.items():
            content_lower = content.lower()
            content_words = set(content_lower.split())
            
            # Calculate simple word overlap score
            common_words = query_words.intersection(content_words)
            score = len(common_words) / len(query_words) if query_words else 0
            
            # Also check for phrase matches
            phrase_score = sum(1 for word in query_words if word in content_lower) / len(query_words)
            final_score = max(score, phrase_score)
            
            if final_score > threshold:
                relevant_docs.append((final_score, content))
        
        # Sort by relevance score
        relevant_docs.sort(key=lambda x: x[0], reverse=True)
        memory_docs = [doc[1] for doc in relevant_docs[:3]]
    
    # If we have in-memory results, use them
    if memory_docs:
        return memory_docs
    
    # Otherwise, try Supabase (this is async but we'll handle it)
    return []

@app.on_event("startup")
async def startup_event():
    """Startup message"""
    storage_mode = "Hybrid (Memory + Supabase)" if supabase else "In-Memory Only"
    print(f"🚀 Starting AI Chatbot API - {storage_mode}")
    if supabase:
        print("💾 Supabase backup storage enabled")
    else:
        print("📝 Note: Documents are stored in memory only")

@app.get("/")
def health_check():
    storage_mode = "hybrid" if supabase else "memory-only"
    return {
        "status": "ok", 
        "message": f"AI Chatbot API is running in {storage_mode} mode!",
        "supabase_enabled": bool(supabase),
        "storage_mode": storage_mode
    }

@app.get("/test")
def test_endpoint():
    """Test endpoint to verify connections"""
    supabase_status = bool(supabase)
    gemini_status = bool(GOOGLE_API_KEY)
    
    # Test Supabase connection
    doc_count_supabase = 0
    if supabase:
        try:
            count_result = supabase.table("documents").select("id", count="exact").execute()
            doc_count_supabase = count_result.count or 0
        except Exception as e:
            print(f"Supabase test error: {e}")
    
    return {
        "status": "success",
        "message": "Connection test successful!",
        "supabase_configured": supabase_status,
        "gemini_configured": gemini_status,
        "documents_memory": len(documents_store),
        "documents_supabase": doc_count_supabase,
        "storage_mode": "hybrid" if supabase else "memory-only",
        "supabase_url": "https://kfekhrbilvrobunqwgzd.supabase.co" if supabase else None
    }

@app.post("/login")
def login(request: LoginRequest):
    """Simple mock login"""
    return {"success": True, "token": "demo-token", "user": {"email": request.email}}

@app.get("/api/v1/data/sources")
async def get_data_sources():
    """Get list of uploaded documents from both memory and Supabase"""
    sources = []
    
    # Add memory sources
    for doc_id, content in documents_store.items():
        existing_metadata = next((doc for doc in documents_metadata if doc['id'] == doc_id), None)
        if existing_metadata:
            sources.append(existing_metadata)
    
    # Add Supabase sources if available
    if supabase:
        try:
            result = supabase.table("documents").select("*").order("upload_date", desc=True).execute()
            
            for doc in result.data:
                # Avoid duplicates and format for frontend compatibility
                if not any(s["id"] == doc["filename"] for s in sources):
                    sources.append({
                        "id": doc["filename"],
                        "name": doc["original_filename"],
                        "type": doc["file_type"],
                        "status": doc["status"],
                        "dateAdded": doc["upload_date"],
                        "size": f"{doc['file_size'] / 1024:.1f} KB"
                    })
        except Exception as e:
            print(f"Error getting Supabase sources: {e}")
    
    return {"sources": sources}

@app.post("/api/v1/data/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload and process files to both memory and Supabase"""
    try:
        uploaded_files = []
        
        for file in files:
            if not file.filename.lower().endswith('.pdf'):
                continue
                
            # Read file content
            content = await file.read()
            
            # Extract text
            text_content = extract_text_from_pdf_bytes(content)
            
            if not text_content:
                continue
            
            # Store in memory (primary)
            doc_id = file.filename
            metadata = {
                "id": doc_id,
                "name": file.filename,
                "type": "pdf",
                "status": "indexed",
                "dateAdded": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "size": f"{len(content) / 1024:.1f} KB"
            }
            
            documents_store[doc_id] = text_content
            
            # Remove existing metadata and add new
            documents_metadata[:] = [doc for doc in documents_metadata if doc['id'] != doc_id]
            documents_metadata.append(metadata)
            
            # Store in Supabase (backup)
            await store_in_supabase(file.filename, content, text_content)
            
            uploaded_files.append(file.filename)
            print(f"✅ Processed: {file.filename}")
        
        storage_info = "memory + Supabase" if supabase else "memory only"
        return {
            "message": f"Successfully uploaded {len(uploaded_files)} files to {storage_info}",
            "files": uploaded_files,
            "storage": storage_info
        }
        
    except Exception as e:
        print(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/data/sources/{source_id}")
async def delete_source(source_id: str):
    """Delete a document from both memory and Supabase"""
    try:
        # Remove from memory
        if source_id in documents_store:
            del documents_store[source_id]
        
        documents_metadata[:] = [doc for doc in documents_metadata if doc['id'] != source_id]
        
        # Remove from Supabase
        if supabase:
            try:
                doc_result = supabase.table("documents").select("*").eq("filename", source_id).execute()
                
                if doc_result.data:
                    document = doc_result.data[0]
                    
                    # Delete from storage
                    if document["storage_path"]:
                        try:
                            supabase.storage.from_("documents").remove([document["storage_path"]])
                        except Exception as e:
                            print(f"Storage deletion error: {e}")
                    
                    # Delete from database
                    supabase.table("documents").delete().eq("id", document["id"]).execute()
                    print(f"✅ Deleted from Supabase: {source_id}")
            except Exception as e:
                print(f"❌ Supabase deletion error: {e}")
        
        return {"message": "Document deleted successfully"}
        
    except Exception as e:
        print(f"Delete error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.options("/api/v1/chat")
def chat_options():
    """Handle CORS preflight for chat endpoint"""
    return {"status": "ok"}

@app.post("/api/v1/chat")
async def chat(request: ChatRequest, req: Request = None):
    """Enhanced chat endpoint with hybrid search"""
    try:
        print(f"💬 Chat request: {request.question}")
        
        if not GOOGLE_API_KEY:
            return {"answer": "Google Gemini API is not configured. Please add GOOGLE_API_KEY to your environment variables."}
        
        # Check both storage systems
        has_documents = bool(documents_store) or (supabase and await check_supabase_documents())
        
        if not has_documents:
            return {"answer": "No documents have been uploaded yet. Please upload some PDF documents first through the admin panel."}
        
        # Search for relevant documents (memory first, then Supabase)
        relevant_docs = search_documents(request.question)
        
        # If no memory results, try Supabase
        if not relevant_docs and supabase:
            relevant_docs = await search_supabase_documents(request.question)
        
        if not relevant_docs:
            return {"answer": "I couldn't find any relevant information in the uploaded documents for your question. Try uploading more specific documents or rephrasing your question."}
        
        # Prepare context for Gemini
        context = "\n\n".join(relevant_docs[:3])
        
        prompt = f"""You are an AI assistant that answers questions based on uploaded documents. Please provide accurate, helpful answers based solely on the information provided.

Document Content:
{context}

User Question: {request.question}

Instructions:
- Answer the question based only on the information in the documents above
- Be specific and detailed when possible
- If the exact information isn't available, say so clearly
- Keep your answer concise but informative
- Use a friendly, helpful tone

Answer:"""
        
        # Call Gemini API
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            answer = response.text
            
            # Store conversation in Supabase (optional)
            if supabase:
                try:
                    conversation_data = {
                        "user_question": request.question,
                        "ai_response": answer,
                        "relevant_documents": [doc[:100] + "..." for doc in relevant_docs],
                        "response_time_ms": 0,
                    }
                    if req:
                        conversation_data["user_agent"] = req.headers.get("user-agent")
                        conversation_data["ip_address"] = req.client.host if req.client else None
                    
                    supabase.table("chat_conversations").insert(conversation_data).execute()
                except Exception as e:
                    print(f"Warning: Failed to store conversation: {e}")
            
            print(f"✅ Generated answer: {answer[:100]}...")
            return {"answer": answer}
            
        except Exception as e:
            print(f"❌ Gemini API error: {e}")
            return {"answer": f"I found relevant information in the documents, but encountered an error generating the response: {str(e)}"}
    
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return {"answer": "I'm sorry, I encountered an error while processing your question. Please try again."}

async def check_supabase_documents():
    """Check if there are any documents in Supabase"""
    if not supabase:
        return False
    
    try:
        result = supabase.table("documents").select("id", count="exact").limit(1).execute()
        return (result.count or 0) > 0
    except Exception:
        return False

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)