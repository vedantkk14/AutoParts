from faker import Faker
import random
from .models import Customer

fake = Faker('en_IN')   # Indian locale for realistic names & cities

# ── Indian cities commonly seen in auto-parts wholesale ──────────────────────
INDIAN_CITIES = [
    'Mumbai', 'Pune', 'Delhi', 'Solapur', 'Pandharpur', 'Mohol'
]

# ── Auto-parts business name suffixes ────────────────────────────────────────
BUSINESS_SUFFIXES = [
    'Auto Parts', 'Motors', 'Auto Traders', 'Spares', 'Auto Works',
    'Enterprises', 'Auto Hub', 'Car Parts', 'Spare Parts', 'Auto Depot',
    'Auto Suppliers', 'Auto Zone', 'Vehicle Parts', 'Auto Mart',
]


def generate_indian_phone():
    """Return a valid 10-digit Indian mobile number as an integer."""
    # Indian mobile numbers start with 6, 7, 8, or 9
    first_digit = random.choice([6, 7, 8, 9])
    remaining   = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    return int(f'{first_digit}{remaining}')


def seed_customers(n):
    """
    Create `n` fake Customer records.
    Skips creation if the DB already has >= n customers to avoid duplicates.

    Usage (from a Django shell or management command):
        from customers.seed import seed_customers
        seed_customers(20)
    """
    existing_count = Customer.objects.count()
    if existing_count >= n:
        print(f'[seed] Already {existing_count} customers in DB. Skipping.')
        return

    to_create = n - existing_count
    customers  = []

    for _ in range(to_create):
        last_name    = fake.last_name()
        company_name = f'{last_name} {random.choice(BUSINESS_SUFFIXES)}'

        customers.append(Customer(
            customer_company_name = company_name,
            customer_name         = fake.name(),
            customer_phone_number = generate_indian_phone(),
            customer_city         = random.choice(INDIAN_CITIES),
        ))

    Customer.objects.bulk_create(customers)
    print(f'[seed] ✅ Created {to_create} fake customers. Total: {Customer.objects.count()}')
