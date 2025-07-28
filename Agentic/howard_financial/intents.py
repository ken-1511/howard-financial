# src/intents.py

"""
This module defines the INTENTS list, which maps natural language patterns (regex)
to specific computational logic using the DSL (amt, pct).
"""

import re
from howard_financial.dsl import amt, pct

# List of (pattern, intent_handler) tuples
INTENTS = [
    # Match questions about spending on eating out or fast food
    (
        re.compile(r"\bhow (?:much|many).*?(?:eat|eating out|fast food)\b", re.I),
        lambda q: {
            "answer": lambda df: amt(tag="eating out")(df).sum(),
            "formula": "Σ Amount where Tags~='eating out'"
        }
    ),

    # Match questions about what portion of income went to food
    (
        re.compile(r"\bportion\b.*\bincome\b.*\bfood\b", re.I),
        lambda q: {
            "answer": lambda df: pct(
                amt(cat='food'),
                amt(cat='income')
            )(df),
            "formula": "Σ Amount(food) / |Σ Amount(income)|"
        }
    ),
]
