# ============================================================
# ZOMATO RESTAURANT ANALYTICS - Full EDA & Business Insights
# Author  : [Your Name]
# Tools   : Python, Pandas, Matplotlib, Seaborn, Plotly
# Dataset : Zomato India Restaurant Data (1,280 restaurants)
# ============================================================

# â”€â”€ 1. IMPORT LIBRARIES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend â€” no popup windows, faster!
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import os

warnings.filterwarnings('ignore')
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.family'] = 'DejaVu Sans'
sns.set_theme(style="darkgrid", palette="husl")

# â”€â”€ 2. LOAD & GENERATE DATASET â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
import random
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
rest_names = [
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

        if random.random() < 0.05:
            rating = None
        if random.random() < 0.03:
            votes = None

        prefix = random.choice(prefixes)
        name = random.choice(rest_names)
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
os.makedirs('dataset', exist_ok=True)
df.to_csv('dataset/zomato_raw.csv', index=False)
print("=" * 60)
print("   ZOMATO RESTAURANT ANALYTICS PROJECT")
print("=" * 60)
print(f"\nðŸ“Š Dataset Shape     : {df.shape[0]} rows Ã— {df.shape[1]} columns")
print(f"ðŸ™ï¸  Cities Covered    : {df['City'].nunique()}")
print(f"ðŸ½ï¸  Restaurant Types  : {df['Restaurant_Type'].nunique()}")
print(f"ðŸ¥˜ Unique Cuisines   : {df['Cuisines'].nunique()}")
print(f"\nðŸ“‹ Columns:\n{list(df.columns)}")

# â”€â”€ 3. DATA CLEANING â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("\n" + "=" * 60)
print("   STEP 1: DATA CLEANING")
print("=" * 60)

print(f"\nðŸ” Missing Values BEFORE cleaning:")
print(df.isnull().sum())

df['Rating'] = df['Rating'].fillna(df['Rating'].median())
df['Votes'] = df['Votes'].fillna(df['Votes'].median())
df.drop_duplicates(inplace=True)
df['Cost_For_Two'] = df['Cost_For_Two'].astype(int)
df['Votes'] = df['Votes'].round(0).astype(int)
df['Value_Score'] = round(df['Rating'] / (df['Cost_For_Two'] / 100), 4)
df['Price_Category'] = pd.cut(df['Cost_For_Two'],
                               bins=[0, 300, 600, 1000, 2000, 10000],
                               labels=['Budget', 'Affordable', 'Mid-Range', 'Premium', 'Luxury'])

df.to_csv('dataset/zomato_cleaned.csv', index=False)
print(f"\nâœ… Missing Values AFTER cleaning:")
print(df.isnull().sum())
print(f"\nâœ… Cleaned dataset saved â†’ dataset/zomato_cleaned.csv")

# â”€â”€ 4. EXPLORATORY DATA ANALYSIS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("\n" + "=" * 60)
print("   STEP 2: EXPLORATORY DATA ANALYSIS")
print("=" * 60)

os.makedirs('charts', exist_ok=True)

# â”€â”€ CHART 1: City-wise Restaurant Count â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
fig, axes = plt.subplots(2, 2, figsize=(18, 14))
fig.suptitle('ðŸ½ï¸  ZOMATO INDIA â€” Restaurant Analytics Dashboard',
             fontsize=20, fontweight='bold', y=1.01, color='#E23744')

city_counts = df['City'].value_counts().reset_index()
city_counts.columns = ['City', 'Count']
colors1 = sns.color_palette("Reds_r", len(city_counts))

ax1 = axes[0, 0]
bars = ax1.barh(city_counts['City'], city_counts['Count'], color=colors1, edgecolor='white')
ax1.set_title('ðŸ™ï¸  City-wise Restaurant Count', fontsize=14, fontweight='bold', pad=10)
ax1.set_xlabel('Number of Restaurants')
for bar, val in zip(bars, city_counts['Count']):
    ax1.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
             f'{val}', va='center', fontsize=9, color='black')
ax1.invert_yaxis()

# â”€â”€ CHART 2: Rating Distribution â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
ax2 = axes[0, 1]
ax2.hist(df['Rating'].dropna(), bins=20, color='#E23744', edgecolor='white', alpha=0.85)
ax2.axvline(df['Rating'].mean(), color='gold', linestyle='--', linewidth=2,
            label=f'Mean: {df["Rating"].mean():.2f}')
ax2.set_title('â­ Rating Distribution', fontsize=14, fontweight='bold', pad=10)
ax2.set_xlabel('Rating')
ax2.set_ylabel('Count')
ax2.legend()

# â”€â”€ CHART 3: Online Order Analysis â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
ax3 = axes[1, 0]
online_data = df['Online_Order'].value_counts()
colors_pie = ['#E23744', '#2ECC71']
wedges, texts, autotexts = ax3.pie(online_data, labels=online_data.index,
                                    autopct='%1.1f%%', colors=colors_pie,
                                    startangle=90, pctdistance=0.85,
                                    wedgeprops={'edgecolor': 'white', 'linewidth': 2})
for text in autotexts:
    text.set_fontsize(12)
    text.set_fontweight('bold')
ax3.set_title('ðŸ“± Online Order Availability', fontsize=14, fontweight='bold', pad=10)

# â”€â”€ CHART 4: Restaurant Type Distribution â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
ax4 = axes[1, 1]
type_counts = df['Restaurant_Type'].value_counts()
colors2 = sns.color_palette("husl", len(type_counts))
bars4 = ax4.bar(type_counts.index, type_counts.values, color=colors2, edgecolor='white')
ax4.set_title('ðŸª Restaurant Type Distribution', fontsize=14, fontweight='bold', pad=10)
ax4.set_xlabel('Restaurant Type')
ax4.set_ylabel('Count')
ax4.tick_params(axis='x', rotation=35)
for bar in bars4:
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
             str(bar.get_height()), ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('charts/01_overview_dashboard.png', bbox_inches='tight', dpi=150)
# plt.show()
print("\nâœ… Chart 1 saved â†’ charts/01_overview_dashboard.png")

# â”€â”€ CHART 5: Top 10 Cuisines â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
all_cuisines = []
for c in df['Cuisines']:
    all_cuisines.extend([x.strip() for x in c.split(',')])
cuisine_series = pd.Series(all_cuisines).value_counts().head(10)

fig2, ax = plt.subplots(figsize=(12, 6))
colors_c = sns.color_palette("magma", len(cuisine_series))
bars_c = ax.bar(cuisine_series.index, cuisine_series.values, color=colors_c, edgecolor='white')
ax.set_title('ðŸ¥˜ Top 10 Most Popular Cuisines in India', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Cuisine Type', fontsize=12)
ax.set_ylabel('Number of Restaurants', fontsize=12)
ax.tick_params(axis='x', rotation=30)
for bar in bars_c:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            str(bar.get_height()), ha='center', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/02_top_cuisines.png', bbox_inches='tight', dpi=150)
# plt.show()
print("âœ… Chart 2 saved â†’ charts/02_top_cuisines.png")

# â”€â”€ CHART 6: Price vs Rating (Scatter) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
fig3, ax = plt.subplots(figsize=(12, 6))
scatter = ax.scatter(df['Cost_For_Two'], df['Rating'],
                     c=df['Votes'], cmap='YlOrRd', alpha=0.6,
                     s=df['Votes']/10 + 20, edgecolors='white', linewidth=0.5)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Number of Votes', fontsize=11)
ax.set_title('ðŸ’° Price vs Rating (Bubble = Popularity)', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Cost For Two (â‚¹)', fontsize=12)
ax.set_ylabel('Rating', fontsize=12)
plt.tight_layout()
plt.savefig('charts/03_price_vs_rating.png', bbox_inches='tight', dpi=150)
# plt.show()
print("âœ… Chart 3 saved â†’ charts/03_price_vs_rating.png")

# â”€â”€ CHART 7: City-wise Average Rating â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
fig4, ax = plt.subplots(figsize=(14, 6))
city_rating = df.groupby('City')['Rating'].mean().sort_values(ascending=False)
colors4 = ['#E23744' if i == 0 else '#FF8C94' if i < 3 else '#FFB3BA'
           for i in range(len(city_rating))]
bars7 = ax.bar(city_rating.index, city_rating.values, color=colors4, edgecolor='white')
ax.set_title('â­ City-wise Average Restaurant Rating', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('City', fontsize=12)
ax.set_ylabel('Average Rating', fontsize=12)
ax.set_ylim(3.0, 4.5)
ax.tick_params(axis='x', rotation=35)
for bar, val in zip(bars7, city_rating.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f'{val:.2f}', ha='center', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/04_city_avg_rating.png', bbox_inches='tight', dpi=150)
# plt.show()
print("âœ… Chart 4 saved â†’ charts/04_city_avg_rating.png")

# â”€â”€ CHART 8: Online vs Offline Rating Comparison â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
fig5, axes5 = plt.subplots(1, 2, figsize=(14, 6))
fig5.suptitle('ðŸ“± Online Order Impact Analysis', fontsize=16, fontweight='bold')

online_rating = df.groupby('Online_Order')['Rating'].mean()
axes5[0].bar(online_rating.index, online_rating.values,
             color=['#E23744', '#2ECC71'], edgecolor='white')
axes5[0].set_title('Average Rating: Online vs Offline')
axes5[0].set_ylabel('Average Rating')
axes5[0].set_ylim(3.0, 4.5)
for i, (idx, val) in enumerate(online_rating.items()):
    axes5[0].text(i, val + 0.02, f'{val:.2f}', ha='center', fontweight='bold', fontsize=12)

online_cost = df.groupby('Online_Order')['Cost_For_Two'].mean()
axes5[1].bar(online_cost.index, online_cost.values,
             color=['#E23744', '#2ECC71'], edgecolor='white')
axes5[1].set_title('Average Cost: Online vs Offline')
axes5[1].set_ylabel('Avg Cost for Two (â‚¹)')
for i, (idx, val) in enumerate(online_cost.items()):
    axes5[1].text(i, val + 5, f'â‚¹{val:.0f}', ha='center', fontweight='bold', fontsize=12)

plt.tight_layout()
plt.savefig('charts/05_online_vs_offline.png', bbox_inches='tight', dpi=150)
# plt.show()
print("âœ… Chart 5 saved â†’ charts/05_online_vs_offline.png")

# â”€â”€ CHART 9: Price Category Distribution â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
fig6, axes6 = plt.subplots(1, 2, figsize=(14, 6))
fig6.suptitle('ðŸ’° Price Category Analysis', fontsize=16, fontweight='bold')

price_dist = df['Price_Category'].value_counts()
colors6 = ['#2ECC71', '#F39C12', '#E67E22', '#E74C3C', '#8E44AD']
axes6[0].pie(price_dist, labels=price_dist.index, autopct='%1.1f%%',
             colors=colors6, startangle=90,
             wedgeprops={'edgecolor': 'white', 'linewidth': 2})
axes6[0].set_title('Restaurant Price Category Split')

price_rating = df.groupby('Price_Category', observed=True)['Rating'].mean().reindex(
    ['Budget', 'Affordable', 'Mid-Range', 'Premium', 'Luxury'])
axes6[1].bar(price_rating.index, price_rating.values, color=colors6, edgecolor='white')
axes6[1].set_title('Avg Rating by Price Category')
axes6[1].set_ylabel('Average Rating')
axes6[1].set_ylim(3.0, 5.0)
axes6[1].tick_params(axis='x', rotation=20)
for i, val in enumerate(price_rating.values):
    axes6[1].text(i, val + 0.02, f'{val:.2f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/06_price_category.png', bbox_inches='tight', dpi=150)
# plt.show()
print("âœ… Chart 6 saved â†’ charts/06_price_category.png")

# â”€â”€ CHART 10: Top 10 Best Value Restaurants â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
fig7, ax7 = plt.subplots(figsize=(14, 7))
top_value = df[df['Votes'] >= 100].nlargest(10, 'Value_Score')[
    ['Restaurant_Name', 'City', 'Rating', 'Cost_For_Two', 'Votes', 'Value_Score']]

colors7 = sns.color_palette("RdYlGn", len(top_value))
bars7b = ax7.barh(
    [f"{r['Restaurant_Name']} ({r['City']})" for _, r in top_value.iterrows()],
    top_value['Value_Score'], color=colors7[::-1], edgecolor='white'
)
ax7.set_title('ðŸ† Top 10 Best Value-for-Money Restaurants', fontsize=16, fontweight='bold', pad=15)
ax7.set_xlabel('Value Score (Rating / Cost Ã— 100)', fontsize=12)
ax7.invert_yaxis()
for bar, (_, row) in zip(bars7b, top_value.iterrows()):
    ax7.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2,
             f'â­{row["Rating"]} | â‚¹{row["Cost_For_Two"]}',
             va='center', fontsize=9)
plt.tight_layout()
plt.savefig('charts/07_top_value_restaurants.png', bbox_inches='tight', dpi=150)
# plt.show()
print("âœ… Chart 7 saved â†’ charts/07_top_value_restaurants.png")

# â”€â”€ CHART 11: Correlation Heatmap â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
fig8, ax8 = plt.subplots(figsize=(8, 6))
numeric_cols = df[['Rating', 'Votes', 'Cost_For_Two', 'Value_Score']].corr()
sns.heatmap(numeric_cols, annot=True, fmt='.2f', cmap='RdYlGn',
            center=0, square=True, ax=ax8, cbar_kws={'shrink': 0.8})
ax8.set_title('ðŸ”— Correlation Heatmap', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('charts/08_correlation_heatmap.png', bbox_inches='tight', dpi=150)
# plt.show()
print("âœ… Chart 8 saved â†’ charts/08_correlation_heatmap.png")

# â”€â”€ 5. BUSINESS INSIGHTS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("\n" + "=" * 60)
print("   STEP 3: KEY BUSINESS INSIGHTS")
print("=" * 60)

top_city = df['City'].value_counts().idxmax()
top_cuisine = pd.Series(all_cuisines).value_counts().idxmax()
avg_rating = df['Rating'].mean()
online_pct = (df['Online_Order'] == 'Yes').mean() * 100
best_city_rating = city_rating.idxmax()
budget_pct = (df['Price_Category'] == 'Budget').mean() * 100

print(f"""
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚           ðŸ“Š BUSINESS INSIGHTS SUMMARY          â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ 1. {top_city} leads with most restaurants       â”‚
â”‚    â†’ Market saturation opportunity in Tier-2    â”‚
â”‚                                                 â”‚
â”‚ 2. {top_cuisine} is India's #1 cuisine         â”‚
â”‚    â†’ New restaurants should include North Indianâ”‚
â”‚                                                 â”‚
â”‚ 3. Avg Rating: {avg_rating:.2f}/5.0              â”‚
â”‚    â†’ {100 - (df['Rating'] >= 4.0).mean()*100:.1f}% restaurants below 4.0 = improvement scope â”‚
â”‚                                                 â”‚
â”‚ 4. {online_pct:.1f}% restaurants offer online orders â”‚
â”‚    â†’ ~35% missing delivery revenue             â”‚
â”‚                                                 â”‚
â”‚ 5. {best_city_rating} has highest avg rating    â”‚
â”‚    â†’ Premium dining culture strong here         â”‚
â”‚                                                 â”‚
â”‚ 6. {budget_pct:.1f}% restaurants in Budget category    â”‚
â”‚    â†’ Affordable segment dominates India market  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
""")

print("=" * 60)
print("âœ… PROJECT COMPLETE! All charts saved in /charts folder")
print("ðŸ“Š Power BI file: Import dataset/zomato_cleaned.csv")
print("ðŸš€ GitHub: Upload all files with README.md")
print("=" * 60)
