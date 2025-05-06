"""
03_agent.py

This module defines the core agent logic for the Howard Financial RAG pipeline.
It processes natural language queries by first attempting to match known
computational intents (formula-based patterns). If no match is found, it
falls back to semantic vector search using FAISS + SentenceTransformer.

Key functions:
- process_query: Entry point that takes a query, enriched metadata, and vector
  index, returning either a computed answer or a semantic search result.

Dependencies:
- Requires howard_financial.intents (for the intent patterns)
- Requires howard_financial.vector_store (for semantic search fallback)
"""
import re
import pandas as pd
from typing import Dict, Any

from howard_financial.intents import INTENTS
from howard_financial.vector_store import simple_query

# Agent core function
def process_query(
    query: str,
    metadata: pd.DataFrame,
    vector_index,
    model_name: str = "all-MiniLM-L6-v2",
    top_k: int = 5
) -> Dict[str, Any]:
    """
    Processes a user query by:
    1. Checking for matching intents (formula-based)
    2. If no intent match, falling back to vector store semantic search.

    Parameters:
    - query: The user's question (string)
    - metadata: The enriched DataFrame (transactions metadata)
    - vector_index: FAISS index
    - model_name: SentenceTransformer model to use (default: MiniLM)
    - top_k: Number of top matches to return (if fallback search)

    Returns:
    - Dict with:
        - 'type': 'formula' or 'search'
        - 'result': numerical answer or DataFrame of results
        - 'formula': (if formula) human-readable formula string
        - 'follow_up': suggested follow-up or clarifications
    """
    # 1️⃣ First, try to match an intent
    for pattern, intent_fn in INTENTS:
        if pattern.search(query):
            print(f"✅ Matched intent: {pattern.pattern}")
            # Build the intent (answer lambda + formula)
            intent = intent_fn(query)
            answer = intent["answer"](metadata)
            formula = intent.get("formula", "N/A")
            follow_up = (
                f"I used `{formula}`. Need any tweaks—different tags, date range, etc.?"
            )
            return {
                "type": "formula",
                "result": answer,
                "formula": formula,
                "follow_up": follow_up
            }

    # 2️⃣ No intent match: fallback to vector search
    print("ℹ️ No intent match; falling back to vector search...")
    results_df = simple_query(
        query_text=query,
        index=vector_index,
        metadata=metadata,
        model_name=model_name,
        top_k=top_k
    )
    follow_up = "I found these transactions that seem relevant. Would you like to filter or refine?"
    return {
        "type": "search",
        "result": results_df,
        "formula": None,
        "follow_up": follow_up
    }
