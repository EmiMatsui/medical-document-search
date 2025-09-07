from .search_core import build_faiss_index

if __name__ == "__main__":
    n = build_faiss_index()
    print(f"Indexed {n} documents.")
