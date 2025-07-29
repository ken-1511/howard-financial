# Howard Financial Dashboard

A modern financial dashboard for tracking and visualizing transaction data with FastAPI backend preparation.

## Project Architecture

This project is structured for both development with CSV data and production with FastAPI backend:

### Directory Structure

```
├── index.html                    # Main entry point (CSV mode)
├── cleaned_finance_transactions.csv  # Transaction data
├── frontend/                     # Frontend code for database integration
│   └── index.html               # Database-ready version
└── backend/                     # FastAPI backend (future implementation)
    └── README.md               # Backend planning and API specs
```

### Dual-Mode Architecture

The application supports two data source modes:

1. **CSV Mode** (Current): Direct file parsing in the root `index.html`
2. **Database Mode** (Future): API integration in `frontend/index.html`

## Technology Stack

- **Frontend**: HTML5, Tailwind CSS, Chart.js, PapaParse
- **Charts**: Chart.js with custom styling and animations
- **Fonts**: Inter font family for modern typography
- **Future Backend**: FastAPI, SQLAlchemy, PostgreSQL/SQLite

## Key Features

### Data Visualization
- Real-time financial metrics with trend indicators
- Interactive line charts with hover tooltips
- Color-coded transaction types (green=income, red=expense, blue=reimbursement)
- Category breakdown in chart tooltips

### User Interface
- Responsive design with sidebar navigation
- Gradient branding with purple color scheme
- Card-based layout with hover animations
- Loading skeletons for better UX

### Data Processing
- Automatic CSV parsing and validation
- Transaction filtering (excludes transfers)
- Running balance calculations
- Currency formatting and date handling

## CSV Data Format

Required columns:
- `Date`: Transaction date (MM/DD/YYYY)
- `Dollars`: Amount with $ symbol
- `Type`: income, expense, reimbursement, transfer
- `Category`: Transaction category
- `Vendor`: Merchant/payee name
- `USAA S`, `USAA C`: Account balances

## FastAPI Integration Plan

The `frontend/index.html` is configured for database mode with:
- API endpoint configuration
- Fallback to CSV if database unavailable
- RESTful API structure planning
- Authentication placeholder

## Development Notes

- Transaction colors: Green (income), Red (expense), Blue (reimbursement)
- Transfers are filtered out of calculations
- Chart uses smooth curves with filled areas
- Responsive grid system for mobile compatibility
- Error handling for data loading failures