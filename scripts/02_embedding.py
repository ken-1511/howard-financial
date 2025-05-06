"""
02_embedding.py

Builds vector embeddings from the cleaned transaction data,
saves the FAISS index and metadata for retrieval, and runs a basic query test.
"""

from pathlib import Path
from howard_financial.vector_store import (
    build_and_save_vector_store,
    load_existing_vector_store,
    simple_query
)

def main():
    # ──────────────────────────────────────────────────────────────
    # Config
    # ──────────────────────────────────────────────────────────────
    PROCESSED_FILE = Path("data/processed/embedding_ready_transactions.csv")
    VECTOR_STORE_FILE = Path("data/processed/vector_store.faiss")
    METADATA_FILE = Path("data/processed/metadata.pkl")
    MODEL_NAME = "all-MiniLM-L6-v2"

    # ──────────────────────────────────────────────────────────────
    # Step 1: Build and Save Vector Store
    # ──────────────────────────────────────────────────────────────
    build_and_save_vector_store(
        processed_csv=PROCESSED_FILE,
        vector_store_file=VECTOR_STORE_FILE,
        metadata_file=METADATA_FILE,
        text_col="text",
        model_name=MODEL_NAME
    )

    # ──────────────────────────────────────────────────────────────
    # Step 2: Load Vector Store for Validation
    # ──────────────────────────────────────────────────────────────
    index, metadata = load_existing_vector_store(
        vector_store_file=VECTOR_STORE_FILE,
        metadata_file=METADATA_FILE
    )

    print(f"✅ FAISS index loaded with {index.ntotal} vectors.")
    print("🔎 Sample metadata (first 5 rows):")
    print(metadata.head())

    # ──────────────────────────────────────────────────────────────
    # Step 3: Run Test Query
    # ──────────────────────────────────────────────────────────────
    query_text = "how much did I spend on food at blenders?"
    results = simple_query(
        query_text=query_text,
        index=index,
        metadata=metadata,
        model_name=MODEL_NAME,
        top_k=5
    )
    print(f"\n🔎 Test query: '{query_text}'\n")
    print(results)

if __name__ == "__main__":
    main()
