# RAG Framework for Electrical Product Data

Python RAG (Retrieval-Augmented Generation) system using **LangChain** to search and query documents about electrical products (bulbs, cables, wires, switches). Uses **DeepSeek** as the LLM (with your API key).

## Document types supported

- **PDF** – product sheets, manuals  
- **CSV** – product tables  
- **Plain text** (.txt) – specs, descriptions  
- **Word** (.doc, .docx)  
- **Excel** (.xls, .xlsx) – price lists, inventories  
- **XML** – structured product data  
- **JSON** – product catalogs  

## Setup

1. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set your DeepSeek API key**

   Create a `.env` file in the project root:

   ```
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   ```

   Optional: if you have an OpenAI API key, you can use OpenAI embeddings (faster, cloud-based). Otherwise the app uses local **sentence-transformers** embeddings (no extra API key).

   ```
   OPENAI_API_KEY=your_openai_key   # optional, for embeddings
   ```

3. **Generate sample documents (optional)**

   The repo includes sample text, CSV, XML, and JSON under `data/documents/`. To add sample PDF, Excel, and Word files:

   ```bash
   python scripts/create_sample_docs.py
   ```

## Folder layout for your data

Place your electrical product files in:

- `data/documents/PDFs/` – PDFs  
- `data/documents/Text_Files/` – .txt, .doc, .docx  
- `data/documents/CSVs/` – .csv  
- `data/documents/XMLs/` – .xml  
- `data/documents/JSONs/` – .json  
- `data/documents/XLS/` – .xls, .xlsx  

## Usage

**Index documents** (load, chunk, embed, store in Chroma):

```bash
python main.py index
```

Force rebuild of the index:

```bash
python main.py index --force
```

**Ask questions** (answers use DeepSeek and retrieved chunks; sources are printed):

```bash
python main.py query "What is the price of the 2.5mm cable?"
python main.py query "Which bulbs are available?" --no-sources
```

## Features

- Load and index documents from all supported formats  
- Embed and store text chunks in a **Chroma** vector store  
- Answer questions over the documents using the **DeepSeek** LLM  
- Return answers with **source references** (file path and snippet)  

## Configuration

See `config.py` and `.env` for:

- `CHUNK_SIZE`, `CHUNK_OVERLAP` – text splitting  
- `TOP_K_RETRIEVAL` – number of chunks passed to the LLM  
- `DEEPSEEK_MODEL` – e.g. `deepseek-chat`  
- `DEEPSEEK_BASE_URL` – API base URL (default: https://api.deepseek.com)  
