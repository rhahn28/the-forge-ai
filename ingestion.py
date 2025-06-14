# ingestion.py
import os
import json
from dotenv import load_dotenv

# We will use pytesseract directly for images
import pytesseract
from PIL import Image
from langchain_core.documents import Document

# We still need these loaders for other file types
from langchain_community.document_loaders import (
    UnstructuredMarkdownLoader,
    PyPDFLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

# --- Configuration ---
KNOWLEDGE_DIR = "knowledge"
VECTOR_DB_DIR = "chroma_db"
# IMPORTANT: If Tesseract is not in your system PATH, you must specify its location.
# Example for Windows:
# TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def load_documents_from_directory(directory_path):
    """
    Loads all supported files, using our own robust OCR logic for images.
    """
    all_docs = []
    print(f"Scanning directory: '{directory_path}'...")

    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            ext = "." + file_name.rsplit(".", 1)[-1].lower() if "." in file_name else ""

            try:
                print(f"Processing file: {file_path}")
                docs_from_file = []
                if ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
                    # --- OUR NEW, ROBUST IMAGE HANDLING LOGIC ---
                    image_text = pytesseract.image_to_string(Image.open(file_path))
                    if image_text.strip():
                        docs_from_file = [Document(page_content=image_text, metadata={"source": file_path})]
                        print(f"  -> Successfully extracted text via OCR.")
                elif ext == ".md":
                    loader = UnstructuredMarkdownLoader(file_path)
                    docs_from_file = loader.load()
                elif ext == ".pdf":
                    loader = PyPDFLoader(file_path)
                    docs_from_file = loader.load()
                
                if docs_from_file:
                    all_docs.extend(docs_from_file)
                else:
                    print(f"  -> ⚠️ WARNING: No content extracted from file {file_path}.")

            except Exception as e:
                print(f"--- ⚠️ WARNING: Failed to process file {file_path}. Error: {e} ---")
                
    return all_docs

def main():
    print("--- Starting robust knowledge base ingestion ---")
    
    if os.path.exists(VECTOR_DB_DIR):
        import shutil
        print(f"Removing old database at '{VECTOR_DB_DIR}'...")
        shutil.rmtree(VECTOR_DB_DIR)

    all_docs = load_documents_from_directory(KNOWLEDGE_DIR)
    
    if not all_docs:
        print("No processable documents found. Exiting."); return

    print(f"✅ Loaded a total of {len(all_docs)} documents.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(all_docs)
    print(f"✅ Split documents into {len(splits)} chunks.")

    if not splits:
        print("--- ⚠️ WARNING: No text chunks were generated. ---"); return

    print("Initializing local embedding model...")
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    print("Creating vector store...")
    Chroma.from_documents(
        documents=splits,
        embedding=embedding_model,
        persist_directory=VECTOR_DB_DIR
    )
    print(f"--- ✅ Ingestion complete. Vector store saved to '{VECTOR_DB_DIR}' ---")

if __name__ == "__main__":
    main()