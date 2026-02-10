"""Configuration for the RAG electrical product system."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# API keys
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"

# Document folders (electrical product data)
PDFs_DIR = DOCUMENTS_DIR / "PDFs"
TEXT_FILES_DIR = DOCUMENTS_DIR / "Text_Files"
CSVs_DIR = DOCUMENTS_DIR / "CSVs"
XMLs_DIR = DOCUMENTS_DIR / "XMLs"
JSONs_DIR = DOCUMENTS_DIR / "JSONs"
XLS_DIR = DOCUMENTS_DIR / "XLS"

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", str(DATA_DIR / "chroma_db"))

# RAG settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RETRIEVAL = 5
# Use OpenAI embeddings if OPENAI_API_KEY set; else sentence-transformers (no API key)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# Ensure directories exist
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
for _dir in (PDFs_DIR, TEXT_FILES_DIR, CSVs_DIR, XMLs_DIR, JSONs_DIR, XLS_DIR):
    _dir.mkdir(parents=True, exist_ok=True)
Path(CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
