import pandas as pd
# retrieves .csv at a specified location and ensures that small features of the data entry
# are accounted for in the structure presented to the agentic workflow
def load_and_clean(path: str) -> pd.DataFrame:
    """
    Phase 1 – Read the raw export and return a tidy DataFrame.
    • Ensures 'Date' is datetime.
    • Converts the money column to signed floats (parentheses → negative).
    • Trims / lower-cases the text columns.
    """
    # ── 1. ingest ----------------------------------------------------------------
    raw = pd.read_csv(path, header=0, engine="python")      # tweak header/skiprows if needed

    # ── 2. normalize header names ------------------------------------------------
    raw.columns = (raw.columns
                     .str.strip()
                     .str.replace(r"\s+", " ", regex=True))   # collapse doubled spaces

    # ── 3. make sure 'Date' exists and convert -----------------------------------
    if "Date" not in raw.columns:
        raise ValueError(f"Expected 'Date' column, got {list(raw.columns)}")
    raw["Date"] = pd.to_datetime(raw["Date"], format="%m/%d/%Y")

    # ── 4. dollars → float (handle parens as negatives) --------------------------
    tx = raw.copy()
    tx["Amount"] = (tx["Dollars"].astype(str)
                                .str.replace(r"[,$]", "", regex=True)   # strip $ and commas
                                .str.replace(r"[()]", "", regex=True)   # drop parens
                                .astype(float))
    neg_mask = raw["Dollars"].astype(str).str.contains(r"\(")
    tx.loc[neg_mask, "Amount"] *= -1

    # ── 5. tidy the string columns ----------------------------------------------
    for col in ["Account", "Type", "Category", "Vendor", "Tags"]:
        if col in tx.columns:
            tx[col] = tx[col].fillna("").str.strip().str.lower()
            
    return tx
