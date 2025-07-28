import pandas as pd

# Prepares a human-readable, natural language description of each transaction.
# This improves downstream embedding and retrieval by summarizing key fields in a sentence-like format.
def format_transaction(row: pd.Series) -> str:
    """
    Generates a natural language description of a single transaction row.

    Components:
    - Includes the date, account, amount, vendor, category, and tags (if available).
    - The output format varies based on transaction type (e.g., expense, income, transfer).

    Parameters:
    - row: A single transaction (Series).

    Returns:
    - A string describing the transaction in a consistent, readable format.
    """
    date = row["Date"].date()
    account = row["Account"]
    amount = abs(row["Amount"])
    vendor = row["Vendor"]
    category = row["Category"]

    # Only include tags if they are non-empty
    tags = f"(tags: {row['Tags']})" if pd.notna(row["Tags"]) and row["Tags"].strip() else ""

    type_lower = row["Type"].lower()

    # Different sentence templates depending on transaction type
    if type_lower == "expense":
        return f"On {date}, you spent ${amount:.2f} at {vendor} (Category: {category}) using {account}. {tags}"
    elif type_lower == "income":
        return f"On {date}, you received an income of ${amount:.2f} from {vendor} (Category: {category}) into {account}. {tags}"
    elif type_lower == "transfer":
        return f"On {date}, ${amount:.2f} was transferred involving {vendor} (Category: {category}) from {account}. {tags}"
    elif type_lower == "withdrawal":
        return f"On {date}, you withdrew ${amount:.2f} from {account} (Vendor: {vendor}, Category: {category}). {tags}"
    elif type_lower == "reimbursement":
        return f"On {date}, you were reimbursed ${amount:.2f} by {vendor} (Category: {category}) into {account}. {tags}"
    else:
        # Catch-all fallback for unexpected types
        return f"On {date}, a transaction of ${amount:.2f} occurred at {vendor} (Type: {row['Type']}, Category: {category}) using {account}. {tags}"


# Adds metadata and natural language descriptions to the entire DataFrame.
def enrich_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enhances the DataFrame with additional metadata and a 'text' column.

    Adds:
    - 'text': A natural language description of the transaction (using format_transaction()).
    - 'weekday': Day of the week for each transaction.
    - 'is_weekend': Boolean indicating whether the transaction occurred on a weekend.
    - 'is_fixed': Boolean indicating if the transaction is a fixed recurring cost (e.g., rent, subscription).

    Parameters:
    - df: The cleaned transaction DataFrame.

    Returns:
    - The enriched DataFrame with new columns ready for embedding and analysis.
    """
    df = df.copy()

    # Create the 'text' column first for embeddings
    df.insert(0, "text", df.apply(format_transaction, axis=1))

    # Add weekday (e.g., Monday, Tuesday)
    df["weekday"] = df["Date"].dt.day_name()

    # Add is_weekend (True if Saturday or Sunday)
    df["is_weekend"] = df["weekday"].isin(["Saturday", "Sunday"])

    # Define what counts as a "fixed" recurring expense
    fixed = {"rent", "subscription", "insurance", "loan payment"}

    # Add is_fixed (True if the Category is one of the fixed types)
    df["is_fixed"] = df["Category"].isin(fixed)

    return df
