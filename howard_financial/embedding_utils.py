import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from pathlib import Path
from typing import List, Tuple

"""
vector_store.py

Handles the creation, saving, loading, and querying of a FAISS-based vector store
for fast semantic search over financial transaction data embeddings.

Main functions:
- compute_embeddings
- save_vector_store
- load_vector_store
- query_vector_store
"""

def compute_embeddings(
    df: pd.DataFrame,
    text_col: str = "text",
    model_name: str = "all-MiniLM-L6-v2"
) -> List[List[float]]:
    """
    Generate embeddings for a DataFrame text column using a SentenceTransformer model.

    Parameters:
    - df: DataFrame containing the text to embed.
    - text_col: Name of the column in df to embed (default: 'text').
    - model_name: The SentenceTransformer model to use for embedding.

    Returns:
    - A list of embedding vectors (one per row).
    """
    model = SentenceTransformer(model_name)
    print(f"🔄 Embedding {len(df)} records using model '{model_name}'...")
    embeddings = model.encode(df[text_col].tolist(), show_progress_bar=True)
    return embeddings


def save_vector_store(
    embeddings: List[List[float]],
    df_metadata: pd.DataFrame,
    vector_store_file: Path,
    metadata_file: Path
):
    """
    Save embeddings and associated metadata to disk.

    - Saves the FAISS index to a binary file.
    - Saves the metadata (DataFrame) as a pickle for retrieval.

    Parameters:
    - embeddings: List of embedding vectors (must match df_metadata row count).
    - df_metadata: DataFrame containing metadata linked to the embeddings.
    - vector_store_file: Path to save the FAISS index.
    - metadata_file: Path to save the metadata pickle.
    """
    # Validate consistency
    assert len(embeddings) == len(df_metadata), (
        f"Embedding count ({len(embeddings)}) does not match metadata rows ({len(df_metadata)})."
    )

    dim = len(embeddings[0])  # Embedding dimensionality
    index = faiss.IndexFlatL2(dim)  # Flat L2 (Euclidean) index
    index.add(embeddings)

    # Ensure directories exist
    vector_store_file.parent.mkdir(parents=True, exist_ok=True)
    metadata_file.parent.mkdir(parents=True, exist_ok=True)

    # Save index
    faiss.write_index(index, str(vector_store_file))
    print(f"✅ Saved FAISS index to {vector_store_file.resolve()}")

    # Save metadata
    with open(metadata_file, "wb") as f:
        pickle.dump(df_metadata, f)
    print(f"✅ Saved metadata to {metadata_file.resolve()}")


def load_vector_store(
    vector_store_file: Path,
    metadata_file: Path
) -> Tuple[faiss.IndexFlatL2, pd.DataFrame]:
    """
    Load the FAISS index and metadata DataFrame from disk.

    Parameters:
    - vector_store_file: Path to the saved FAISS index file.
    - metadata_file: Path to the pickled metadata file.

    Returns:
    - (FAISS index object, metadata DataFrame)
    """
    index = faiss.read_index(str(vector_store_file))
    with open(metadata_file, "rb") as f:
        metadata = pickle.load(f)

    # Validate consistency
    assert index.ntotal == len(metadata), (
        f"FAISS index contains {index.ntotal} vectors but metadata has {len(metadata)} rows."
    )

    print(f"✅ Loaded FAISS index and metadata successfully.")
    return index, metadata


def query_vector_store(
    query_text: str,
    index: faiss.IndexFlatL2,
    metadata: pd.DataFrame,
    model_name: str = "all-MiniLM-L6-v2",
    top_k: int = 5,
    model: SentenceTransformer = None
) -> pd.DataFrame:
    """
    Query the vector store with a text prompt and return the top_k most similar results.

    Parameters:
    - query_text: The text query to embed and search for.
    - index: The FAISS index to search.
    - metadata: DataFrame containing metadata for the indexed vectors.
    - model_name: The SentenceTransformer model to use (if model not provided).
    - top_k: Number of top results to return.
    - model: Optional pre-loaded SentenceTransformer instance (to reuse models efficiently).

    Returns:
    - A DataFrame of the top_k results, including a 'similarity_score' column.
    """
    if index.ntotal == 0:
        raise ValueError("❌ The FAISS index is empty. Please build the vector store before querying.")

    top_k = min(top_k, index.ntotal)

    # Use provided model or load fresh
    if model is None:
        model = SentenceTransformer(model_name)

    # Encode the query and search
    query_vec = model.encode([query_text])
    D, I = index.search(query_vec, top_k)

    results = metadata.iloc[I[0]].copy()
    results = results.reset_index(drop=True)
    results["similarity_score"] = 1 - (D[0] / 2)  # Optionally convert L2 distance to similarity
    return results
