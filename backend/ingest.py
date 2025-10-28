import os
from dotenv import load_dotenv

# Import updated LangChain components from langchain_community
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    YoutubeLoader,
)
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Load environment variables from .env file
load_dotenv()

# --- 1. Define Constants ---
# Path to the directory where uploaded documents are stored
DATA_PATH = "data"
# Path to the directory where the Chroma vector database will be persisted
DB_PATH = "chroma_db"
# Name of the Hugging Face embedding model to use
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# --- 2. Define Document Loaders for different file types ---
DOCUMENT_LOADERS = {
    ".pdf": PyPDFLoader,
    ".docx": UnstructuredWordDocumentLoader,
    ".doc": UnstructuredWordDocumentLoader,
}

def load_documents(data_path):
    """
    Loads all supported documents from the specified data path.
    Returns a list of LangChain Document objects.
    """
    documents = []
    print(f"Scanning for documents in: {data_path}")
    for filename in os.listdir(data_path):
        file_path = os.path.join(data_path, filename)
        _, ext = os.path.splitext(filename)
        
        if ext in DOCUMENT_LOADERS:
            try:
                print(f"Loading document: {filename}")
                loader_class = DOCUMENT_LOADERS[ext]
                loader = loader_class(file_path)
                documents.extend(loader.load())
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    
    print(f"Successfully loaded {len(documents)} documents.")
    return documents

def load_youtube_videos(urls):
    """
    Loads transcripts from a list of YouTube video URLs.
    Returns a list of LangChain Document objects.
    """
    documents = []
    print(f"Loading YouTube transcripts for {len(urls)} video(s)...")
    for url in urls:
        try:
            print(f"Loading transcript for: {url}")
            loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
            documents.extend(loader.load())
        except Exception as e:
            print(f"Error loading YouTube URL {url}: {e}")
    
    print(f"Successfully loaded {len(documents)} YouTube transcripts.")
    return documents

def split_text(documents):
    """
    Splits the text of the loaded documents into smaller chunks.
    """
    print("Splitting documents into text chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")
    return chunks

def create_vector_store(chunks):
    """
    Creates and persists a Chroma vector store from the text chunks.
    """
    print("Creating embeddings and vector store...")
    
    # Initialize the embedding model
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    # Create the vector store from the chunks and embeddings
    # This will automatically create the embeddings and store them.
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    
    print(f"Vector store created and saved to: {DB_PATH}")
    return vector_store

def main():
    """
    Main function to run the ingestion pipeline.
    """
    print("--- Starting Ingestion Pipeline ---")
    
    # For now, we'll manually define a YouTube URL to test.
    # In the next step, our API will pass these in dynamically.
    youtube_urls = [
        # Example URL - replace with any YouTube video you want to test
        "https://www.youtube.com/watch?v=8C_kHJ5YEiA" 
    ]
    
    # Load all documents from files and YouTube
    all_documents = []
    all_documents.extend(load_documents(DATA_PATH))
    all_documents.extend(load_youtube_videos(youtube_urls))
    
    if not all_documents:
        print("No new documents or videos to process. Exiting.")
        return

    # Split the documents into chunks
    text_chunks = split_text(all_documents)
    
    # Create and persist the vector store
    create_vector_store(text_chunks)
    
    print("--- Ingestion Pipeline Complete ---")

if __name__ == "__main__":
    main()