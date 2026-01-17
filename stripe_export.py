import os
import csv
import requests
from datetime import datetime
from dotenv import load_dotenv 

# - - - - - - -
# LOAD API KEY
# - - - - - - -

# Load the .env file 
load_dotenv()

def load_api_key():
    # Load Stripe API key from environment variable
    api_key = os.getenv("STRIPE_SECRET_KEY")
    if not api_key:
        raise ValueError("STRIPE_SECRET_KEY environemnt variable not set")
    return api_key

# - - - - - - -
# FETCH TRANSACTIONS
# - - - - - - -

def fetch_transactions(api_key, limit=100):
    print(f"Fetching up to {limit} transactions from Stripe...")

    url = "https://api.stripe.com/v1/charges"
    headers = {
    "Authorization": f"Bearer {api_key}"
    }
    params = {
    "limit": limit
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        charges = data.get('data', [])
        print(f"Successfully fetched {len(charges)} transactions")
        return charges

    except requests.exceptions.RequestException as e:
        print("Error fetching transactions: {str(e)}")
        raise

# - - - - - - -
# EXTRACT CHARGES
# - - - - - - -

def extract_fields(charge):
    # Extract required fields from a Stripe charge object.
    payment_method = charge.get('paymemt_method_details', {})
    payment_type = payment_method.get('type', 'N/A') if payment_method else 'N/A'

    return {
        'id': charge.get('id', 'N/A'),
        'amount': format_amount(charge.get('amount', 0), charge.get('currency', 'usd')),
        'currency': charge.get('currency', 'N/A').upper(),
        'status': charge.get('status') or 'N/A',
        'customer': charge.get('customer') or 'N/A',
        'description': charge.get('description') or 'N/A',
        'created': format_date(charge.get('created', 0)),
        'receipt_email': charge.get('receipt_email') or 'N/A',
        'payment_method': payment_type
    }

# - - - - - - -
# FORMAT TRANSACTIONS
# - - - - - - -

def format_amount(amount, currency):
    # Format amount from cents to dollars (or approporiate unit).

    return f"{amount / 100:.2f}"

def format_date(timestamp):
    # Format Unix timestamp to readable date.
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# - - - - - - -
# CREATE CSV
# - - - - - - -

def write_to_csv(transactions, filename='stripe_transactions.csv'):
    if not transactions:
        print("No transactiosn to write")
        return
    
    headers = [ 'id', 'amount', 'currency', 'status', 'customer', 
               'description', 'created', 'receipt_email', 'payment_method']
    print(f"Writing {len(transactions)} transactions to {filename}...")

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(transactions)

    print(f"Succesfully exported to {filename}")

# - - - - - - -
# MAIN CTRL
# - - - - - - -

def main():
    # Main execution function
    try:

        # Load API key from environment 
        api_key = load_api_key()

        # Fetch transactions from Stripe
        charges = fetch_transactions(api_key, limit=100)

        # Extract required fields
        transactions = [extract_fields(charge) for charge in charges]

        # Write to CSV
        write_to_csv(transactions)

        print('\n✓ Export completed successfully!')

    except ValueError as e:
        print(f"Configuration error: {str(e)}")
        print(f"\nPlease set your Stripe API key")
        print("export stripe_secret_key='sk_test_...'")
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())