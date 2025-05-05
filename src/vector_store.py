import pandas as pd
from pathlib import Path
from embedding_utils import (
    compute_embeddings,
    save_vector_store,
    load_vector_store,
    query_vector_store
)

def build_and_save_vector_store(
    processed_csv: Path,
    vector_store_file: Path,
    metadata_file: Path,
    text_col: str = "text",
    model_name: str = "all-MiniLM-L6-v2"
):
    """
    Build a vector store from the processed CSV and save the index + metadata.

    Parameters:
    - processed_csv: Path to the processed CSV file (e.g., embedding_ready_transactions.csv).
    - vector_store_file: Where to save the FAISS index.
    - metadata_file: Where to save the metadata pickle.
    - text_col: Column in CSV to embed (default: 'text').
    - model_name: SentenceTransformer model to use.
    """
    print(f"🔄 Loading processed data from {processed_csv}...")
    df = pd.read_csv(processed_csv)

    embeddings = compute_embeddings(df, text_col=text_col, model_name=model_name)

    # Save vector store + metadata
    save_vector_store(embeddings, df, vector_store_file, metadata_file)
    print("✅ Vector store built and saved successfully.")


def load_existing_vector_store(
    vector_store_file: Path,
    metadata_file: Path
):
    """
    Load an existing vector store (FAISS index + metadata).

    Parameters:
    - vector_store_file: Path to the FAISS index.
    - metadata_file: Path to the metadata pickle.

    Returns:
    - (FAISS index, metadata DataFrame)
    """
    return load_vector_store(vector_store_file, metadata_file)


def simple_query(
    query_text: str,
    index,
    metadata,
    model_name: str = "all-MiniLM-L6-v2",
    top_k: int = 5
) -> pd.DataFrame:
    """
    Convenience wrapper for querying the vector store.

    Parameters:
    - query_text: The text to query.
    - index: The FAISS index object.
    - metadata: The metadata DataFrame.
    - model_name: Model to use for encoding the query.
    - top_k: Number of top results to return.

    Returns:
    - A DataFrame of top_k results.
    """
    return query_vector_store(query_text, index, metadata, model_name=model_name, top_k=top_k)
