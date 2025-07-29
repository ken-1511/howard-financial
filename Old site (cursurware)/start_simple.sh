#!/bin/bash

echo "🚀 Starting Howard Financial - Simple Mode"
echo "📊 This is a lightweight setup for frontend testing"
echo ""

# Check if CSV file exists
if [ ! -f "data/raw/cleaned_finance_transactions.csv" ]; then
    echo "❌ Error: CSV file not found at data/raw/cleaned_finance_transactions.csv"
    echo "Please make sure your data file is in the correct location"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install pandas if not already installed in venv
pip show pandas > /dev/null 2>&1 || pip install pandas==2.1.3

echo ""
echo "🌐 Starting server..."
echo "📱 Frontend will be available at: http://localhost:8000/index.html"
echo "🔧 API endpoints:"
echo "   - http://localhost:8000/api/v1/transactions"
echo "   - http://localhost:8000/api/v1/summary"
echo ""
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

python simple_server.py 