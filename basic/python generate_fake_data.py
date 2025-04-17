import csv
import random
from faker import Faker

# Initialize Faker
fake = Faker()

# Cities list
cities = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
    "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte",
    "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington"
]

# Number of rows
num_rows = 10000

# Output CSV file
output_file = 'basic/datasets/fake_data.csv'

# Write to CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['name', 'age', 'city', 'sales'])  # Header
    
    for _ in range(num_rows):
        name = fake.name()
        age = random.randint(20, 60)
        city = random.choice(cities)
        sales = random.randint(10000, 50000)
        
        writer.writerow([name, age, city, sales])

print(f"Successfully generated {num_rows} rows into '{output_file}'!")
