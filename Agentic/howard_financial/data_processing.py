import pandas as pd

# Loads and cleans a personal finance CSV for analysis.
# This ensures the data is structured, cleaned, and normalized for downstream workflows.
def load_and_clean(path: str) -> pd.DataFrame:
    """
    Phase 1 – Load the raw export and return a tidy DataFrame.
    
    Steps:
    - Reads in the CSV file.
    - Ensures 'Date' is a proper datetime (malformed dates become NaT).
    - Converts the 'Dollars' column to signed floats (handles negatives via parentheses)
      BUT only applies negative signs to specific types (expense, withdrawal).
    - Normalizes key text columns (e.g., lowercasing, stripping spaces) for consistency.
    """
    # ── 1. Load (Ingest) the Raw Data --------------------------------------------
    # "Ingest" means reading raw data from the file system into a DataFrame.
    # We use header=0 (first row is header) and engine="python" for flexible parsing.
    raw = pd.read_csv(path, header=0, engine="python")

    # ── 2. Normalize Column Headers ----------------------------------------------
    # Standardize header names: remove extra spaces and unify spacing within names.
    # For example: "  Vendor Name  " → "Vendor Name"
    raw.columns = (raw.columns
                     .str.strip()
                     .str.replace(r"\s+", " ", regex=True))  # collapse multiple spaces

    # ── 3. Validate and Parse 'Date' Column --------------------------------------
    # Ensure the 'Date' column exists and convert it to datetime format.
    # Invalid dates (e.g., typos) will be converted to NaT (Not a Time) using errors="coerce".
    if "Date" not in raw.columns:
        raise ValueError(f"Expected 'Date' column, got {list(raw.columns)}")
    raw["Date"] = pd.to_datetime(
        raw["Date"],
        format="%m/%d/%Y",
        errors="coerce"  # prevents failure on bad dates; replaces them with NaT
    )

    # ── 4. Convert 'Dollars' to Numeric Amounts ----------------------------------
    # Remove $ signs, commas, and parentheses, then convert to float.
    # Parentheses are used in finance to indicate negatives (e.g., ($500) → -500),
    # BUT we apply negative signs **only for specific transaction types.**
    tx = raw.copy()
    tx["Amount"] = (tx["Dollars"].astype(str)
                                .str.replace(r"[,$]", "", regex=True)   # remove $ and commas
                                .str.replace(r"[()]", "", regex=True)   # remove parentheses
                                .astype(float))

    # Apply NEGATIVE only for 'expense' and 'withdrawal' types
    neg_types = ["expense", "withdrawal"]
    neg_mask = tx["Type"].str.lower().isin(neg_types)
    tx.loc[neg_mask, "Amount"] *= -1

    # ── 5. Clean Up String Columns -----------------------------------------------
    # Standardize text fields for consistency: strip leading/trailing spaces and lowercase.
    # Applies to: Account, Type, Category, Vendor, Tags.
    for col in ["Account", "Type", "Category", "Vendor", "Tags"]:
        if col in tx.columns:
            tx[col] = tx[col].fillna("").str.strip().str.lower()

    # ── 6. Sanity Check: Log unique transaction types ----------------------------
    print("✅ Sanity Check – Unique 'Type' values found:", tx["Type"].unique())

    return tx
