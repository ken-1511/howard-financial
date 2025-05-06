"""
01_03_pipeline_test.py

Full pipeline test:
- Step 1: Load and clean raw data.
- Step 2: Enrich metadata and save processed CSV.
- Step 3: Build vector store (FAISS index + metadata).
- Step 4: Run an agent query to verify the pipeline.

This ensures everything works from raw → processed → embeddings → agent in one run.
"""

import pandas as pd
from pathlib import Path

from howard_financial.data_processing import load_and_clean
from howard_financial.text_formatting import enrich_metadata
from howard_financial.vector_store import (
    build_and_save_vector_store,
    load_existing_vector_store
)
from howard_financial.agent import process_query

# -------------------- Paths --------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_FILE = ROOT_DIR / "data" / "raw" / "personal_finance_log.csv"
PROCESSED_CSV = ROOT_DIR / "data" / "processed" / "embedding_ready_transactions.csv"
VECTOR_STORE_FILE = ROOT_DIR / "data" / "processed" / "vector_store.faiss"
METADATA_FILE = ROOT_DIR / "data" / "processed" / "metadata.pkl"

# -------------------- Step 1: Load + Clean --------------------
print("🔄 Step 1: Loading and cleaning raw data...")
df_clean = load_and_clean(RAW_FILE)

# -------------------- Step 2: Enrich + Save --------------------
print("✨ Step 2: Enriching metadata...")
df_enriched = enrich_metadata(df_clean)

# Ensure processed directory exists
PROCESSED_CSV.parent.mkdir(parents=True, exist_ok=True)

# Save processed CSV
df_enriched.to_csv(PROCESSED_CSV, index=False)
print(f"✅ Processed CSV saved to: {PROCESSED_CSV.resolve()}")

# -------------------- Step 3: Build Vector Store --------------------
print("\n🔧 Step 3: Building vector store...")
build_and_save_vector_store(
    processed_csv=PROCESSED_CSV,
    vector_store_file=VECTOR_STORE_FILE,
    metadata_file=METADATA_FILE,
    text_col="text",
    model_name="all-MiniLM-L6-v2"
)

# -------------------- Step 4: Agent Test --------------------
print("\n🤖 Step 4: Running agent test...")

# Load vector store
index, metadata = load_existing_vector_store(
    vector_store_file=VECTOR_STORE_FILE,
    metadata_file=METADATA_FILE
)

# Example query to test (portion of income spent on food)
query_text = "What portion of my income went to food?"
print(f"\n🔎 Query: {query_text}")

# Run agent
result = process_query(
    query=query_text,
    metadata=metadata,
    vector_index=index
)

# Print results
if result["type"] == "formula":
    print(f"✅ Matched formula:\n- Formula: {result['formula']}\n- Result: {result['result']}")
else:
    print("🔍 Top vector search results:")
    print(result["result"])

print("\n💬 Follow-up suggestion:", result["follow_up"])
