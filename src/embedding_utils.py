# src/embedding_utils.py


import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from pathlib import Path
from typing import List, Tuple

def compute_embeddings(
    df: pd.DataFrame,
    text_col: str = "text",
    model_name: str = "all-MiniLM-L6-v2"
) -> List[List[float]]:
    """
    Generate embeddings for the specified text column using SentenceTransformer.
    """
    model = SentenceTransformer(model_name)
    print(f"Embedding {len(df)} records with model '{model_name}'...")
    embeddings = model.encode(df[text_col].tolist(), show_progress_bar=True)
    return embeddings


def save_vector_store(
    embeddings: List[List[float]],
    df_metadata: pd.DataFrame,
    vector_store_file: Path,
    metadata_file: Path
):
    """
    Save embeddings to a FAISS index and metadata (like DataFrame rows) to a pickle.
    """
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    
    faiss.write_index(index, str(vector_store_file))
    print(f"✅ Saved FAISS index to {vector_store_file}")

    with open(metadata_file, "wb") as f:
        pickle.dump(df_metadata, f)
    print(f"✅ Saved metadata to {metadata_file}")


def load_vector_store(
    vector_store_file: Path,
    metadata_file: Path
) -> Tuple[faiss.IndexFlatL2, pd.DataFrame]:
    """
    Load the FAISS index and the metadata DataFrame.
    """
    index = faiss.read_index(str(vector_store_file))
    with open(metadata_file, "rb") as f:
        metadata = pickle.load(f)
    print(f"✅ Loaded FAISS index and metadata.")
    return index, metadata


def query_vector_store(
    query_text: str,
    index: faiss.IndexFlatL2,
    metadata: pd.DataFrame,
    model_name: str = "all-MiniLM-L6-v2",
    top_k: int = 5
) -> pd.DataFrame:
    """
    Query the vector store with a new question and return top_k matches.
    """
    model = SentenceTransformer(model_name)
    query_vec = model.encode([query_text])
    D, I = index.search(query_vec, top_k)

    results = metadata.iloc[I[0]].copy()
    results["similarity_score"] = 1 - (D[0] / 2)  # optional: convert distance to similarity
    return results.reset_index(drop=True)
