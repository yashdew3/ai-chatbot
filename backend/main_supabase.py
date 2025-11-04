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
from supabase import create_client, Client
import io

# Load environment variables
load_dotenv()

# Configure Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    print("✓ Google Gemini API configured")
else:
    print("✗ Warning: GOOGLE_API_KEY not found in environment variables")

# Configure Supabase
SUPABASE_URL = "https://kfekhrbilvrobunqwgzd.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

if SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✓ Supabase client configured")
else:
    print("✗ Warning: SUPABASE_ANON_KEY not found in environment variables")
    supabase = None

# Initialize FastAPI
app = FastAPI(title="AI Chatbot API - Supabase Edition", version="3.0.0")

# CORS Configuration
FRONTEND_URLS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080", 
    "https://ai-chatbot-frontend-xxxx.onrender.com",  # Update with your actual frontend URL
    "https://*.onrender.com",
    "*"  # Allow all origins for demo - remove this in production for security
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_URLS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware to log all requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    print(f"🌐 {request.method} {request.url.path} - Client: {request.client.host if request.client else 'Unknown'}")
    
    response = await call_next(request)
    
    process_time = (datetime.now() - start_time).total_seconds()
    print(f"⚡ Response: {response.status_code} - Time: {process_time:.3f}s")
    
    return response

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

async def store_document_in_supabase(filename: str, file_content: bytes, content: str):
    """Store document and its chunks in Supabase"""
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    
    try:
        print(f"🔄 Starting upload process for: {filename}")
        
        # Store file in Supabase storage
        file_path = f"uploads/{uuid.uuid4()}_{filename}"
        print(f"📁 Uploading to storage path: {file_path}")
        
        storage_result = supabase.storage.from_("documents").upload(file_path, file_content)
        print(f"✅ Storage upload result: {storage_result}")
        
        # Create document record
        print(f"💾 Creating document record in database...")
        document_data = {
            "filename": filename,
            "original_filename": filename,
            "file_type": "pdf",
            "file_size": len(file_content),
            "content_preview": content[:500] + "..." if len(content) > 500 else content,
            "status": "processing",
            "storage_path": file_path,
        }
        
        doc_result = supabase.table("documents").insert(document_data).execute()
        print(f"✅ Document record created: {doc_result}")
        document_id = doc_result.data[0]["id"]
        print(f"🆔 Document ID: {document_id}")
        
        # Split content into chunks and store
        chunks = chunk_text(content)
        print(f"📝 Created {len(chunks)} chunks from document")
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
            chunk_result = supabase.table("document_chunks").insert(chunk_data).execute()
            print(f"✅ Chunks inserted: {len(chunk_data)} chunks")
        
        # Update document status
        update_result = supabase.table("documents").update({
            "status": "indexed",
            "processed_date": datetime.now().isoformat()
        }).eq("id", document_id).execute()
        print(f"✅ Document status updated to indexed")
        
        print(f"🎉 Successfully stored document {filename} with ID: {document_id}")
        return document_id
        
    except Exception as e:
        print(f"❌ Error storing document in Supabase: {e}")
        print(f"❌ Error type: {type(e)}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Failed to store document: {str(e)}")

async def search_documents_supabase(query: str) -> List[str]:
    """Enhanced search function with flexible keyword matching"""
    if not supabase:
        return []
    
    try:
        print(f"🔍 Searching for: '{query}'")
        
        # Extract keywords from query (remove common words)
        stop_words = {'the', 'is', 'are', 'what', 'how', 'where', 'when', 'why', 'who', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'explain', 'tell', 'me', 'about'}
        keywords = [word.lower().strip() for word in query.split() if word.lower().strip() not in stop_words and len(word.strip()) > 2]
        print(f"🔑 Extracted keywords: {keywords}")
        
        if not keywords:
            # If no meaningful keywords, use the original query
            keywords = [query.lower().strip()]
        
        # Get all chunks and perform flexible search
        all_chunks_result = supabase.table("document_chunks").select("content, document_id, chunk_index").execute()
        all_chunks = all_chunks_result.data
        print(f"📊 Total chunks in database: {len(all_chunks)}")
        
        # Score chunks based on keyword matches
        scored_chunks = []
        for chunk in all_chunks:
            content_lower = chunk["content"].lower()
            score = 0
            matched_keywords = []
            
            # Check each keyword
            for keyword in keywords:
                if keyword in content_lower:
                    # Count occurrences for better scoring
                    occurrences = content_lower.count(keyword)
                    score += occurrences
                    matched_keywords.append(keyword)
            
            # Also check for partial matches and variations
            for keyword in keywords:
                # Check for word boundaries to avoid partial word matches
                import re
                if re.search(rf'\b{re.escape(keyword)}', content_lower):
                    score += 0.5  # Lower score for word boundary matches
            
            if score > 0:
                scored_chunks.append({
                    "content": chunk["content"],
                    "score": score,
                    "matched_keywords": matched_keywords,
                    "document_id": chunk["document_id"],
                    "chunk_index": chunk["chunk_index"]
                })
        
        # Sort by score (descending) and take top results
        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        top_chunks = scored_chunks[:8]  # Get more results for better context
        
        print(f"📊 Keyword search found: {len(top_chunks)} relevant chunks")
        for i, chunk in enumerate(top_chunks[:3]):  # Log top 3
            print(f"� Result {i+1} (score: {chunk['score']}, keywords: {chunk['matched_keywords']}): {chunk['content'][:150]}...")
        
        if top_chunks:
            return [chunk["content"] for chunk in top_chunks]
        
        # Fallback: If no keyword matches, try partial string matching
        print("🔄 No keyword matches found, trying partial string matching...")
        partial_matches = []
        query_words = query.lower().split()
        
        for chunk in all_chunks:
            content_lower = chunk["content"].lower()
            for word in query_words:
                if len(word) > 3 and word in content_lower:
                    partial_matches.append(chunk["content"])
                    break
            if len(partial_matches) >= 5:
                break
        
        print(f"📊 Partial matching found: {len(partial_matches)} chunks")
        return partial_matches
        
    except Exception as e:
        print(f"❌ Error in enhanced search: {e}")
        print(f"❌ Error type: {type(e)}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return []

@app.on_event("startup")
async def startup_event():
    """Startup message for Supabase edition"""
    print("🚀 Starting AI Chatbot API - Supabase Edition")
    print(f"📊 Database URL: {SUPABASE_URL}")
    print("💾 Documents stored persistently in Supabase")

@app.get("/")
def health_check():
    return {
        "status": "ok", 
        "message": "AI Chatbot API with Supabase is running!",
        "database": "supabase",
        "persistent_storage": True
    }

@app.get("/test")
def test_endpoint():
    """Test endpoint to verify connections"""
    supabase_status = bool(supabase)
    gemini_status = bool(GOOGLE_API_KEY)
    
    # Test database connection
    doc_count = 0
    chunk_count = 0
    if supabase:
        try:
            count_result = supabase.table("documents").select("id", count="exact").execute()
            doc_count = count_result.count
            chunk_result = supabase.table("document_chunks").select("id", count="exact").execute()
            chunk_count = chunk_result.count
        except Exception as e:
            print(f"Database test error: {e}")
    
    return {
        "status": "success",
        "message": "Connection test successful!",
        "supabase_configured": supabase_status,
        "gemini_configured": gemini_status,
        "documents_count": doc_count,
        "chunks_count": chunk_count,
        "storage_mode": "supabase",
        "database_url": SUPABASE_URL
    }

@app.get("/debug/chunks")
def debug_chunks():
    """Debug endpoint to inspect stored chunks"""
    if not supabase:
        return {"error": "Supabase not configured"}
    
    try:
        # Get all chunks with document info
        chunks = supabase.table("document_chunks").select(
            "id, document_id, chunk_index, content, content_length"
        ).order("document_id", desc=False).order("chunk_index", desc=False).execute()
        
        # Get document info
        docs = supabase.table("documents").select("id, filename, original_filename").execute()
        doc_lookup = {doc["id"]: doc for doc in docs.data}
        
        # Format for debugging
        debug_data = []
        for chunk in chunks.data:
            doc_info = doc_lookup.get(chunk["document_id"], {})
            debug_data.append({
                "chunk_id": chunk["id"],
                "document": doc_info.get("original_filename", "Unknown"),
                "chunk_index": chunk["chunk_index"],
                "content_preview": chunk["content"][:200] + "..." if len(chunk["content"]) > 200 else chunk["content"],
                "content_length": chunk["content_length"],
                "full_content": chunk["content"]  # Full content for debugging
            })
        
        return {
            "total_chunks": len(debug_data),
            "chunks": debug_data
        }
        
    except Exception as e:
        print(f"Debug chunks error: {e}")
        return {"error": str(e)}

@app.post("/login")
def login(request: LoginRequest):
    """Simple mock login (no auth required for demo)"""
    return {"success": True, "token": "demo-token", "user": {"email": request.email}}

@app.get("/api/v1/data/sources")
async def get_data_sources():
    """Get list of uploaded documents from Supabase"""
    if not supabase:
        return {"sources": []}
    
    try:
        result = supabase.table("documents").select("*").order("upload_date", desc=True).execute()
        
        # Format for frontend compatibility
        sources = []
        for doc in result.data:
            sources.append({
                "id": doc["filename"],  # Use filename as ID for compatibility
                "name": doc["original_filename"],
                "type": doc["file_type"],
                "status": doc["status"],
                "dateAdded": doc["upload_date"],
                "size": f"{doc['file_size'] / 1024:.1f} KB"
            })
        
        return {"sources": sources}
        
    except Exception as e:
        print(f"Error getting sources: {e}")
        return {"sources": []}

@app.post("/api/v1/data/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload and process files to Supabase"""
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
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
            
            # Store in Supabase
            print(f"🔄 Processing file: {file.filename}")
            print(f"📏 File size: {len(content)} bytes")
            print(f"📄 Text extracted: {len(text_content)} characters")
            
            document_id = await store_document_in_supabase(file.filename, content, text_content)
            uploaded_files.append(file.filename)
            
            print(f"🎯 Successfully processed: {file.filename} (ID: {document_id})")
        
        return {
            "message": f"Successfully uploaded {len(uploaded_files)} files to Supabase",
            "files": uploaded_files,
            "storage": "supabase"
        }
        
    except Exception as e:
        print(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/data/sources/{source_id}")
async def delete_source(source_id: str):
    """Delete a document from Supabase"""
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        # Find document by filename
        doc_result = supabase.table("documents").select("*").eq("filename", source_id).execute()
        
        if not doc_result.data:
            raise HTTPException(status_code=404, detail="Document not found")
        
        document = doc_result.data[0]
        
        # Delete from storage
        if document["storage_path"]:
            try:
                supabase.storage.from_("documents").remove([document["storage_path"]])
            except Exception as e:
                print(f"Storage deletion error: {e}")
        
        # Delete from database (cascades to chunks)
        supabase.table("documents").delete().eq("id", document["id"]).execute()
        
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
    """Chat endpoint with Supabase document search"""
    try:
        print(f"💬 Chat request: {request.question}")
        
        if not GOOGLE_API_KEY:
            return {"answer": "Google Gemini API is not configured. Please add GOOGLE_API_KEY to your environment variables."}
        
        if not supabase:
            return {"answer": "Database is not configured. Please check Supabase connection."}
        
        # Search for relevant documents in Supabase
        relevant_docs = await search_documents_supabase(request.question)
        
        print(f"🔍 Search results: Found {len(relevant_docs)} relevant documents")
        if relevant_docs:
            print(f"📄 First result preview: {relevant_docs[0][:200]}...")
        
        if not relevant_docs:
            # Let's check if there are any documents in the database at all
            try:
                total_docs = supabase.table("documents").select("id", count="exact").execute()
                total_chunks = supabase.table("document_chunks").select("id", count="exact").execute()
                print(f"📊 Database status: {total_docs.count} documents, {total_chunks.count} chunks")
                
                if total_docs.count == 0:
                    return {"answer": "No documents have been uploaded to the knowledge base yet. Please upload some documents first."}
                else:
                    return {"answer": f"I found {total_docs.count} documents in the knowledge base, but couldn't find relevant information for your specific question: '{request.question}'. Try rephrasing your question or using different keywords."}
            except Exception as db_check_error:
                print(f"❌ Database check error: {db_check_error}")
                return {"answer": "I couldn't find any relevant information in the knowledge base for your question. Please make sure documents have been uploaded to the system."}
        
        # Prepare context for Gemini
        context = "\n\n".join(relevant_docs[:3])  # Use top 3 matches
        
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
            try:
                conversation_data = {
                    "user_question": request.question,
                    "ai_response": answer,
                    "relevant_documents": [doc[:100] + "..." for doc in relevant_docs],  # Store truncated content
                    "response_time_ms": 0,  # Could measure actual time
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
            return {"answer": f"I found relevant information in the knowledge base, but encountered an error generating the response: {str(e)}"}
    
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return {"answer": "I'm sorry, I encountered an error while processing your question. Please try again."}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)