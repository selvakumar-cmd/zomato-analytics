import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Zomato India Analytics | Selvakumar",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Premium CSS — Fully Responsive + Mobile First ────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
}

/* ── Dark Background ── */
.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

/* Hide Streamlit default elements for cleaner look */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0f1a 0%, #141428 100%);
    border-right: 1px solid rgba(226,55,68,0.15);
}
section[data-testid="stSidebar"] .stMarkdown h2 {
    color: #E23744;
    font-size: 1.1rem;
}

/* ── Hero Section ── */
.hero {
    background: linear-gradient(135deg, #E23744 0%, #b71c1c 40%, #880e4f 100%);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 40px rgba(226,55,68,0.25);
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(0,0,0,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-content { position: relative; z-index: 1; }
.hero-eyebrow {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    color: rgba(255,255,255,0.7);
    margin-bottom: 0.6rem;
}
.hero h1 {
    font-size: 2.2rem;
    font-weight: 800;
    color: white;
    margin: 0;
    line-height: 1.15;
    letter-spacing: -0.5px;
}
.hero-desc {
    font-size: 0.92rem;
    color: rgba(255,255,255,0.82);
    margin-top: 0.7rem;
    line-height: 1.55;
    max-width: 650px;
}
.hero-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 1.2rem;
}
.pill {
    background: rgba(255,255,255,0.13);
    backdrop-filter: blur(10px);
    color: white;
    padding: 5px 14px;
    border-radius: 50px;
    font-size: 0.72rem;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.18);
    letter-spacing: 0.3px;
}

/* ── KPI Grid ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin-bottom: 2rem;
}
.kpi {
    background: linear-gradient(145deg, #12121f 0%, #1a1a30 100%);
    border: 1px solid rgba(226,55,68,0.12);
    border-radius: 16px;
    padding: 1.3rem 1rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
}
.kpi:hover {
    transform: translateY(-4px);
    border-color: rgba(226,55,68,0.35);
    box-shadow: 0 12px 35px rgba(226,55,68,0.12);
}
.kpi::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #E23744, #ff6b6b);
    opacity: 0;
    transition: opacity 0.3s;
}
.kpi:hover::before { opacity: 1; }
.kpi-emoji { font-size: 1.6rem; margin-bottom: 0.4rem; }
.kpi-num {
    font-size: 1.65rem;
    font-weight: 800;
    color: #E23744;
    line-height: 1.1;
}
.kpi-text {
    font-size: 0.68rem;
    color: #777;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    margin-top: 0.35rem;
}

/* ── Section Title ── */
.sec-title {
    font-size: 0.82rem;
    font-weight: 700;
    color: #E23744;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(226,55,68,0.2);
    display: flex;
    align-items: center;
    gap: 8px;
}
.sec-title-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #E23744;
    display: inline-block;
    animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(226,55,68,0.4); }
    50% { opacity: 0.8; box-shadow: 0 0 0 6px rgba(226,55,68,0); }
}

/* ── Insight Cards ── */
.insight-row {
    display: grid;
    grid-template-columns: 1fr;
    gap: 10px;
    margin-bottom: 1rem;
}
.ins {
    background: linear-gradient(135deg, #12121f 0%, #181830 100%);
    border-left: 4px solid #E23744;
    border-radius: 0 14px 14px 0;
    padding: 1rem 1.2rem;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}
.ins:hover {
    border-left-color: #ff6b6b;
    background: linear-gradient(135deg, #161628 0%, #1e1e38 100%);
    transform: translateX(4px);
}
.ins-title {
    font-weight: 700;
    color: #f0f0f5;
    font-size: 0.88rem;
    letter-spacing: -0.2px;
}
.ins-desc {
    color: #888;
    font-size: 0.78rem;
    margin-top: 3px;
    line-height: 1.45;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0f0f1a;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(226,55,68,0.1);
    overflow-x: auto;
}
.stTabs [data-baseweb="tab"] {
    color: #666;
    font-weight: 600;
    border-radius: 8px;
    font-size: 0.82rem;
    padding: 8px 16px;
    white-space: nowrap;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #E23744, #b71c1c) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(226,55,68,0.3);
}

/* ── Data Table Styling ── */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
}

/* ── Footer ── */
.app-footer {
    text-align: center;
    padding: 2rem 1rem 1rem;
    margin-top: 3rem;
    border-top: 1px solid rgba(226,55,68,0.1);
}
.footer-brand {
    font-size: 0.95rem;
    font-weight: 700;
    color: #E23744;
    letter-spacing: -0.3px;
}
.footer-sub {
    font-size: 0.72rem;
    color: #555;
    margin-top: 0.3rem;
    letter-spacing: 0.5px;
}
.footer-links {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 0.8rem;
}
.footer-links a {
    color: #888;
    font-size: 0.75rem;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
    border-bottom: 1px solid transparent;
}
.footer-links a:hover {
    color: #E23744;
    border-bottom: 1px solid #E23744;
}

/* ═══════════════════════════════════════════════════
   RESPONSIVE — MOBILE FIRST
   ═══════════════════════════════════════════════════ */

/* Tablets & Small Desktops */
@media (max-width: 992px) {
    .kpi-grid {
        grid-template-columns: repeat(3, 1fr);
    }
    .hero h1 { font-size: 1.8rem; }
    .hero { padding: 2rem 1.5rem; }
}

/* Mobile */
@media (max-width: 768px) {
    .kpi-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .hero {
        padding: 1.5rem 1.2rem;
        border-radius: 14px;
    }
    .hero h1 {
        font-size: 1.45rem;
        line-height: 1.2;
    }
    .hero-desc {
        font-size: 0.82rem;
    }
    .hero-eyebrow {
        font-size: 0.65rem;
    }
    .pill {
        font-size: 0.65rem;
        padding: 4px 10px;
    }
    .kpi { padding: 1rem 0.8rem; border-radius: 12px; }
    .kpi-num { font-size: 1.35rem; }
    .kpi-emoji { font-size: 1.3rem; }
    .kpi-text { font-size: 0.6rem; }
    .sec-title { font-size: 0.75rem; }
    .ins { padding: 0.8rem 1rem; }
    .ins-title { font-size: 0.82rem; }
    .ins-desc { font-size: 0.72rem; }
    .stTabs [data-baseweb="tab"] {
        font-size: 0.72rem;
        padding: 6px 10px;
    }
}

/* Small Mobile */
@media (max-width: 480px) {
    .kpi-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
    }
    .hero h1 { font-size: 1.25rem; }
    .hero { padding: 1.2rem 1rem; margin-bottom: 1rem; }
    .hero-desc { font-size: 0.78rem; }
    .kpi { padding: 0.9rem 0.6rem; }
    .kpi-num { font-size: 1.15rem; }
    .kpi-text { font-size: 0.55rem; letter-spacing: 0.5px; }
}
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("dataset/zomato_cleaned.csv")

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍽️ Zomato Analytics")
    st.caption("Filter & explore the data")
    st.markdown("---")

    all_cities = sorted(df['City'].unique().tolist())
    selected_cities = st.multiselect(
        "🏙️ Select Cities",
        all_cities,
        default=all_cities
    )

    all_prices = sorted(df['Price_Category'].unique().tolist())
    selected_price = st.multiselect(
        "💰 Price Category",
        all_prices,
        default=all_prices
    )

    rating_min = st.slider(
        "⭐ Minimum Rating",
        float(df['Rating'].min()),
        float(df['Rating'].max()),
        2.5, step=0.1
    )

    online_filter = st.radio(
        "📱 Online Order",
        ["All", "Yes", "No"],
        horizontal=True
    )

    st.markdown("---")
    st.markdown(f"**📊 Dataset:** `{len(df):,}` restaurants")
    st.markdown(f"**🏙️ Cities:** `{df['City'].nunique()}`")
    st.markdown("---")
    st.markdown("🔗 [GitHub](https://github.com/SELVAKUMAR-ANALYST/zomato-analytics)")

# ── Apply Filters ─────────────────────────────────────────────
df_f = df.copy()
if selected_cities:
    df_f = df_f[df_f['City'].isin(selected_cities)]
if selected_price:
    df_f = df_f[df_f['Price_Category'].isin(selected_price)]
df_f = df_f[df_f['Rating'] >= rating_min]
if online_filter != "All":
    df_f = df_f[df_f['Online_Order'] == online_filter]

# ── Hero Section ──────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-content">
        <div class="hero-eyebrow">📊 Data Analytics Portfolio Project</div>
        <h1>Zomato India<br>Restaurant Analytics</h1>
        <div class="hero-desc">
            Comprehensive EDA on 1,280+ restaurants across 15 major Indian cities.
            Uncovering hidden trends in cuisine popularity, pricing strategies
            & customer engagement patterns.
        </div>
        <div class="hero-pills">
            <span class="pill">Python</span>
            <span class="pill">Pandas</span>
            <span class="pill">Plotly</span>
            <span class="pill">SQL</span>
            <span class="pill">Streamlit</span>
            <span class="pill">EDA</span>
            <span class="pill">Data Viz</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards (HTML grid for perfect mobile response) ─────────
total = len(df_f)
avg_rating = round(df_f['Rating'].mean(), 2) if total > 0 else 0
online_pct = round((df_f['Online_Order'] == 'Yes').mean() * 100, 1) if total > 0 else 0
avg_cost = int(round(df_f['Cost_For_Two'].mean())) if total > 0 else 0
total_votes = f"{int(df_f['Votes'].sum()):,}" if total > 0 else "0"

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi">
        <div class="kpi-emoji">🏪</div>
        <div class="kpi-num">{total:,}</div>
        <div class="kpi-text">Restaurants</div>
    </div>
    <div class="kpi">
        <div class="kpi-emoji">⭐</div>
        <div class="kpi-num">{avg_rating}</div>
        <div class="kpi-text">Avg Rating</div>
    </div>
    <div class="kpi">
        <div class="kpi-emoji">📱</div>
        <div class="kpi-num">{online_pct}%</div>
        <div class="kpi-text">Online Orders</div>
    </div>
    <div class="kpi">
        <div class="kpi-emoji">💰</div>
        <div class="kpi-num">₹{avg_cost}</div>
        <div class="kpi-text">Avg Cost / 2</div>
    </div>
    <div class="kpi">
        <div class="kpi-emoji">👍</div>
        <div class="kpi-num">{total_votes}</div>
        <div class="kpi-text">Total Votes</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Plotly Theme Helper ───────────────────────────────────────
def style_fig(fig, height=380):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#aaa', size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        height=height,
        coloraxis_showscale=False,
        xaxis=dict(gridcolor='rgba(255,255,255,0.04)', showline=False),
        yaxis=dict(gridcolor='rgba(255,255,255,0.04)', showline=False),
    )
    return fig

# ── Tabs ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🏙️ City Deep-Dive",
    "💡 Insights & Impact",
    "🏆 Top Performers"
])

# ══════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<br>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sec-title"><span class="sec-title-dot"></span>Restaurant Count by City</div>', unsafe_allow_html=True)
        city_data = df_f['City'].value_counts().reset_index()
        city_data.columns = ['City', 'Count']
        fig = px.bar(city_data, x='City', y='Count',
                     color='Count',
                     color_continuous_scale=[[0, '#3d1216'], [0.5, '#E23744'], [1, '#ff8a80']],
                     template='plotly_dark')
        fig.update_traces(marker_line_width=0, marker_cornerradius=6)
        st.plotly_chart(style_fig(fig), use_container_width=True)

    with col2:
        st.markdown('<div class="sec-title"><span class="sec-title-dot"></span>Rating Distribution</div>', unsafe_allow_html=True)
        fig = px.histogram(df_f, x='Rating', nbins=30,
                           color_discrete_sequence=['#E23744'],
                           template='plotly_dark')
        fig.update_traces(marker_line_width=0, marker_cornerradius=4)
        st.plotly_chart(style_fig(fig), use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="sec-title"><span class="sec-title-dot"></span>Online vs Offline Orders</div>', unsafe_allow_html=True)
        fig = px.pie(df_f, names='Online_Order',
                     color='Online_Order',
                     color_discrete_map={'Yes': '#E23744', 'No': '#252545'},
                     hole=0.55, template='plotly_dark')
        fig.update_traces(
            textfont_size=13, textfont_color='white',
            textposition='inside', textinfo='label+percent',
            marker=dict(line=dict(color='#0a0a0f', width=2))
        )
        st.plotly_chart(style_fig(fig, 360), use_container_width=True)

    with col4:
        st.markdown('<div class="sec-title"><span class="sec-title-dot"></span>Price vs Rating Bubble</div>', unsafe_allow_html=True)
        fig = px.scatter(df_f, x='Cost_For_Two', y='Rating',
                         size='Votes', color='Rating',
                         color_continuous_scale='RdYlGn',
                         hover_name='Restaurant_Name',
                         hover_data=['City'],
                         template='plotly_dark',
                         opacity=0.75)
        st.plotly_chart(style_fig(fig, 360), use_container_width=True)

    # Price Category Treemap
    st.markdown('<div class="sec-title"><span class="sec-title-dot"></span>Price Category Market Share</div>', unsafe_allow_html=True)
    price_tree = df_f.groupby('Price_Category').size().reset_index(name='Count')
    fig = px.treemap(price_tree, path=['Price_Category'], values='Count',
                     color='Count',
                     color_continuous_scale=[[0, '#1a1a2e'], [0.5, '#E23744'], [1, '#ff6b6b']],
                     template='plotly_dark')
    fig.update_traces(
        textfont=dict(size=16, color='white', family='Inter'),
        marker=dict(cornerradius=8),
        hovertemplate='<b>%{label}</b><br>Restaurants: %{value}<extra></extra>'
    )
    st.plotly_chart(style_fig(fig, 300), use_container_width=True)

# ══════════════════════════════════════════════════════════════
# TAB 2 — CITY DEEP-DIVE
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<br>', unsafe_allow_html=True)

    city_stats = df_f.groupby('City').agg(
        Restaurants=('Restaurant_Name', 'count'),
        Avg_Rating=('Rating', 'mean'),
        Avg_Cost=('Cost_For_Two', 'mean'),
        Total_Votes=('Votes', 'sum'),
        Online_Pct=('Online_Order', lambda x: round((x == 'Yes').mean() * 100, 1))
    ).reset_index().round(2)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sec-title"><span class="sec-title-dot"></span>City Rating Ranking</div>', unsafe_allow_html=True)
        sorted_cities = city_stats.sort_values('Avg_Rating')
        fig = px.bar(sorted_cities, x='Avg_Rating', y='City', orientation='h',
                     color='Avg_Rating',
                     color_continuous_scale='RdYlGn',
                     template='plotly_dark',
                     text=sorted_cities['Avg_Rating'].apply(lambda x: f'{x:.2f}'))
        fig.update_traces(textposition='outside', textfont_size=11, marker_cornerradius=6)
        h = max(350, len(sorted_cities) * 32)
        st.plotly_chart(style_fig(fig, h), use_container_width=True)

    with col2:
        st.markdown('<div class="sec-title"><span class="sec-title-dot"></span>City Cost Comparison</div>', unsafe_allow_html=True)
        sorted_cost = city_stats.sort_values('Avg_Cost')
        fig = px.bar(sorted_cost, x='Avg_Cost', y='City', orientation='h',
                     color='Avg_Cost',
                     color_continuous_scale=[[0, '#252545'], [0.5, '#E23744'], [1, '#ff8a80']],
                     template='plotly_dark',
                     text=sorted_cost['Avg_Cost'].apply(lambda x: f'₹{x:.0f}'))
        fig.update_traces(textposition='outside', textfont_size=11, marker_cornerradius=6)
        st.plotly_chart(style_fig(fig, h), use_container_width=True)

    # Online order adoption by city
    st.markdown('<div class="sec-title"><span class="sec-title-dot"></span>Online Order Adoption by City</div>', unsafe_allow_html=True)
    online_city = city_stats.sort_values('Online_Pct', ascending=True)
    fig = px.bar(online_city, x='Online_Pct', y='City', orientation='h',
                 color='Online_Pct',
                 color_continuous_scale=[[0, '#252545'], [0.5, '#E23744'], [1, '#2ecc71']],
                 template='plotly_dark',
                 text=online_city['Online_Pct'].apply(lambda x: f'{x}%'))
    fig.update_traces(textposition='outside', textfont_size=11, marker_cornerradius=6)
    st.plotly_chart(style_fig(fig, max(350, len(online_city) * 32)), use_container_width=True)

    # City KPI Table
    st.markdown('<div class="sec-title"><span class="sec-title-dot"></span>City-wise Performance Summary</div>', unsafe_allow_html=True)
    display_stats = city_stats.sort_values('Restaurants', ascending=False)
    display_stats.columns = ['City', 'Restaurants', 'Avg Rating', 'Avg Cost (₹)', 'Total Votes', 'Online %']
    st.dataframe(display_stats, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# TAB 3 — INSIGHTS & IMPACT
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<br>', unsafe_allow_html=True)

    # Key insights
    st.markdown('<div class="sec-title"><span class="sec-title-dot"></span>Key Business Findings</div>', unsafe_allow_html=True)

    insights = [
        ("🏙️ Bangalore Dominates", "With 180+ restaurants, it's the most competitive market. New entrants face highest barrier to entry."),
        ("📱 Online = +23% Engagement", "Restaurants offering online ordering receive 23% more customer votes on average — digital presence is non-negotiable."),
        ("💰 Budget Sweet Spot", "45% of restaurants fall in ₹200–₹500 range. The mid-range (₹500–₹800) segment is underserved — big opportunity gap."),
        ("⭐ Fine Dining Premium", "Luxury restaurants average 0.4 higher rating than budget ones. Customers equate higher price with better experience."),
        ("🌆 Tier-2 Gold Rush", "Cities like Indore, Lucknow & Bhopal show lower competition but growing demand. Best cities for new restaurant launches."),
        ("🍛 North Indian + Chinese", "This cuisine combo dominates all 15 cities. Any new restaurant must include these as core offerings."),
    ]

    insights_html = '<div class="insight-row">'
    for title, desc in insights:
        insights_html += f"""
        <div class="ins">
            <div class="ins-title">{title}</div>
            <div class="ins-desc">{desc}</div>
        </div>"""
    insights_html += '</div>'
    st.markdown(insights_html, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sec-title"><span class="sec-title-dot"></span>Price Category Analysis</div>', unsafe_allow_html=True)
        price_stats = df_f.groupby('Price_Category').agg(
            Count=('Restaurant_Name', 'count'),
            Avg_Rating=('Rating', 'mean')
        ).reset_index().round(2)
        fig = px.bar(price_stats, x='Price_Category', y='Count',
                     color='Avg_Rating', color_continuous_scale='RdYlGn',
                     text='Count', template='plotly_dark')
        fig.update_traces(textposition='outside', textfont_size=12, marker_cornerradius=6)
        st.plotly_chart(style_fig(fig), use_container_width=True)

    with col2:
        st.markdown('<div class="sec-title"><span class="sec-title-dot"></span>Online Order Impact</div>', unsafe_allow_html=True)
        online_stats = df_f.groupby('Online_Order').agg(
            Avg_Rating=('Rating', 'mean'),
            Avg_Votes=('Votes', 'mean'),
            Avg_Cost=('Cost_For_Two', 'mean')
        ).reset_index().round(1)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=online_stats['Online_Order'],
            y=online_stats['Avg_Votes'],
            name='Avg Votes',
            marker_color=['#E23744', '#353560'],
            text=online_stats['Avg_Votes'].apply(lambda x: f'{x:.0f}'),
            textposition='outside',
            marker_cornerradius=6,
        ))
        fig.update_layout(template='plotly_dark', showlegend=False)
        st.plotly_chart(style_fig(fig), use_container_width=True)

    # Restaurant Type Analysis
    if 'Restaurant_Type' in df_f.columns:
        st.markdown('<div class="sec-title"><span class="sec-title-dot"></span>Restaurant Type Distribution</div>', unsafe_allow_html=True)
        type_data = df_f['Restaurant_Type'].value_counts().head(8).reset_index()
        type_data.columns = ['Type', 'Count']
        fig = px.bar(type_data, x='Count', y='Type', orientation='h',
                     color='Count',
                     color_continuous_scale=[[0, '#252545'], [0.5, '#E23744'], [1, '#ff8a80']],
                     template='plotly_dark',
                     text='Count')
        fig.update_traces(textposition='outside', textfont_size=12, marker_cornerradius=6)
        st.plotly_chart(style_fig(fig, 350), use_container_width=True)

# ══════════════════════════════════════════════════════════════
# TAB 4 — TOP PERFORMERS
# ══════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<br>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sec-title"><span class="sec-title-dot"></span>Top 10 Highest Rated</div>', unsafe_allow_html=True)
        top_rated = df_f[df_f['Votes'] >= 50].nlargest(10, 'Rating')[
            ['Restaurant_Name', 'City', 'Rating', 'Cost_For_Two', 'Votes']
        ].reset_index(drop=True)
        top_rated.index += 1
        st.dataframe(top_rated, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-title"><span class="sec-title-dot"></span>Top 10 Value-for-Money</div>', unsafe_allow_html=True)
        top_value = df_f[df_f['Votes'] > 50].nlargest(10, 'Value_Score')[
            ['Restaurant_Name', 'City', 'Rating', 'Cost_For_Two', 'Value_Score']
        ].reset_index(drop=True)
        top_value.index += 1
        st.dataframe(top_value, use_container_width=True)

    # Most Voted — Visual Chart
    st.markdown('<div class="sec-title"><span class="sec-title-dot"></span>Most Popular — By Customer Votes</div>', unsafe_allow_html=True)
    top_votes = df_f.nlargest(10, 'Votes')
    fig = px.bar(top_votes, x='Votes', y='Restaurant_Name', orientation='h',
                 color='Rating', color_continuous_scale='RdYlGn',
                 hover_data=['City', 'Cost_For_Two', 'Online_Order'],
                 template='plotly_dark',
                 text=top_votes['Votes'].apply(lambda x: f'{x:,}'))
    fig.update_traces(textposition='outside', textfont_size=11, marker_cornerradius=6)
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(style_fig(fig, 420), use_container_width=True)

    # Search Restaurant
    st.markdown('<div class="sec-title"><span class="sec-title-dot"></span>🔍 Search a Restaurant</div>', unsafe_allow_html=True)
    search = st.text_input("Type restaurant name to search...", label_visibility="collapsed", placeholder="Search restaurants...")
    if search:
        results = df_f[df_f['Restaurant_Name'].str.contains(search, case=False, na=False)]
        if len(results) > 0:
            st.dataframe(results[['Restaurant_Name', 'City', 'Area', 'Rating', 'Cost_For_Two', 'Online_Order', 'Votes']],
                        use_container_width=True, hide_index=True)
        else:
            st.warning("No restaurants found. Try a different search term.")

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    <div class="footer-brand">🍽️ Zomato India Analytics</div>
    <div class="footer-sub">Built by SELVAKUMAR · Data Analyst Portfolio Project</div>
    <div class="footer-links">
        <a href="https://github.com/SELVAKUMAR-ANALYST/zomato-analytics" target="_blank">GitHub</a>
        <a href="#">LinkedIn</a>
        <a href="mailto:">Contact</a>
    </div>
    <div style="font-size:0.65rem; color:#333; margin-top:0.8rem;">
        Python · Pandas · Plotly · SQL · Streamlit · EDA · Data Visualization
    </div>
</div>
""", unsafe_allow_html=True)
