import pandas as pd
# Clean and prepare a natural language column with
# Smarter, type-aware transaction descriptions
def format_transaction(row):
    date = row["Date"].date()
    account = row["Account"]
    amount = abs(row["Amount"])
    vendor = row["Vendor"]
    category = row["Category"]
    tags = f"(tags: {row['Tags']})" if pd.notna(row["Tags"]) and row["Tags"].strip() else ""

    type_lower = row["Type"].lower()
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
        return f"On {date}, a transaction of ${amount:.2f} occurred at {vendor} (Type: {row['Type']}, Category: {category}) using {account}. {tags}"

def enrich_metadata(df):
    df["Amount"] = df["Amount"].replace('[\$,()]', '', regex=True).astype(float) * -1
    df["weekday"]     = df["Date"].dt.day_name()
    df["is_weekend"]  = df["weekday"].isin(["Saturday", "Sunday"])
    fixed = {"rent", "subscription", "insurance", "loan payment"}
    df["is_fixed"]    = df["Category"].isin(fixed)
    # Generate 'text' column
    df.insert(0, "text", df.apply(format_transaction, axis=1))

    # Save for embedding and future use
    df.to_csv("data/processed/embedding_ready_transactions.csv", index=False)