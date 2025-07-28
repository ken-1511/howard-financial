from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

app = FastAPI(title="Howard Financial API", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load transaction data
def load_transactions():
    """Load transactions from CSV file"""
    csv_path = Path("../data/raw/cleaned_finance_transactions.csv")
    if not csv_path.exists():
        return pd.DataFrame()
    
    df = pd.read_csv(csv_path)
    # Convert date strings to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    # Convert Dollars to numeric, removing $ symbol
    df['Dollars'] = df['Dollars'].str.replace('$', '').str.replace(',', '').astype(float)
    return df

# Global transactions data
transactions_df = load_transactions()

@app.get("/")
async def root():
    """Serve the main dashboard"""
    return FileResponse("../index.html")

@app.get("/api/v1/transactions")
async def get_transactions(
    limit: Optional[int] = None,
    offset: Optional[int] = 0,
    type_filter: Optional[str] = None,
    category_filter: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Get all transactions with optional filtering"""
    global transactions_df
    
    if transactions_df.empty:
        return {"transactions": [], "total": 0}
    
    # Apply filters
    filtered_df = transactions_df.copy()
    
    if type_filter:
        filtered_df = filtered_df[filtered_df['Type'] == type_filter]
    
    if category_filter:
        filtered_df = filtered_df[filtered_df['Category'] == category_filter]
    
    if start_date:
        start_dt = pd.to_datetime(start_date)
        filtered_df = filtered_df[filtered_df['Date'] >= start_dt]
    
    if end_date:
        end_dt = pd.to_datetime(end_date)
        filtered_df = filtered_df[filtered_df['Date'] <= end_dt]
    
    # Apply pagination
    total = len(filtered_df)
    if offset:
        filtered_df = filtered_df.iloc[offset:]
    if limit:
        filtered_df = filtered_df.head(limit)
    
    # Convert to JSON-serializable format
    transactions = []
    for _, row in filtered_df.iterrows():
        transaction = {
            "id": len(transactions) + 1,  # Simple ID generation
            "date": row['Date'].strftime('%Y-%m-%d'),
            "amount": float(row['Dollars']),
            "type": row['Type'],
            "category": row['Category'],
            "vendor": row['Vendor'],
            "account": row['Account'],
            "tags": row.get('Tags', ''),
            "running_balance": float(row.get('USAA S', 0)) if row['Account'] == 'USAA S' else float(row.get('USAA C', 0))
        }
        transactions.append(transaction)
    
    return {
        "transactions": transactions,
        "total": total,
        "limit": limit,
        "offset": offset
    }

@app.get("/api/v1/transactions/{transaction_id}")
async def get_transaction(transaction_id: int):
    """Get a specific transaction by ID"""
    global transactions_df
    
    if transactions_df.empty or transaction_id <= 0 or transaction_id > len(transactions_df):
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    row = transactions_df.iloc[transaction_id - 1]
    transaction = {
        "id": transaction_id,
        "date": row['Date'].strftime('%Y-%m-%d'),
        "amount": float(row['Dollars']),
        "type": row['Type'],
        "category": row['Category'],
        "vendor": row['Vendor'],
        "account": row['Account'],
        "tags": row.get('Tags', ''),
        "running_balance": float(row.get('USAA S', 0)) if row['Account'] == 'USAA S' else float(row.get('USAA C', 0))
    }
    
    return transaction

@app.get("/api/v1/summary")
async def get_summary():
    """Get financial summary statistics"""
    global transactions_df
    
    if transactions_df.empty:
        return {
            "total_income": 0,
            "total_expenses": 0,
            "net_income": 0,
            "current_balance": 0,
            "transaction_count": 0,
            "categories": {},
            "monthly_trends": []
        }
    
    # Calculate basic stats
    income = transactions_df[transactions_df['Dollars'] > 0]['Dollars'].sum()
    expenses = abs(transactions_df[transactions_df['Dollars'] < 0]['Dollars'].sum())
    net_income = income - expenses
    
    # Get current balance (last transaction)
    current_balance = transactions_df.iloc[-1].get('USAA S', 0) + transactions_df.iloc[-1].get('USAA C', 0)
    
    # Category breakdown
    category_totals = transactions_df.groupby('Category')['Dollars'].sum().to_dict()
    
    # Monthly trends (last 6 months)
    transactions_df['Month'] = transactions_df['Date'].dt.to_period('M')
    monthly_trends = transactions_df.groupby('Month')['Dollars'].sum().tail(6).to_dict()
    monthly_trends = [{"month": str(k), "amount": float(v)} for k, v in monthly_trends.items()]
    
    return {
        "total_income": float(income),
        "total_expenses": float(expenses),
        "net_income": float(net_income),
        "current_balance": float(current_balance),
        "transaction_count": len(transactions_df),
        "categories": {k: float(v) for k, v in category_totals.items()},
        "monthly_trends": monthly_trends
    }

@app.get("/api/v1/categories")
async def get_categories():
    """Get all unique categories"""
    global transactions_df
    
    if transactions_df.empty:
        return {"categories": []}
    
    categories = transactions_df['Category'].unique().tolist()
    return {"categories": categories}

@app.get("/api/v1/types")
async def get_types():
    """Get all unique transaction types"""
    global transactions_df
    
    if transactions_df.empty:
        return {"types": []}
    
    types = transactions_df['Type'].unique().tolist()
    return {"types": types}

@app.get("/api/v1/accounts")
async def get_accounts():
    """Get all unique accounts"""
    global transactions_df
    
    if transactions_df.empty:
        return {"accounts": []}
    
    accounts = transactions_df['Account'].unique().tolist()
    return {"accounts": accounts}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 