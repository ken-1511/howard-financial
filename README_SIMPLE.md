# Howard Financial - Simple Mode

A lightweight setup for frontend testing and design without Docker or complex databases.

## 🚀 Quick Start

1. **Make sure your CSV data is in place:**
   ```
   data/raw/cleaned_finance_transactions.csv
   ```

2. **Start the server:**
   ```bash
   ./start_simple.sh
   ```

3. **Open your browser:**
   ```
   http://localhost:8000/index.html
   ```

## 📁 What's Included

- **`simple_server.py`** - Minimal Python HTTP server
- **`start_simple.sh`** - Startup script
- **`requirements_simple.txt`** - Only pandas dependency
- **`index.html`** - Your existing frontend

## 🔧 API Endpoints

- `GET /api/v1/transactions` - Get all transactions
- `GET /api/v1/summary` - Get financial summary

## 🛠️ Manual Setup (if needed)

If the startup script doesn't work:

```bash
# Install pandas
pip3 install pandas==2.1.3

# Start server manually
python3 simple_server.py
```

## 📊 Data Format

The server expects your CSV to have these columns:
- `Date` - Transaction date
- `Dollars` - Amount (with $ and commas)
- `Type` - Transaction type
- `Category` - Transaction category
- `Vendor` - Vendor name
- `Account` - Account name

## 🎯 Perfect For

- Frontend testing and design
- Quick prototyping
- Local development
- No database complexity

## ⏹️ Stop Server

Press `Ctrl+C` in the terminal where the server is running.

---

**That's it!** Simple, lightweight, and ready for frontend development. 