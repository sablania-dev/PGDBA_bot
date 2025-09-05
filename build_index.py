# build_index.py
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


context_file = "data/context_document.txt"
index_file = "models/embeddings_index.faiss"


def build_index():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    with open(context_file, "r", encoding="utf-8") as f:
        text = f.read()
    # Split on double newlines (paragraphs)
    chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]

    embeddings = model.encode(chunks)
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, index_file)
    print(f"✅ Index built from {len(chunks)} chunks and saved to {index_file}")

if __name__ == "__main__":
    build_index()
