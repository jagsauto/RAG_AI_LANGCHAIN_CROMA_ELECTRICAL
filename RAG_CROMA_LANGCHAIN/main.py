"""CLI for the RAG electrical product system: index documents and query with DeepSeek."""
import argparse
import sys
from pathlib import Path

# Ensure project root on path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import DEEPSEEK_API_KEY
from document_loaders import load_all_documents
from rag import build_vector_store, query


def cmd_index(force: bool) -> None:
    docs = load_all_documents()
    print(f"Loaded {len(docs)} document(s).")
    if not docs:
        print("Add files to data/documents subfolders: PDFs, Text_Files, CSVs, XMLs, JSONs, XLS.")
        return
    store = build_vector_store(force_rebuild=force)
    print("Vector store ready (Chroma).")


def cmd_query(question: str, no_sources: bool) -> None:
    if not DEEPSEEK_API_KEY:
        print("Set DEEPSEEK_API_KEY in .env to use the LLM.")
        return
    result = query(question, return_sources=not no_sources)
    print(result["answer"])
    if result.get("sources"):
        print("\n--- Sources ---")
        for i, s in enumerate(result["sources"], 1):
            src = s.get("metadata", {}).get("source", "?")
            print(f"  {i}. {src}")
            print(f"     {s.get('content', '')[:200]}...")


def main() -> None:
    parser = argparse.ArgumentParser(description="RAG for electrical product data (LangChain + DeepSeek)")
    sub = parser.add_subparsers(dest="command", required=True)
    idx = sub.add_parser("index", help="Load and index documents into the vector store")
    idx.add_argument("--force", action="store_true", help="Force rebuild index")
    q = sub.add_parser("query", help="Ask a question over the documents")
    q.add_argument("question", nargs="+", help="Question (words)")
    q.add_argument("--no-sources", action="store_true", help="Do not print source refs")
    args = parser.parse_args()

    if args.command == "index":
        cmd_index(force=getattr(args, "force", False))
    elif args.command == "query":
        cmd_query(question=" ".join(args.question), no_sources=args.no_sources)


if __name__ == "__main__":
    main()
