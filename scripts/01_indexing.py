"""
01_indexing.py

Loads raw bank statement data, cleans it, enriches it with metadata, and writes
the output as a processed CSV. This is Step 1 of the RAG pipeline.
"""

import pandas as pd
from pathlib import Path
from howard_financial.data_processing import load_and_clean
from howard_financial.text_formatting import enrich_metadata

def main():
    # ──────────────────────────────────────────────────────────────
    # Config
    # ──────────────────────────────────────────────────────────────
    RAW_FILE = Path("data/raw/personal_finance_log.csv")
    PROCESSED_FILE = Path("data/processed/embedding_ready_transactions.csv")

    # ──────────────────────────────────────────────────────────────
    # Step 1: Load and Clean
    # ──────────────────────────────────────────────────────────────
    print(f"🔄 Loading and cleaning raw data from {RAW_FILE}...")
    tx = load_and_clean(RAW_FILE)

    # ──────────────────────────────────────────────────────────────
    # Step 2: Enrich Metadata
    # ──────────────────────────────────────────────────────────────
    print("✨ Enriching metadata (adding text + flags)...")
    enriched_tx = enrich_metadata(tx)

    # ──────────────────────────────────────────────────────────────
    # Step 3: Save Processed Data
    # ──────────────────────────────────────────────────────────────
    print(f"💾 Saving enriched data to {PROCESSED_FILE}...")
    enriched_tx.to_csv(PROCESSED_FILE, index=False)

    print("✅ Indexing complete!")

if __name__ == "__main__":
    main()
