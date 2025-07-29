#!/usr/bin/env python3
import http.server
import socketserver
import json
import pandas as pd
import urllib.parse
import os

PORT = 8000
CSV_PATH = "data/raw/cleaned_finance_transactions.csv"

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/'):
            self.handle_api()
        else:
            super().do_GET()
    
    def handle_api(self):
        try:
            df = pd.read_csv(CSV_PATH)
            df['Date'] = pd.to_datetime(df['Date'])
            df['Dollars'] = df['Dollars'].str.replace('$', '').str.replace(',', '').astype(float)
            
            if self.path == '/api/v1/transactions':
                transactions = []
                for idx, row in df.iterrows():
                    transactions.append({
                        "id": idx + 1,
                        "date": row['Date'].strftime('%Y-%m-%d'),
                        "amount": float(row['Dollars']),
                        "type": row['Type'],
                        "category": row['Category'],
                        "vendor": row['Vendor'],
                        "account": row['Account']
                    })
                data = {"transactions": transactions, "total": len(df)}
            
            elif self.path == '/api/v1/summary':
                total_income = df[df['Dollars'] > 0]['Dollars'].sum()
                total_expenses = abs(df[df['Dollars'] < 0]['Dollars'].sum())
                data = {
                    "total_income": float(total_income),
                    "total_expenses": float(total_expenses),
                    "net_income": float(df['Dollars'].sum()),
                    "transaction_count": len(df)
                }
            
            else:
                data = {"error": "Endpoint not found"}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
            
        except Exception as e:
            self.send_error(500, str(e))

if __name__ == "__main__":
    print(f"🚀 Starting simple server on port {PORT}")
    print(f"📊 Loading data from: {CSV_PATH}")
    print(f"🌐 Frontend: http://localhost:{PORT}/index.html")
    
    with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
        print("✅ Server started! Press Ctrl+C to stop")
        httpd.serve_forever() 