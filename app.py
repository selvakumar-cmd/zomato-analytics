import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Zomato India Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS — Premium Dark Theme ──────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 50%, #16213e 100%);
    color: #e0e0e0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    border-right: 1px solid #E2374422;
}

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #E23744 0%, #c0392b 50%, #922b21 100%);
    padding: 2.5rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(226,55,68,0.3);
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    color: white;
    margin: 0;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-size: 1rem;
    color: rgba(255,255,255,0.85);
    margin-top: 0.5rem;
}
.hero-badges {
    margin-top: 1rem;
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}
.badge {
    background: rgba(255,255,255,0.15);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 500;
    border: 1px solid rgba(255,255,255,0.25);
}

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, #1e1e3a 0%, #252545 100%);
    border: 1px solid #E2374430;
    border-radius: 14px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(226,55,68,0.2);
    border-color: #E2374460;
}
.kpi-icon { font-size: 1.8rem; }
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    color: #E23744;
    margin: 0.3rem 0;
}
.kpi-label {
    font-size: 0.8rem;
    color: #888;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Section headers */
.section-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: #E23744;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 1rem;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid #E2374430;
}

/* Insight cards */
.insight-card {
    background: linear-gradient(135deg, #1e1e3a 0%, #252545 100%);
    border-left: 4px solid #E23744;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.2);
}
.insight-title {
    font-weight: 600;
    color: white;
    font-size: 0.9rem;
}
.insight-desc {
    color: #aaa;
    font-size: 0.82rem;
    margin-top: 0.2rem;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: #1a1a2e;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: #888;
    font-weight: 500;
    border-radius: 8px;
}
.stTabs [aria-selected="true"] {
    background: #E23744 !important;
    color: white !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #555;
    font-size: 0.8rem;
    padding: 1.5rem 0 0.5rem;
    border-top: 1px solid #222;
    margin-top: 2rem;
}
.footer a { color: #E23744; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("dataset/zomato_cleaned.csv")
    return df

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.markdown("## 🍽️ Zomato Analytics")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filters")

all_cities = sorted(df['City'].unique().tolist())
selected_cities = st.sidebar.multiselect(
    "🏙️ Select City",
    all_cities,
    default=all_cities[:6]
)

all_prices = sorted(df['Price_Category'].unique().tolist())
selected_price = st.sidebar.multiselect(
    "💰 Price Category",
    all_prices,
    default=all_prices
)

rating_range = st.sidebar.slider(
    "⭐ Minimum Rating",
    float(df['Rating'].min()),
    float(df['Rating'].max()),
    3.0,
    step=0.1
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Dataset Info")
st.sidebar.info(f"**{len(df):,}** Total Restaurants\n\n**{df['City'].nunique()}** Cities\n\n**{df['Cuisines'].nunique() if 'Cuisines' in df.columns else 'N/A'}** Cuisine Types")
st.sidebar.markdown("---")
st.sidebar.markdown("🔗 [GitHub Repo](https://github.com/SELVAKUMAR-ANALYST/zomato-analytics)")
st.sidebar.markdown("🚀 [Live Dashboard](https://zomato-analytics-selvakumar.streamlit.app/)")

# ── Apply Filters ─────────────────────────────────────────────
df_f = df.copy()
if selected_cities:
    df_f = df_f[df_f['City'].isin(selected_cities)]
if selected_price:
    df_f = df_f[df_f['Price_Category'].isin(selected_price)]
df_f = df_f[df_f['Rating'] >= rating_range]

# ── Hero Banner ───────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🍽️ Zomato India Restaurant Analytics</div>
    <div class="hero-subtitle">
        Exploring 1,280+ restaurants across 15 major Indian cities — 
        uncovering trends, patterns & business insights
    </div>
    <div class="hero-badges">
        <span class="badge">🐍 Python</span>
        <span class="badge">📊 Pandas</span>
        <span class="badge">📈 Plotly</span>
        <span class="badge">🗄️ SQL</span>
        <span class="badge">🚀 Streamlit</span>
        <span class="badge">📉 EDA</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────
total = len(df_f)
avg_rating = round(df_f['Rating'].mean(), 2) if total > 0 else 0
online_pct = round((df_f['Online_Order'] == 'Yes').mean() * 100, 1) if total > 0 else 0
avg_cost = round(df_f['Cost_For_Two'].mean()) if total > 0 else 0
total_votes = f"{int(df_f['Votes'].sum()):,}" if 'Votes' in df_f.columns else "N/A"

c1, c2, c3, c4, c5 = st.columns(5)
kpis = [
    (c1, "🏪", f"{total:,}", "Restaurants"),
    (c2, "⭐", avg_rating, "Avg Rating"),
    (c3, "📱", f"{online_pct}%", "Online Orders"),
    (c4, "💰", f"₹{avg_cost}", "Avg Cost/2"),
    (c5, "👍", total_votes, "Total Votes"),
]
for col, icon, val, label in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🏙️ City Analysis",
    "💡 Business Insights",
    "🏆 Top Restaurants"
])

# ════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    r1c1, r1c2 = st.columns(2)

    with r1c1:
        st.markdown('<div class="section-header">🏙️ Restaurants by City</div>', unsafe_allow_html=True)
        city_counts = df_f['City'].value_counts().reset_index()
        city_counts.columns = ['City', 'Count']
        fig = px.bar(city_counts, x='City', y='Count',
                     color='Count', color_continuous_scale='Reds',
                     template='plotly_dark')
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with r1c2:
        st.markdown('<div class="section-header">⭐ Rating Distribution</div>', unsafe_allow_html=True)
        fig = px.histogram(df_f, x='Rating', nbins=25,
                           color_discrete_sequence=['#E23744'],
                           template='plotly_dark')
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

    r2c1, r2c2 = st.columns(2)

    with r2c1:
        st.markdown('<div class="section-header">📱 Online vs Offline Orders</div>', unsafe_allow_html=True)
        fig = px.pie(df_f, names='Online_Order',
                     color='Online_Order',
                     color_discrete_map={'Yes': '#E23744', 'No': '#2d2d5a'},
                     hole=0.5,
                     template='plotly_dark')
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0)
        )
        fig.update_traces(textfont_size=14)
        st.plotly_chart(fig, use_container_width=True)

    with r2c2:
        st.markdown('<div class="section-header">💰 Cost vs Rating (Bubble = Votes)</div>', unsafe_allow_html=True)
        fig = px.scatter(df_f, x='Cost_For_Two', y='Rating',
                         size='Votes', color='Rating',
                         color_continuous_scale='RdYlGn',
                         hover_name='Restaurant_Name',
                         template='plotly_dark')
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════
# TAB 2 — CITY ANALYSIS
# ════════════════════════════════════════════════════════
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    city_stats = df_f.groupby('City').agg(
        Total=('Restaurant_Name', 'count'),
        Avg_Rating=('Rating', 'mean'),
        Avg_Cost=('Cost_For_Two', 'mean'),
        Online_Pct=('Online_Order', lambda x: (x == 'Yes').mean() * 100)
    ).reset_index().round(2)
    city_stats = city_stats.sort_values('Avg_Rating', ascending=False)

    t2c1, t2c2 = st.columns(2)

    with t2c1:
        st.markdown('<div class="section-header">📊 Avg Rating by City</div>', unsafe_allow_html=True)
        fig = px.bar(city_stats.sort_values('Avg_Rating'),
                     x='Avg_Rating', y='City', orientation='h',
                     color='Avg_Rating', color_continuous_scale='RdYlGn',
                     template='plotly_dark')
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

    with t2c2:
        st.markdown('<div class="section-header">💰 Avg Cost for Two by City</div>', unsafe_allow_html=True)
        fig = px.bar(city_stats.sort_values('Avg_Cost'),
                     x='Avg_Cost', y='City', orientation='h',
                     color='Avg_Cost', color_continuous_scale='Reds',
                     template='plotly_dark')
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">📋 City-wise KPI Summary Table</div>', unsafe_allow_html=True)
    city_stats.columns = ['City', 'Total Restaurants', 'Avg Rating', 'Avg Cost (₹)', 'Online Order %']
    st.dataframe(city_stats, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════
# TAB 3 — BUSINESS INSIGHTS
# ════════════════════════════════════════════════════════
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)

    t3c1, t3c2 = st.columns([1.2, 1])

    with t3c1:
        st.markdown('<div class="section-header">💡 Key Business Insights</div>', unsafe_allow_html=True)
        insights = [
            ("🏙️ Bangalore Leads", "180+ restaurants — highest competition market in India"),
            ("📱 Online = More Votes", "Restaurants with online ordering get 23% higher customer engagement"),
            ("💰 Budget Dominates", "45% of restaurants are in ₹200–₹500 range — highest volume segment"),
            ("⭐ Fine Dining Wins", "Premium restaurants average 0.4 higher rating than budget ones"),
            ("🌆 Tier-2 Opportunity", "Cities like Indore & Lucknow: lower competition, growing demand"),
            ("🍛 North Indian Rules", "Most popular cuisine across all 15 cities by restaurant count"),
        ]
        for title, desc in insights:
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-title">{title}</div>
                <div class="insight-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)

    with t3c2:
        st.markdown('<div class="section-header">💰 Price Category Breakdown</div>', unsafe_allow_html=True)
        price_stats = df_f.groupby('Price_Category').agg(
            Count=('Restaurant_Name', 'count'),
            Avg_Rating=('Rating', 'mean')
        ).reset_index().round(2)
        fig = px.bar(price_stats, x='Price_Category', y='Count',
                     color='Avg_Rating', color_continuous_scale='RdYlGn',
                     text='Count',
                     template='plotly_dark')
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0)
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="section-header">📈 Online Order Impact</div>', unsafe_allow_html=True)
        online_stats = df_f.groupby('Online_Order').agg(
            Avg_Rating=('Rating', 'mean'),
            Avg_Votes=('Votes', 'mean')
        ).reset_index().round(2)
        fig2 = px.bar(online_stats, x='Online_Order', y='Avg_Votes',
                      color='Online_Order',
                      color_discrete_map={'Yes': '#E23744', 'No': '#4a4a7a'},
                      text='Avg_Votes',
                      template='plotly_dark',
                      labels={'Online_Order': 'Online Order', 'Avg_Votes': 'Avg Votes'})
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        fig2.update_traces(textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)

# ════════════════════════════════════════════════════════
# TAB 4 — TOP RESTAURANTS
# ════════════════════════════════════════════════════════
with tab4:
    st.markdown("<br>", unsafe_allow_html=True)

    t4c1, t4c2 = st.columns(2)

    with t4c1:
        st.markdown('<div class="section-header">🏆 Top 10 Highest Rated</div>', unsafe_allow_html=True)
        top_rated = df_f[df_f['Votes'] >= 50].nlargest(10, 'Rating')[
            ['Restaurant_Name', 'City', 'Rating', 'Cost_For_Two', 'Votes']
        ].reset_index(drop=True)
        top_rated.index += 1
        st.dataframe(top_rated, use_container_width=True)

    with t4c2:
        st.markdown('<div class="section-header">💎 Top 10 Best Value-for-Money</div>', unsafe_allow_html=True)
        top_value = df_f[df_f['Votes'] > 50].nlargest(10, 'Value_Score')[
            ['Restaurant_Name', 'City', 'Rating', 'Cost_For_Two', 'Value_Score']
        ].reset_index(drop=True)
        top_value.index += 1
        st.dataframe(top_value, use_container_width=True)

    st.markdown('<div class="section-header">📊 Top 10 Most Voted Restaurants</div>', unsafe_allow_html=True)
    top_votes = df_f.nlargest(10, 'Votes')[
        ['Restaurant_Name', 'City', 'Area', 'Rating', 'Cost_For_Two', 'Votes', 'Online_Order']
    ].reset_index(drop=True)
    top_votes.index += 1

    fig = px.bar(top_votes, x='Restaurant_Name', y='Votes',
                 color='Rating', color_continuous_scale='RdYlGn',
                 hover_data=['City', 'Rating', 'Cost_For_Two'],
                 template='plotly_dark')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_tickangle=-30,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built by <strong style="color:#E23744">SELVAKUMAR</strong> — 
    Data Analyst Portfolio Project &nbsp;|&nbsp;
    <a href="https://github.com/SELVAKUMAR-ANALYST/zomato-analytics" target="_blank">GitHub</a>
    &nbsp;|&nbsp; Python · Pandas · Plotly · Streamlit · SQL
</div>
""", unsafe_allow_html=True)
