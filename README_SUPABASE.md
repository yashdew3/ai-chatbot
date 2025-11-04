# AI Chatbot with Supabase Integration

This project provides an AI-powered chatbot system with persistent document storage using Supabase. Users can upload documents and chat with an AI assistant that answers questions based on the uploaded content.

## Features

- 📄 **Document Upload**: Support for PDF files with text extraction
- 🤖 **AI Chat**: Powered by Google Gemini for intelligent responses
- 💾 **Persistent Storage**: Documents stored in Supabase database and storage
- 🔍 **Smart Search**: Full-text search across document content
- 🌐 **Two Interfaces**:
  - Admin interface for document management
  - Public chat demo for end users
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Architecture

### Frontend (React + TypeScript)
- **Home Page** (`/`): Overview with admin and demo links
- **Chat Demo** (`/chat`): Public-facing chat interface
- **Admin Dashboard** (`/admin`): Document management and analytics

### Backend (Python + FastAPI)
- **Document Processing**: PDF text extraction and chunking
- **Database Integration**: Supabase for persistent storage
- **AI Integration**: Google Gemini for generating responses
- **Search Engine**: PostgreSQL full-text search

### Database Schema (Supabase)
- `documents`: Metadata for uploaded files
- `document_chunks`: Processed text chunks for search
- `chat_conversations`: Chat history for analytics
- Storage bucket for actual file storage

## Setup Instructions

### 1. Supabase Setup

The Supabase database has been configured with the following tables:
- ✅ `documents` table created
- ✅ `document_chunks` table created  
- ✅ `chat_conversations` table created
- ✅ Storage bucket `documents` created

**Supabase Project URL**: https://kfekhrbilvrobunqwgzd.supabase.co

You'll need to get your Supabase anon key from the project settings.

### 2. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Run the setup script:
   ```bash
   setup_supabase.bat
   ```

3. Edit the `.env` file and add your API keys:
   ```
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   SUPABASE_ANON_KEY=your_supabase_anon_key_here
   ```

4. Start the backend server:
   ```bash
   start_supabase.bat
   ```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## API Keys Required

### Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file as `GOOGLE_API_KEY`

### Supabase Anon Key
1. Go to your Supabase project settings
2. Navigate to API settings
3. Copy the "anon public" key
4. Add it to your `.env` file as `SUPABASE_ANON_KEY`

## Usage

### For Administrators
1. Visit `http://localhost:5173/admin`
2. Upload PDF documents via the Knowledge Base section
3. Monitor chat conversations and system health

### For End Users
1. Visit `http://localhost:5173/chat`
2. Start chatting with the AI assistant
3. Ask questions about the uploaded documents

## API Endpoints

### Document Management
- `POST /api/v1/data/upload` - Upload PDF files
- `GET /api/v1/data/sources` - List uploaded documents
- `DELETE /api/v1/data/sources/{source_id}` - Delete a document

### Chat Interface
- `POST /api/v1/chat` - Send a chat message and get AI response

### System
- `GET /` - Health check
- `GET /test` - Connection test with detailed status

## Database Tables

### documents
- Stores metadata for uploaded files
- Includes filename, size, upload date, processing status
- Links to storage bucket for actual files

### document_chunks
- Contains processed text chunks from documents
- Enables efficient full-text search
- Includes content hashing for deduplication

### chat_conversations
- Records all chat interactions
- Includes user questions, AI responses, and metadata
- Useful for analytics and improving the system

## Technology Stack

**Frontend:**
- React 18 with TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- shadcn/ui components
- React Router for navigation

**Backend:**
- Python 3.8+
- FastAPI for REST API
- Supabase for database and storage
- Google Gemini for AI responses
- PyPDF2 for PDF processing

**Database:**
- PostgreSQL (via Supabase)
- Full-text search capabilities
- File storage with Supabase Storage

## Deployment Notes

### Environment Variables
Ensure all required environment variables are set:
- `GOOGLE_API_KEY`: For AI responses
- `SUPABASE_ANON_KEY`: For database access
- `PORT`: Backend port (optional, defaults to 8000)

### Security Considerations
- Currently no authentication for demo purposes
- File uploads limited to PDF format
- CORS configured for development and production URLs

## Troubleshooting

### Backend Issues
1. Check if all dependencies are installed: `pip install -r requirements_supabase.txt`
2. Verify API keys in `.env` file
3. Test database connection with `GET /test` endpoint

### Frontend Issues
1. Ensure backend is running on port 8000
2. Check browser console for errors
3. Verify API endpoint configuration

### Database Issues
1. Check Supabase project status
2. Verify anon key permissions
3. Check table creation in Supabase dashboard

## Contributing

This is a demo project showcasing AI chatbot integration with Supabase. Feel free to extend it with additional features like:
- User authentication
- Multiple file format support
- Advanced analytics dashboard
- Conversation memory
- Custom AI model fine-tuning