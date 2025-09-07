import os
import glob
import pickle
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer
from .config import DATA_DIR, FAISS_INDEX_PATH, FAISS_META_PATH, EMB_MODEL

# モデルはプロセスで1つ（API起動時にロード）
_model = SentenceTransformer(EMB_MODEL)

def load_text_chunks(pattern: str = "*.txt"):
    chunks = []
    for path in glob.glob(str(DATA_DIR / pattern)):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read().strip()
        if text:
            chunks.append({"file_path": path, "text": text})
    return chunks

def build_faiss_index():
    chunks = load_text_chunks()
    if not chunks:
        raise RuntimeError("No .txt files found under data-source/")
    vecs = _model.encode([c["text"] for c in chunks], normalize_embeddings=True).astype("float32")
    index = faiss.IndexFlatL2(vecs.shape[1])
    index.add(vecs)

    FAISS_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(FAISS_INDEX_PATH))
    with open(FAISS_META_PATH, "wb") as f:
        pickle.dump(chunks, f)
    return len(chunks)

def load_index_and_meta():
    if not FAISS_INDEX_PATH.exists() or not FAISS_META_PATH.exists():
        raise RuntimeError("FAISS index/meta not found. Run build_index.py first.")
    index = faiss.read_index(str(FAISS_INDEX_PATH))
    with open(FAISS_META_PATH, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def encode_query(q: str):
    return _model.encode([q], normalize_embeddings=True).astype("float32")
