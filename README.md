# Stripe Transactions Export to CSV

A Python automation tool to export Stripe transactions to CSV format.

## Features

- 🔐 Secure API key management with environment variables
- 📊 Fetches balance transactions from Stripe API
- 💰 Formats amounts from cents to dollars
- 📅 Converts timestamps to readable dates
- 📁 Exports to clean CSV format
- ✨ Easy to use and customise

## Project Structure

```
stripe-transactions-export/
│
├── output/
│   └── stripe_transactions.csv    # Generated CSV file
│
├── stripe_export.py                # Main Python script
├── README.md                       # This file
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
└── requirements.txt                # Python dependencies
```

## Setup Instructions

### 1. Clone or Create the Project

Create a new directory and set up the project structure.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Get your Stripe API key:
   - Go to [Stripe Dashboard](https://dashboard.stripe.com/apikeys)
   - Copy your **Secret Key** (starts with `sk_test_` for test mode)

3. Edit `.env` and add your key:
   ```
   STRIPE_SECRET_KEY=sk_test_your_actual_key_here
   ```

### 4. Run the Script

```bash
python stripe_export.py
```

## Usage

The script will:
1. Load your Stripe API key from `.env`
2. Fetch the last 100 transactions (configurable)
3. Extract and format transaction data
4. Save to `output/stripe_transactions.csv`

### Customise Transaction Limit

Edit the `fetch_transactions()` call in `stripe_export.py`:

```python
transactions = fetch_transactions(limit=500)  # Fetch 500 transactions
```

## CSV Output Format

The exported CSV includes these columns:

| Column | Description |
|--------|-------------|
| id | Stripe transaction ID |
| type | Transaction type (charge, refund, etc.) |
| amount | Gross amount |
| net | Net amount after fees |
| fee | Stripe fee |
| currency | Currency code (USD, EUR, etc.) |
| status | Transaction status |
| created | Date and time created |
| description | Transaction description |
| source | Source ID |

## Security Notes

⚠️ **Important**: Never commit your `.env` file to version control!

- The `.gitignore` file is configured to exclude `.env`
- Always use environment variables for API keys
- Use test mode keys during development

## Troubleshooting

### "Invalid API key" Error
- Check that your API key is correctly set in `.env`
- Ensure you're using the Secret Key, not Publishable Key
- Verify the key matches your Stripe account mode (test/live)

### "No transactions found"
- Your account may not have any transactions yet
- Check that you're using the correct API key for your mode
- Try creating a test transaction in the Stripe Dashboard

## Advanced Usage

### Filter by Date Range

Modify the `fetch_transactions()` function:

```python
def fetch_transactions(limit=100, created_after=None):
    params = {'limit': limit}
    if created_after:
        params['created'] = {'gte': created_after}
    
    transactions = stripe.BalanceTransaction.list(**params)
    return transactions.data
```

### Export Different Transaction Types

Filter by transaction type in `extract_transaction_data()`:

```python
# Only export charges
if txn.type == 'charge':
    extracted_data.append(data)
```

## License

MIT License - feel free to use and modify as needed.

## Support

For Stripe API documentation, visit: https://stripe.com/docs/api

---

**Happy exporting! 🚀**
