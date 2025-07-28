# Backend - FastAPI Financial Dashboard

This directory will contain the FastAPI backend implementation for the Howard Financial Dashboard.

## Future Implementation

The backend will provide:

- RESTful API endpoints for transaction data
- Database integration (PostgreSQL/SQLite)
- Data validation and processing
- Authentication and authorization
- Real-time data updates

## Planned API Endpoints

```
GET /api/v1/transactions - Retrieve all transactions
GET /api/v1/transactions/{id} - Get specific transaction
POST /api/v1/transactions - Create new transaction
PUT /api/v1/transactions/{id} - Update transaction
DELETE /api/v1/transactions/{id} - Delete transaction
GET /api/v1/summary - Get financial summary
GET /api/v1/categories - Get transaction categories
```

## Development Setup (To be implemented)

```bash
pip install fastapi uvicorn sqlalchemy alembic
uvicorn main:app --reload
```

## Database Schema (Planned)

```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    type VARCHAR(20) NOT NULL,
    category VARCHAR(50),
    vendor VARCHAR(100),
    account VARCHAR(50),
    running_balance DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```