import subprocess
import sys
import os
from threading import Thread
import time

def run_backend():
    """Run FastAPI backend"""
    os.system("uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")

def run_frontend():
    """Run Streamlit frontend"""
    time.sleep(5)  # Wait for backend to start
    os.system("streamlit run frontend/streamlit_app.py --server.port 8501")

if __name__ == "__main__":
    print("Starting IntelliDoc Application...")
    print("Backend will be available at: http://localhost:8000")
    print("Frontend will be available at: http://localhost:8501")
    print("API Documentation: http://localhost:8000/docs")
    
    # Start backend in a separate thread
    backend_thread = Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Start frontend
    run_frontend()

# Installation and Setup Instructions

"""
1. Create a virtual environment:
   python -m venv intellidoc_env
   source intellidoc_env/bin/activate  # On Windows: intellidoc_env\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Set up environment variables:
   Create a .env file with the following:
   DATABASE_URL=sqlite:///./intellidoc.db
   SECRET_KEY=your-secret-key-here
   HUGGINGFACE_API_KEY=your-hf-api-key (optional)

4. Install system dependencies:
   - For OCR: Install Tesseract OCR
     - Ubuntu: sudo apt-get install tesseract-ocr
     - macOS: brew install tesseract
     - Windows: Download from GitHub

5. Run the application:
   python run_app.py

6. Access the application:
   - Frontend: http://localhost:8501
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

Features:
- User authentication
- Document upload and processing
- AI-powered document classification
- Text extraction from PDFs, DOCX, images
- Document question answering
- Semantic search across documents
- Analytics dashboard
- Multi-language support
- Vector database for similarity search
"""