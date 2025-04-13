import json

ORDERS_FILE = 'orders/orders.json'
KITCHEN_FILE = 'kitchen/kitchen_orders.json'
PAYMENTS_FILE = 'payments/payments.json'

# List of files to clear
files_to_clear = [ORDERS_FILE, KITCHEN_FILE, PAYMENTS_FILE]

for filepath in files_to_clear:
    try:
        with open(filepath, 'w') as f:
            json.dump([], f, indent=2)
        print(f'✅ cleared: {filepath}')
    except FileNotFoundError:
        print(f'⚠️ File not found: {filepath}')
    except Exception as e:
        print(f'❌ Error clearing {filepath}: {e}')
