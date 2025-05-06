"""
03_agent.py

Tests the RAG agent logic by processing a natural language query
against the enriched transaction data and vector store.
"""

from pathlib import Path
from howard_financial.agent import process_query
from howard_financial.vector_store import load_existing_vector_store

def main():
    # ──────────────────────────────────────────────────────────────
    # Config
    # ──────────────────────────────────────────────────────────────
    VECTOR_STORE_FILE = Path("data/processed/vector_store.faiss")
    METADATA_FILE = Path("data/processed/metadata.pkl")

    # ──────────────────────────────────────────────────────────────
    # Step 1: Load Vector Store + Metadata
    # ──────────────────────────────────────────────────────────────
    index, metadata = load_existing_vector_store(
        vector_store_file=VECTOR_STORE_FILE,
        metadata_file=METADATA_FILE
    )
    print(f"✅ FAISS index loaded with {index.ntotal} vectors.")

    # ──────────────────────────────────────────────────────────────
    # Step 2: Process Agent Query
    # ──────────────────────────────────────────────────────────────
    query = "What portion of my income went to food?"

    result = process_query(query, metadata, index)

    # ──────────────────────────────────────────────────────────────
    # Step 3: Display Result
    # ──────────────────────────────────────────────────────────────
    print(f"\n🔎 Query: {query}")
    print(f"✅ Matched intent: {result['matched_intent']}")
    print(f"🔢 Answer: {result['answer']}")
    print(f"🧮 Formula: {result['formula']}")
    print(f"💬 Follow-up: {result['follow_up']}")

if __name__ == "__main__":
    main()
