"""RAG pipeline: load documents, embed, store in Chroma, query with DeepSeek and source references."""
from pathlib import Path
from typing import Any

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
    CHROMA_PERSIST_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K_RETRIEVAL,
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    SENTENCE_TRANSFORMER_MODEL,
)
from document_loaders import load_all_documents


def get_embeddings():
    """Use OpenAI embeddings if API key set; else sentence-transformers (no API key)."""
    if OPENAI_API_KEY:
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model=EMBEDDING_MODEL)
    from langchain_community.embeddings import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name=SENTENCE_TRANSFORMER_MODEL)


def get_llm():
    """DeepSeek chat model (OpenAI-compatible API)."""
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model=DEEPSEEK_MODEL,
        openai_api_key=DEEPSEEK_API_KEY,
        openai_api_base=DEEPSEEK_BASE_URL,
        temperature=0,
    )


def build_vector_store(force_rebuild: bool = False) -> Any:
    """Load documents, chunk, embed, and persist to Chroma. Returns the Chroma vector store."""
    from langchain_chroma import Chroma

    embeddings = get_embeddings()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    if not force_rebuild:
        try:
            store = Chroma(
                persist_directory=CHROMA_PERSIST_DIR,
                embedding_function=embeddings,
            )
            if store._collection.count() > 0:
                return store
        except Exception:
            pass

    docs = load_all_documents()
    if not docs:
        raise ValueError("No documents loaded. Add files to data/documents subfolders (PDFs, Text_Files, CSVs, XMLs, JSONs, XLS).")
    chunks = splitter.split_documents(docs)
    store = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
    )
    return store


def query(
    question: str,
    vector_store: Any = None,
    return_sources: bool = True,
) -> dict[str, Any]:
    """
    Answer a question over the indexed electrical product documents using DeepSeek.
    Returns answer text and, if return_sources, the list of source documents.
    """
    if vector_store is None:
        vector_store = build_vector_store()
    if not DEEPSEEK_API_KEY:
        return {
            "answer": "Set DEEPSEEK_API_KEY in .env to use the LLM.",
            "sources": [],
        }

    retriever = vector_store.as_retriever(search_kwargs={"k": TOP_K_RETRIEVAL})
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You answer questions about electrical products (bulbs, cables, wires, switches) using only the provided context. If the context does not contain the answer, say so. Be concise."),
        ("human", "Context:\n{context}\n\nQuestion: {question}"),
    ])

    def format_docs(docs: list[Document]) -> str:
        return "\n\n---\n\n".join(d.page_content for d in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = chain.invoke(question)
    out: dict[str, Any] = {"answer": answer}
    if return_sources:
        source_docs = retriever.invoke(question)
        out["sources"] = [
            {"content": d.page_content[:500], "metadata": d.metadata}
            for d in source_docs
        ]
    return out
