import os
from pathlib import Path
from typing import List
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.config import UPLOAD_DIR
from app.db import Base, engine, get_db
from app.models import FileRecord
from app.llm import rewrite_query_for_search, summarize_text
from app.search_core import load_index_and_meta, encode_query


# DBテーブル作成
Base.metadata.create_all(engine)

# アプリ＆CORS
app = FastAPI(title="Medical Doc Search API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# インデックス（起動時に読み込み）
try:
    index, chunks = load_index_and_meta()
except Exception as e:
    index, chunks = None, []
    print(f"[WARN] index not loaded: {e}")

@app.get("/ping")
def ping():
    return {"ok": True, "indexed": len(chunks)}

class SearchRequest(BaseModel):
    question: str
    k: int = 4

@app.post("/search")
def search_case(request: SearchRequest):
    if index is None or not chunks:
        raise HTTPException(status_code=503, detail="Index not ready. Run build_index first.")
    refined = rewrite_query_for_search(request.question)
    qvec = encode_query(refined)
    D, I = index.search(qvec, k=request.k)

    out = []
    for i, d in zip(I[0], D[0]):
        if 0 <= i < len(chunks):
            summary = summarize_text(chunks[i]["text"])
            out.append({
                "ファイル名": Path(chunks[i]["file_path"]).name,
                "要約": summary,
                "距離": round(float(d), 4),
            })

    return JSONResponse({"refined_query": refined, "results": out})

# ===== アップロード（任意） =====
@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...), db=Depends(get_db)):
    results = []
    for f in files:
        safe_name = f.filename.replace("/", "_")
        dest = UPLOAD_DIR / safe_name
        content = await f.read()
        with open(dest, "wb") as out:
            out.write(content)

        rec = FileRecord(
            original_name=f.filename,
            saved_path=str(dest),
            mime_type=f.content_type,
            size_bytes=len(content),
        )
        db.add(rec); db.commit(); db.refresh(rec)
        results.append({
            "id": rec.id, "original_name": rec.original_name,
            "mime_type": rec.mime_type, "size_bytes": rec.size_bytes,
            "saved_path": rec.saved_path,
        })
    return {"uploaded": results}

@app.get("/files")
def list_files(db=Depends(get_db)):
    rows = db.query(FileRecord).order_by(FileRecord.id.desc()).limit(100).all()
    return [{
        "id": r.id, "original_name": r.original_name, "mime_type": r.mime_type,
        "size_bytes": r.size_bytes, "uploaded_at": (r.uploaded_at.isoformat() if r.uploaded_at else None),
    } for r in rows]