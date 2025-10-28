import os
import uvicorn
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import PyPDF2
import google.generativeai as genai
from dotenv import load_dotenv
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

# Initialize FastAPI
app = FastAPI(title="AI Chatbot API - Free Tier", version="2.0.0")

# CORS Configuration
FRONTEND_URLS = [
    "http://localhost:3000",
    "http://localhost:8080", 
    "https://ai-chatbot-app.onrender.com",
    "https://*.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_URLS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage ONLY (no file system dependency)
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

def search_documents(query, threshold=0.1):
    """Simple keyword-based document search"""
    if not documents_store:
        return []
    
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
    return [doc[1] for doc in relevant_docs[:3]]  # Top 3 documents

@app.on_event("startup")
async def startup_event():
    """Startup message for free tier deployment"""
    print("🚀 Starting AI Chatbot API - Free Tier Mode")
    print("📝 Note: Documents are stored in memory only")
    print("🔄 Documents will be lost when service restarts/sleeps")
    print("💡 Users will need to re-upload documents after cold starts")

@app.get("/")
def health_check():
    return {
        "status": "ok", 
        "message": "AI Chatbot API is running on Free Tier!",
        "mode": "in-memory-only",
        "note": "Documents are temporary and lost on restart"
    }

@app.get("/test")
def test_endpoint():
    return {
        "status": "success",
        "message": "Connection test successful!",
        "documents_loaded": len(documents_store),
        "gemini_configured": bool(GOOGLE_API_KEY),
        "storage_mode": "in-memory-only",
        "free_tier": True,
        "environment": "production" if os.getenv("PORT") else "development"
    }

@app.post("/login")
def login(request: LoginRequest):
    # Simple mock login
    return {"success": True, "token": "mock-token", "user": {"email": request.email}}

@app.get("/api/v1/data/sources")
def get_data_sources():
    """Get list of uploaded documents (in-memory only)"""
    try:
        return {"sources": documents_metadata}
    except Exception as e:
        print(f"Error getting sources: {e}")
        return {"sources": []}

@app.post("/api/v1/data/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload and process files (in-memory only)"""
    try:
        uploaded_files = []
        
        for file in files:
            if not file.filename.endswith('.pdf'):
                continue
                
            # Read file content into memory
            content = await file.read()
            
            # Extract text directly from bytes (no file system storage)
            text_content = extract_text_from_pdf_bytes(content)
            
            if not text_content:
                continue
            
            # Create metadata
            doc_id = file.filename
            metadata = {
                "id": doc_id,
                "name": file.filename,
                "type": "pdf",
                "status": "indexed",
                "dateAdded": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "size": f"{len(content) / 1024:.1f} KB"
            }
            
            # Store in memory ONLY
            documents_store[doc_id] = text_content
            
            # Add to metadata list (avoid duplicates)
            existing_doc = next((doc for doc in documents_metadata if doc['id'] == doc_id), None)
            if existing_doc:
                documents_metadata.remove(existing_doc)
            documents_metadata.append(metadata)
            
            uploaded_files.append(file.filename)
            print(f"✅ Processed in memory: {file.filename}")
        
        return {
            "message": f"Successfully uploaded {len(uploaded_files)} files to memory",
            "files": uploaded_files,
            "note": "Files are stored in memory only and will be lost on service restart"
        }
        
    except Exception as e:
        print(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/data/sources/{source_id}")
def delete_source(source_id: str):
    """Delete a document source (from memory)"""
    try:
        # Remove from memory
        if source_id in documents_store:
            del documents_store[source_id]
        
        # Remove from metadata
        documents_metadata[:] = [doc for doc in documents_metadata if doc['id'] != source_id]
        
        return {"message": "Source deleted successfully from memory"}
        
    except Exception as e:
        print(f"Delete error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/chat")
def chat(request: ChatRequest):
    """Chat endpoint with document search"""
    try:
        print(f"💬 Chat request: {request.question}")
        
        if not GOOGLE_API_KEY:
            return {"answer": "Google Gemini API is not configured. Please add GOOGLE_API_KEY to your environment variables."}
        
        if not documents_store:
            return {"answer": "No documents have been uploaded yet. Please upload some PDF documents first! Note: On free tier, documents are stored temporarily and may be lost when the service restarts."}
        
        # Search for relevant documents
        relevant_docs = search_documents(request.question)
        
        if not relevant_docs:
            return {"answer": "I couldn't find any relevant information in the uploaded documents for your question. Try uploading more specific documents or rephrasing your question."}
        
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
            
            print(f"✅ Generated answer: {answer[:100]}...")
            return {"answer": answer}
            
        except Exception as e:
            print(f"❌ Gemini API error: {e}")
            return {"answer": f"I found relevant information in the documents, but encountered an error generating the response: {str(e)}"}
    
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return {"answer": "I'm sorry, I encountered an error while processing your question. Please try again."}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)