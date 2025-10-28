# Simple Chatbot Backend

This is a simplified, reliable backend that replaces the complex LangChain implementation with a basic but functional approach.

## Features
- Simple PDF text extraction
- Basic keyword-based document search
- Direct Google Gemini API integration
- Robust error handling (no server crashes)
- In-memory document storage for fast access

## Setup Instructions

### 1. Install Dependencies
Run the setup script to install required packages:
```cmd
setup_simple.bat
```

### 2. Configure Google API Key
Make sure your `.env` file contains:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Start the Backend
```cmd
start_simple_server.bat
```

### 4. Test the Backend
```cmd
test_simple_endpoints.bat
```

## How It Works

1. **File Upload**: PDFs are uploaded and text is extracted using PyPDF2
2. **Storage**: Document content is stored in memory and metadata in `documents.json`
3. **Search**: Simple keyword matching finds relevant documents
4. **Chat**: Google Gemini generates responses based on relevant document content

## API Endpoints

- `GET /test` - Health check
- `GET /api/v1/data/sources` - List uploaded documents
- `POST /api/v1/data/upload` - Upload PDF files
- `DELETE /api/v1/data/sources/{id}` - Delete a document
- `POST /api/v1/chat` - Chat with the AI assistant

## Troubleshooting

### Backend won't start
- Check if virtual environment is activated
- Run `setup_simple.bat` to install dependencies
- Check if port 8000 is available

### Chat not working
- Verify GOOGLE_API_KEY is set in .env file
- Upload some PDF documents first
- Check console output for error messages

### Documents not showing
- Check if files are in the `data` folder
- Check `documents.json` file for metadata
- Try refreshing the frontend page

## Migration from Complex Backend

If you want to use your existing documents:
1. Copy PDF files from old `data` folder to new `data` folder
2. Start the simple backend
3. The backend will automatically detect and process existing PDFs