"""Load documents from PDF, CSV, text, doc/docx, xls/xlsx, XML, and JSON."""
# rm -rf chroma_db db chroma
#  python3 main.py index --force
# python3 main.py query "What is the voltage rating for LED Bulb E27 15W?"
# python3 main.py query "What is the price of LED Bulb E27 15W?"
# python3 main.py query "What are the specifications of LED Bulb E27 15W?"
# python3 main.py query "What is the category of the product with SKU B-E27-15W?"
# python3 main.py query "How many lumens does the LED Bulb E27 15W produce?"

from pathlib import Path
from typing import Iterator

from langchain_core.documents import Document
from typing import Iterator, Optional

from config import (
    # PDFs_DIR,
    # TEXT_FILES_DIR,
    CSVs_DIR,
    # XMLs_DIR,
    JSONs_DIR,
    # XLS_DIR,
)


def _metadata(source: Path) -> dict:
    return {"source": str(source)}


# def load_pdfs() -> list[Document]:
#     docs = []
#     try:
#         from langchain_community.document_loaders import PyPDFLoader
#     except ImportError:
#         return docs
#     for path in (PDFs_DIR or Path()).glob("*.pdf"):
#         try:
#             loader = PyPDFLoader(str(path))
#             for page in loader.lazy_load():
#                 page.metadata.update(_metadata(path))
#                 docs.append(page)
#         except Exception as e:
#             print(f"Skip {path}: {e}")
#     return docs


# def load_docx(dir_path: Optional[Path] = None) -> list[Document]:
#     docs = []
#     try:
#         from langchain_community.document_loaders import TextLoader
#     except ImportError:
#         return docs
#     for path in (TEXT_FILES_DIR or Path()).glob("*.txt"):
#         try:
#             loader = TextLoader(str(path), encoding="utf-8", autodetect_encoding=True)
#             for d in loader.lazy_load():
#                 d.metadata.update(_metadata(path))
#                 docs.append(d)
#         except Exception as e:
#             print(f"Skip {path}: {e}")
#     return docs


def load_csvs() -> list[Document]:
    docs = []
    try:
        from langchain_community.document_loaders import CSVLoader
    except ImportError:
        return docs
    for path in (CSVs_DIR or Path()).glob("*.csv"):
        try:
            loader = CSVLoader(str(path), encoding="utf-8")
            for d in loader.lazy_load():
                d.metadata.update(_metadata(path))
                docs.append(d)
        except Exception as e:
            print(f"Skip {path}: {e}")
    return docs


# def load_docx(dir_path: Path | None = None) -> list[Document]:
#     docs = []
#     try:
#         from langchain_community.document_loaders import Docx2txtLoader
#     except ImportError:
#         return docs
#     base = dir_path or TEXT_FILES_DIR or Path()
#     for path in list(base.glob("*.docx")) + list(base.glob("*.doc")):
#         try:
#             loader = Docx2txtLoader(str(path))
#             for d in loader.lazy_load():
#                 d.metadata.update(_metadata(path))
#                 docs.append(d)
#         except Exception as e:
#             print(f"Skip {path}: {e}")
#     return docs


# def load_xlsx_xls() -> list[Document]:
#     docs = []
#     base = XLS_DIR or Path()
#     # XLSX
#     try:
#         import openpyxl
#         import pandas as pd
#     except ImportError:
#         pass
#     else:
#         for path in list(base.glob("*.xlsx")):
#             try:
#                 df = pd.read_excel(path, sheet_name=None, engine="openpyxl")
#                 for sheet, data in df.items():
#                     text = data.to_string() if not data.empty else f"Sheet: {sheet} (empty)"
#                     docs.append(Document(page_content=text, metadata={**_metadata(path), "sheet": sheet}))
#             except Exception as e:
#                 print(f"Skip {path}: {e}")
#     # XLS (xlrd)
#     try:
#         import pandas as pd
#     except ImportError:
#         pass
#     else:
#         for path in list(base.glob("*.xls")):
#             try:
#                 df = pd.read_excel(path, sheet_name=None, engine="xlrd")
#                 for sheet, data in df.items():
#                     text = data.to_string() if not data.empty else f"Sheet: {sheet} (empty)"
#                     docs.append(Document(page_content=text, metadata={**_metadata(path), "sheet": sheet}))
#             except Exception as e:
#                 print(f"Skip {path}: {e}")
#     return docs


# def load_xmls() -> list[Document]:
#     docs = []
#     try:
#         import xml.etree.ElementTree as ET
#     except ImportError:
#         return docs
#     for path in (XMLs_DIR or Path()).glob("*.xml"):
#         try:
#             tree = ET.parse(path)
#             root = tree.getroot()
#             text_parts = []
#             for elem in root.iter():
#                 if elem.text and elem.text.strip():
#                     text_parts.append(elem.text.strip())
#                 if elem.tail and elem.tail.strip():
#                     text_parts.append(elem.tail.strip())
#             text = " ".join(text_parts) or root.tag
#             docs.append(Document(page_content=text, metadata=_metadata(path)))
#         except Exception as e:
#             print(f"Skip {path}: {e}")
#     return docs


def load_jsons() -> list[Document]:
    docs = []
    import json
    for path in (JSONs_DIR or Path()).glob("*.json"):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                for obj in data:
                    text = "\n".join(f"{k}: {v}" for k, v in obj.items())
                    print(f"Loaded JSON doc: {text}")  # <-- Add this line
                    docs.append(Document(page_content=text, metadata=_metadata(path)))
            elif isinstance(data, dict):
                text = "\n".join(f"{k}: {v}" for k, v in data.items())
                print(f"Loaded JSON doc: {text}")  # <-- Add this line
                docs.append(Document(page_content=text, metadata=_metadata(path)))
        except Exception as e:
            print(f"Skip {path}: {e}")
    return docs


def load_all_documents() -> list[Document]:
    """Load and merge documents from all supported formats in the configured folders."""
    all_docs: list[Document] = []
    # all_docs.extend(load_pdfs())
    # all_docs.extend(load_text_files())
    # all_docs.extend(load_docx())
    all_docs.extend(load_csvs())
    # all_docs.extend(load_xlsx_xls())
    # all_docs.extend(load_xmls())
    all_docs.extend(load_jsons())
    return all_docs
