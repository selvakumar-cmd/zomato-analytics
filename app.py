import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Zomato Analytics", page_icon="🍽️", layout="wide")

# App Title
st.title("🍽️ Zomato India Restaurant Analytics")
st.markdown("Interactive dashboard exploring restaurant data across India. Built with Python & Streamlit.")
st.markdown("---")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("dataset/zomato_cleaned.csv")

df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filters")
st.sidebar.markdown("Filter the dashboard data below:")

cities = df['City'].unique()
selected_cities = st.sidebar.multiselect("Select City", cities, default=list(cities)[:5])

price_cats = df['Price_Category'].unique()
selected_price = st.sidebar.multiselect("Price Category", price_cats, default=list(price_cats))

# Apply Filters
df_filtered = df.copy()
if selected_cities:
    df_filtered = df_filtered[df_filtered['City'].isin(selected_cities)]
if selected_price:
    df_filtered = df_filtered[df_filtered['Price_Category'].isin(selected_price)]

# Top KPIs
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Restaurants", f"{len(df_filtered):,}")
col2.metric("Average Rating", f"⭐ {round(df_filtered['Rating'].mean(), 2)}")
col3.metric("Online Delivery %", f"{round((df_filtered['Online_Order'] == 'Yes').mean() * 100, 1)}%")
col4.metric("Avg Cost for Two", f"₹{round(df_filtered['Cost_For_Two'].mean())}")

st.markdown("<br>", unsafe_allow_html=True)

# First Row of Charts
c1, c2 = st.columns(2)

with c1:
    st.markdown("### 🏙️ Restaurants by City")
    city_counts = df_filtered['City'].value_counts().reset_index()
    fig_city = px.bar(city_counts, x='City', y='count', 
                      color='count', color_continuous_scale='Reds',
                      labels={'count':'Number of Restaurants'})
    st.plotly_chart(fig_city, use_container_width=True)

with c2:
    st.markdown("### ⭐ Rating Distribution")
    fig_rating = px.histogram(df_filtered, x='Rating', nbins=20, 
                              color_discrete_sequence=['#E23744'],
                              labels={'count':'Restaurants'})
    st.plotly_chart(fig_rating, use_container_width=True)

# Second Row of Charts
c3, c4 = st.columns(2)

with c3:
    st.markdown("### 📱 Online Order Availability")
    fig_online = px.pie(df_filtered, names='Online_Order', 
                        color='Online_Order', 
                        color_discrete_map={'Yes':'#2ECC71', 'No':'#E23744'},
                        hole=0.4)
    st.plotly_chart(fig_online, use_container_width=True)

with c4:
    st.markdown("### 💰 Price vs Rating Analysis")
    fig_scatter = px.scatter(df_filtered, x='Cost_For_Two', y='Rating', 
                             size='Votes', color='Rating', 
                             color_continuous_scale='RdYlGn',
                             hover_name='Restaurant_Name')
    st.plotly_chart(fig_scatter, use_container_width=True)

# Top Restaurants Table
st.markdown("---")
st.subheader("🏆 Top 10 Best Value-for-Money Restaurants")
st.markdown("Sorted by Value Score (Rating / Cost)")
top_value = df_filtered[df_filtered['Votes'] > 50].nlargest(10, 'Value_Score')
display_df = top_value[['Restaurant_Name', 'City', 'Area', 'Rating', 'Cost_For_Two', 'Votes', 'Value_Score']]
st.dataframe(display_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("Built by **SELVAKUMAR-ANALYST** | Powered by Streamlit & Plotly")
