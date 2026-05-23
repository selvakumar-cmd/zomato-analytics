import pandas as pd
import numpy as np
import random
import os

random.seed(42)
np.random.seed(42)

cities = {
    'Bangalore': 180, 'Mumbai': 160, 'Delhi': 150, 'Hyderabad': 120,
    'Chennai': 110, 'Pune': 100, 'Kolkata': 90, 'Ahmedabad': 70,
    'Jaipur': 60, 'Surat': 50, 'Lucknow': 50, 'Kochi': 40,
    'Chandigarh': 35, 'Indore': 35, 'Bhopal': 30
}

cuisines = [
    'North Indian', 'South Indian', 'Chinese', 'Fast Food', 'Biryani',
    'Pizza', 'Mughlai', 'Continental', 'Italian', 'Street Food',
    'Desserts', 'Beverages', 'Seafood', 'Bengali', 'Rajasthani',
    'Gujarati', 'Punjabi', 'Thai', 'Mexican', 'Cafe'
]

restaurant_types = ['Quick Bites', 'Casual Dining', 'Cafe', 'Delivery',
                    'Dessert Parlour', 'Food Court', 'Fine Dining', 'Bakery']

areas = {
    'Bangalore': ['Koramangala', 'Indiranagar', 'Whitefield', 'HSR Layout', 'BTM Layout', 'Jayanagar', 'MG Road'],
    'Mumbai': ['Bandra', 'Andheri', 'Juhu', 'Powai', 'Colaba', 'Dadar', 'Borivali'],
    'Delhi': ['Connaught Place', 'Lajpat Nagar', 'Karol Bagh', 'Saket', 'Dwarka', 'Rohini'],
    'Hyderabad': ['Banjara Hills', 'Jubilee Hills', 'Hitech City', 'Gachibowli', 'Secunderabad'],
    'Chennai': ['Anna Nagar', 'T Nagar', 'Velachery', 'Adyar', 'Nungambakkam', 'OMR'],
    'Pune': ['Koregaon Park', 'Baner', 'Hinjewadi', 'Kothrud', 'Viman Nagar'],
    'Kolkata': ['Park Street', 'Salt Lake', 'New Town', 'Gariahat', 'Behala'],
    'Ahmedabad': ['SG Highway', 'CG Road', 'Navrangpura', 'Satellite'],
    'Jaipur': ['MI Road', 'Vaishali Nagar', 'C Scheme', 'Malviya Nagar'],
    'Surat': ['Adajan', 'Vesu', 'Athwa', 'Katargam'],
    'Lucknow': ['Hazratganj', 'Gomti Nagar', 'Aliganj'],
    'Kochi': ['Marine Drive', 'Edappally', 'Kakkanad'],
    'Chandigarh': ['Sector 17', 'Sector 22', 'Sector 35'],
    'Indore': ['Vijay Nagar', 'Palasia', 'Bhawarkua'],
    'Bhopal': ['MP Nagar', 'Arera Colony', 'New Market']
}

prefixes = ['The', 'Hotel', 'Cafe', 'Restaurant', '', '', '', 'Shree', 'New', 'Royal']
names = [
    'Spice Garden', 'Food Hub', 'Taste of India', 'Biryani House', 'Pizza Palace',
    'Dosa Corner', 'Curry Leaf', 'Burger Barn', 'Saffron', 'Masala Twist',
    'The Hungry Tiger', 'Food Street', 'Kebab King', 'Sweet Tooth', 'Noodle Box',
    'Dhaba Express', 'Chaat Junction', 'Grill House', 'Tiffin Box', 'Momo Point',
    'Fusion Bites', 'Classic Dining', 'Urban Kitchen', 'Flavor Town', 'Spicy Treat',
    'Crave Kitchen', 'The Food Lab', 'Aroma Restaurant', 'Taste Buds', 'Cloud Kitchen'
]

rows = []
for city, count in cities.items():
    city_areas = areas.get(city, ['City Center'])
    for _ in range(count):
        rest_type = random.choice(restaurant_types)
        cuisine_count = random.randint(1, 3)
        selected_cuisines = ', '.join(random.sample(cuisines, cuisine_count))
        online_order = random.choices(['Yes', 'No'], weights=[65, 35])[0]
        book_table = random.choices(['Yes', 'No'], weights=[30, 70])[0]

        if rest_type == 'Fine Dining':
            rating = round(random.uniform(3.8, 4.9), 1)
            cost = random.randint(1500, 4000)
            votes = random.randint(200, 2000)
        elif rest_type in ['Casual Dining', 'Cafe']:
            rating = round(random.uniform(3.2, 4.7), 1)
            cost = random.randint(400, 1200)
            votes = random.randint(50, 1500)
        else:
            rating = round(random.uniform(2.5, 4.5), 1)
            cost = random.randint(100, 600)
            votes = random.randint(10, 800)

        # Add some noise
        if random.random() < 0.05:
            rating = None
        if random.random() < 0.03:
            votes = None

        prefix = random.choice(prefixes)
        name = random.choice(names)
        restaurant_name = f"{prefix} {name}".strip() if prefix else name

        rows.append({
            'Restaurant_Name': restaurant_name,
            'City': city,
            'Area': random.choice(city_areas),
            'Cuisines': selected_cuisines,
            'Restaurant_Type': rest_type,
            'Online_Order': online_order,
            'Book_Table': book_table,
            'Rating': rating,
            'Votes': votes,
            'Cost_For_Two': cost
        })

df = pd.DataFrame(rows)
os.makedirs('../dataset', exist_ok=True)
df.to_csv('../dataset/zomato_raw.csv', index=False)
print(f"✅ Dataset generated: {len(df)} restaurants across {df['City'].nunique()} cities")
print(df.head())
