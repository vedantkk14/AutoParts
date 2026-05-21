import os
import sys
import random
import django
from faker import Faker

# Add project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from inventory.models import Inventory, VehicleCompatibility

# Define realistic automotive parts data
PARTS_TEMPLATES = {
    'braking': [
        ('Front Brake Pad Set', 'BP'),
        ('Rear Brake Pad Set', 'BP'),
        ('Brake Rotor Disc - Front', 'BR'),
        ('Brake Rotor Disc - Rear', 'BR'),
        ('Brake Caliper Assembly', 'BC'),
        ('Brake Booster Hose', 'BH'),
        ('Brake Master Cylinder', 'BM'),
    ],
    'engine': [
        ('Engine Oil Filter', 'OF'),
        ('Air Filter Element', 'AF'),
        ('Cabin AC Filter', 'CF'),
        ('Spark Plug Platinum', 'SP'),
        ('Timing Belt Kit', 'TB'),
        ('Engine Valve Cover Gasket', 'VG'),
        ('Fuel Injector Nozzle', 'FI'),
        ('Piston Ring Set', 'PR'),
    ],
    'suspension': [
        ('Front Shock Absorber Strut', 'SA'),
        ('Rear Shock Absorber', 'SA'),
        ('Lower Control Arm Left', 'CA'),
        ('Lower Control Arm Right', 'CA'),
        ('Stabilizer Link Rod', 'LR'),
        ('Tie Rod End Outer', 'TR'),
        ('Ball Joint Front Upper', 'BJ'),
    ],
    'electrical': [
        ('12V Car Battery', 'BT'),
        ('Alternator Assembly 90A', 'AL'),
        ('Starter Motor Assembly', 'SM'),
        ('LED Headlight Bulb H4', 'HL'),
        ('Ignition Coil Pack', 'IC'),
        ('Oxygen Sensor O2', 'OS'),
        ('Windshield Wiper Motor', 'WM'),
    ],
    'other': [
        ('Radiator Cooling Fan', 'RF'),
        ('Clutch Plate & Cover Kit', 'CP'),
        ('Wheel Bearing Front Hub', 'WB'),
        ('Engine Underbody Shield', 'US'),
    ]
}

VEHICLES_MAP = {
    'toyota': ['Innova', 'Fortuner', 'Corolla Altis', 'Glanza', 'Yaris'],
    'honda': ['City', 'Civic', 'Amaze', 'Jazz', 'WR-V'],
    'maruti_suzuki': ['Swift', 'Baleno', 'Alto 800', 'Ertiga', 'WagonR', 'Brezza', 'Dzire'],
    'hyundai': ['Creta', 'i20', 'Verna', 'Grand i10', 'Tucson', 'Venue'],
    'kia': ['Seltos', 'Sonet', 'Carens', 'Carnival'],
    'mahindra': ['XUV700', 'Scorpio-N', 'Thar', 'Bolero', 'XUV300'],
    'tata': ['Nexon', 'Harrier', 'Safari', 'Altroz', 'Punch', 'Tiago'],
    'volkswagen': ['Polo', 'Vento', 'Taigun', 'Virtus'],
    'skoda': ['Rapid', 'Octavia', 'Superb', 'Kushaq', 'Slavia'],
    'Renault': ['Kwid', 'Triber', 'Kiger', 'Duster'],
    'nissan': ['Magnite', 'Sunny', 'Terrano']
}

def seed_data(num_items=30):
    fake = Faker()
    
    print(f"Starting database seed: Creating {num_items} inventory items...")
    
    # Optional: Clear existing inventory if requested, but let's keep it safe and just append new items
    # Inventory.objects.all().delete()
    
    brands = [b[0] for b in Inventory.Brand.choices]
    categories = [c[0] for c in Inventory.Category.choices]
    makes = [m[0] for m in VehicleCompatibility.Make.choices]
    
    created_count = 0
    sku_attempts = 0
    
    while created_count < num_items and sku_attempts < 1000:
        category = random.choice(categories)
        templates = PARTS_TEMPLATES.get(category, PARTS_TEMPLATES['other'])
        part_base_name, sku_prefix = random.choice(templates)
        
        # Add random modifier to part name to avoid identical names
        modifiers = ['Premium', 'Heavy Duty', 'Standard', 'Pro Series', 'OEM Spec', 'Eco-Line']
        modifier = random.choice(modifiers)
        part_name = f"{modifier} {part_base_name}"
        
        # Build unique SKU
        sku_num = random.randint(10000, 99999)
        sku = f"{sku_prefix}-{sku_num}"
        
        if Inventory.objects.filter(sku=sku).exists():
            sku_attempts += 1
            continue
            
        brand = random.choice(brands)
        description = fake.paragraph(nb_sentences=3)
        initial_stock = random.randint(0, 80)
        low_stock_threshold = random.randint(3, 10)
        
        aisle = random.choice(['A', 'B', 'C', 'D', 'E', 'F'])
        aisle_num = random.randint(1, 25)
        aisle_location = f"{aisle}{aisle_num}"
        
        bin_num = random.randint(1, 50)
        bin_location = f"B{bin_num}"
        
        wholesale_price = round(random.uniform(80.00, 8000.00), 2)
        retail_price = round(wholesale_price * random.uniform(1.20, 1.60), 2)
        is_taxable = random.choice([True, False])
        status = random.choice(['active', 'draft'])
        
        # Create Inventory item
        item = Inventory.objects.create(
            part_name=part_name,
            sku=sku,
            category=category,
            brand=brand,
            description=description,
            initial_stock=initial_stock,
            low_stock_threshold=low_stock_threshold,
            aisle_location=aisle_location,
            bin_location=bin_location,
            wholesale_price=wholesale_price,
            retail_price=retail_price,
            is_taxable=is_taxable,
            status=status
        )
        
        # Create 1 to 3 Vehicle Compatibilities
        num_vehicles = random.randint(1, 3)
        chosen_makes = random.sample(list(VEHICLES_MAP.keys()), num_vehicles)
        
        for vehicle_make in chosen_makes:
            models_list = VEHICLES_MAP[vehicle_make]
            model_name = random.choice(models_list)
            
            start_year = random.randint(2010, 2023)
            end_year = start_year + random.randint(2, 6)
            # Cap at current year
            if end_year > 2026:
                end_year = 2026
            year_range = f"{start_year}-{end_year}"
            
            VehicleCompatibility.objects.create(
                part=item,
                make=vehicle_make,
                model_name=model_name,
                year_range=year_range
            )
            
        created_count += 1
        print(f"Created: {item.part_name} | SKU: {item.sku}")
        
    print(f"\nSeed completed! Successfully added {created_count} items with vehicle compatibilities.")

if __name__ == '__main__':
    seed_data(30)
