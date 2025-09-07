from pathlib import Path
import os

# ルートからの相対パス
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data-source"
FAISS_DIR = DATA_DIR / "faiss"
FAISS_DIR.mkdir(parents=True, exist_ok=True)

# インデックス保存先
FAISS_INDEX_PATH = FAISS_DIR / "faiss.index"
FAISS_META_PATH = FAISS_DIR / "faiss_meta.pkl"

# アップロード保存先（ここでは data-source に保存）
UPLOAD_DIR = DATA_DIR
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# LLM設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = "gpt-3.5-turbo"       # プロトタイプ用に安いモデル
EMB_MODEL = "intfloat/multilingual-e5-small"
