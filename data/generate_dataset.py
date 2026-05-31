import pandas as pd
import numpy as np
import random
import os

random.seed(42)
np.random.seed(42)

cities = {
    'Chennai': 300, 'Coimbatore': 200, 'Madurai': 150, 'Trichy': 120,
    'Salem': 100, 'Tiruppur': 80, 'Vellore': 70, 'Thanjavur': 60,
    'Tirunelveli': 60, 'Tuticorin': 40, 'Kanyakumari': 40, 'Erode': 40
}

cuisines = [
    'South Indian', 'Chettinad', 'Biryani', 'Chinese', 'Fast Food', 
    'North Indian', 'Tandoori', 'Seafood', 'Desserts', 'Beverages', 
    'Street Food', 'Mughlai', 'Bakery', 'Cafe', 'Arabian', 'Kothu Parotta'
]

restaurant_types = ['Quick Bites', 'Casual Dining', 'Cafe', 'Delivery',
                    'Dessert Parlour', 'Food Court', 'Fine Dining', 'Bakery']

areas = {
    'Chennai': ['Anna Nagar', 'T Nagar', 'Velachery', 'Adyar', 'Nungambakkam', 'OMR', 'Mylapore', 'Tambaram'],
    'Coimbatore': ['RS Puram', 'Gandhipuram', 'Peelamedu', 'Saibaba Colony', 'Saravanampatti', 'Race Course'],
    'Madurai': ['KK Nagar', 'Simmakkal', 'Goripalayam', 'Anna Nagar', 'Mattuthavani', 'Aarapalayam'],
    'Trichy': ['Thillai Nagar', 'Cantonment', 'Srirangam', 'KK Nagar', 'Chatram'],
    'Salem': ['New Bus Stand', 'Four Roads', 'Fairlands', 'Hasthampatti', 'Meyyanur'],
    'Tiruppur': ['Avinashi Road', 'Khaderpet', 'Palladam Road', 'Dharapuram Road'],
    'Vellore': ['Sathuvachari', 'Katpadi', 'Gandhi Nagar', 'Bagayam'],
    'Thanjavur': ['Medical College Road', 'Old Bus Stand', 'Mariamman Kovil', 'South Rampart'],
    'Tirunelveli': ['Palayamkottai', 'Vannarpettai', 'Junction', 'Town'],
    'Tuticorin': ['Cruz Puram', 'WGC Road', 'Millerpuram', 'Chidambara Nagar'],
    'Kanyakumari': ['Nagercoil Town', 'Beach Road', 'Kanyakumari Main'],
    'Erode': ['Perundurai Road', 'Sathy Road', 'Bus Stand Area']
}

prefixes = ['Sri', 'Hotel', 'A2B', 'Anjappar', 'Thalappakatti', 'Junior Kuppanna', 'Salem RR', 'Karaikudi', 'Madurai Kannappar', 'Sangeetha', 'Ambur Star', '']
names = [
    'Saravana Bhavan', 'Ananda Bhavan', 'Aryaas', 'Veg Restaurant', 'Biryani Hotel',
    'Chettinad Mess', 'Vilasam', 'Unavagam', 'Canteen', 'Grand Restaurant',
    'Spicy Kitchen', 'Tiffin Room', 'Kalyan Mess', 'Star Biryani', 'Nair Mess',
    'Salem Mess', 'Bhavan', 'Dosa Club', 'Cafe Coffee', 'Momo House',
    'Aroma', 'Urban Dhaba', 'Biryani Bucket', 'Bun Parotta Corner', 'Jigarthanda Hub'
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
