import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import base64
import os

# ── Helper for Image Base64 ───────────────────────────────────
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""


# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Zomato Tamil Nadu Analytics | Selvakumar",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════
# GOD LEVEL CSS — Premium Dark + Glassmorphism + Animations
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
}

/* ── Hide defaults ── */
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display: none !important; }

/* ── Animated Background ── */
.stApp {
    background: #06060c;
    color: #e8e8f0;
}
.stApp::before {
    content: '';
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(226,55,68,0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(120,40,200,0.04) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 80%, rgba(226,55,68,0.03) 0%, transparent 50%);
    animation: bg-shift 20s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: -1;
}
@keyframes bg-shift {
    0% { transform: translate(0, 0) rotate(0deg); }
    100% { transform: translate(-3%, -3%) rotate(2deg); }
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #08080f 0%, #0d0d1a 100%);
    border-right: 1px solid rgba(226,55,68,0.08);
    backdrop-filter: blur(20px);
}

/* ── HERO — Animated Gradient Border ── */
.hero-wrap {
    padding: 2px;
    border-radius: 22px;
    background: linear-gradient(135deg, #E23744, #ff6b6b, #E23744, #880e4f);
    background-size: 300% 300%;
    animation: gradient-border 6s ease infinite;
    margin-bottom: 2rem;
    box-shadow: 0 0 60px rgba(226,55,68,0.15), 0 0 120px rgba(226,55,68,0.05);
}
@keyframes gradient-border {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.hero {
    background: linear-gradient(135deg, #0c0c16 0%, #121220 100%);
    border-radius: 20px;
    padding: 2.8rem 2.2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -80px;
    right: -80px;
    width: 350px;
    height: 350px;
    background: radial-gradient(circle, rgba(226,55,68,0.12) 0%, transparent 70%);
    border-radius: 50%;
    animation: float 8s ease-in-out infinite;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -60px;
    left: -40px;
    width: 250px;
    height: 250px;
    background: radial-gradient(circle, rgba(120,40,200,0.08) 0%, transparent 70%);
    border-radius: 50%;
    animation: float 10s ease-in-out infinite reverse;
}
@keyframes float {
    0%, 100% { transform: translate(0, 0); }
    50% { transform: translate(-15px, -20px); }
}
.hero-content { position: relative; z-index: 2; }
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: #E23744;
    margin-bottom: 0.8rem;
    background: rgba(226,55,68,0.08);
    padding: 5px 14px;
    border-radius: 50px;
    border: 1px solid rgba(226,55,68,0.15);
}
.hero-dot {
    width: 6px; height: 6px;
    background: #E23744;
    border-radius: 50%;
    animation: pulse-glow 2s infinite;
}
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 0 0 rgba(226,55,68,0.6); }
    50% { box-shadow: 0 0 0 6px rgba(226,55,68,0); }
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 900;
    color: white;
    margin: 0;
    line-height: 1.1;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #ffffff 0%, #cccccc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero h1 span {
    background: linear-gradient(135deg, #E23744 0%, #ff6b6b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-desc {
    font-size: 0.9rem;
    color: rgba(255,255,255,0.55);
    margin-top: 0.8rem;
    line-height: 1.6;
    max-width: 600px;
    font-weight: 400;
}
.hero-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    margin-top: 1.4rem;
}
.pill {
    background: rgba(226,55,68,0.08);
    backdrop-filter: blur(10px);
    color: rgba(255,255,255,0.75);
    padding: 6px 14px;
    border-radius: 50px;
    font-size: 0.7rem;
    font-weight: 600;
    border: 1px solid rgba(226,55,68,0.12);
    transition: all 0.3s;
    letter-spacing: 0.3px;
}
.pill:hover {
    background: rgba(226,55,68,0.18);
    border-color: rgba(226,55,68,0.35);
    color: white;
    transform: translateY(-2px);
}

/* ── KPI Grid — Glass Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin-bottom: 2.2rem;
}
.kpi {
    background: rgba(14,14,26,0.7);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(226,55,68,0.08);
    border-radius: 18px;
    padding: 1.4rem 1rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.4,0,0.2,1);
}
.kpi::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, #E23744, transparent);
    opacity: 0;
    transition: opacity 0.4s;
}
.kpi:hover {
    transform: translateY(-6px);
    border-color: rgba(226,55,68,0.25);
    box-shadow: 0 20px 50px rgba(226,55,68,0.1), 0 0 30px rgba(226,55,68,0.05);
}
.kpi:hover::before { opacity: 1; }
.kpi-emoji {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0 2px 8px rgba(226,55,68,0.2));
}
.kpi-num {
    font-size: 1.75rem;
    font-weight: 800;
    background: linear-gradient(135deg, #E23744 0%, #ff6b6b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.kpi-text {
    font-size: 0.62rem;
    color: rgba(255,255,255,0.35);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 700;
    margin-top: 0.4rem;
}

/* ── Section Title — Animated ── */
.sec-title {
    font-size: 0.78rem;
    font-weight: 700;
    color: #E23744;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 1.2rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(226,55,68,0.12);
    display: flex;
    align-items: center;
    gap: 10px;
}
.sec-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #E23744;
    display: inline-block;
    animation: pulse-glow 2s infinite;
    box-shadow: 0 0 10px rgba(226,55,68,0.4);
}

/* ── Insight Cards — Glass ── */
.ins {
    background: rgba(14,14,26,0.6);
    backdrop-filter: blur(12px);
    border-left: 3px solid #E23744;
    border-radius: 0 14px 14px 0;
    padding: 1.1rem 1.3rem;
    margin-bottom: 10px;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    position: relative;
}
.ins:hover {
    border-left-color: #ff6b6b;
    transform: translateX(6px);
    background: rgba(20,20,38,0.8);
    box-shadow: -4px 0 20px rgba(226,55,68,0.08);
}
.ins-num {
    position: absolute;
    top: 10px;
    right: 14px;
    font-size: 2rem;
    font-weight: 900;
    color: rgba(226,55,68,0.07);
    line-height: 1;
}
.ins-title {
    font-weight: 700;
    color: #f0f0f5;
    font-size: 0.88rem;
}
.ins-desc {
    color: rgba(255,255,255,0.45);
    font-size: 0.78rem;
    margin-top: 4px;
    line-height: 1.5;
}

/* ── Tabs — Premium ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(10,10,18,0.8);
    border-radius: 14px;
    padding: 5px;
    gap: 5px;
    border: 1px solid rgba(226,55,68,0.08);
    overflow-x: auto;
    backdrop-filter: blur(10px);
}
.stTabs [data-baseweb="tab"] {
    color: rgba(255,255,255,0.35);
    font-weight: 600;
    border-radius: 10px;
    font-size: 0.8rem;
    padding: 10px 18px;
    white-space: nowrap;
    transition: all 0.3s;
}
.stTabs [data-baseweb="tab"]:hover {
    color: rgba(255,255,255,0.6);
    background: rgba(226,55,68,0.05);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #E23744, #c0392b) !important;
    color: white !important;
    box-shadow: 0 6px 20px rgba(226,55,68,0.3);
}

/* ── Download Button ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #E23744, #c0392b) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.3s !important;
    box-shadow: 0 4px 15px rgba(226,55,68,0.25) !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(226,55,68,0.35) !important;
}

/* ── Footer ── */
.app-footer {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    margin-top: 3rem;
    border-top: 1px solid rgba(226,55,68,0.08);
    position: relative;
}
.app-footer::before {
    content: '';
    position: absolute;
    top: -1px;
    left: 20%;
    right: 20%;
    height: 1px;
    background: linear-gradient(90deg, transparent, #E23744, transparent);
}
.footer-brand {
    font-size: 1.1rem;
    font-weight: 800;
    background: linear-gradient(135deg, #E23744, #ff6b6b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.footer-sub {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.3);
    margin-top: 0.4rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-weight: 500;
}
.footer-links {
    display: flex;
    justify-content: center;
    gap: 24px;
    margin-top: 1rem;
}
.footer-links a {
    color: rgba(255,255,255,0.4);
    font-size: 0.75rem;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s;
    padding-bottom: 2px;
    border-bottom: 1px solid transparent;
}
.footer-links a:hover {
    color: #E23744;
    border-bottom-color: #E23744;
}
.footer-tech {
    font-size: 0.6rem;
    color: rgba(255,255,255,0.15);
    margin-top: 1rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ── Hero Split Layout ── */
.hero-layout {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 2.2rem;
}
.hero-content {
    flex: 1.4;
    position: relative;
    z-index: 2;
}
.hero-image-container {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    z-index: 2;
}
.hero-img {
    width: 100%;
    max-width: 320px;
    border-radius: 16px;
    border: 2px solid rgba(226,55,68,0.25);
    box-shadow: 0 10px 30px rgba(226,55,68,0.2), 0 0 40px rgba(226,55,68,0.1);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.hero-img:hover {
    transform: scale(1.03) rotate(1deg);
    border-color: rgba(226,55,68,0.5);
    box-shadow: 0 15px 40px rgba(226,55,68,0.35), 0 0 50px rgba(226,55,68,0.2);
}

/* ═══ RESPONSIVE ═══ */
@media (max-width: 992px) {
    .kpi-grid { grid-template-columns: repeat(3, 1fr); }
    .hero h1 { font-size: 2rem; }
    .hero { padding: 2rem 1.5rem; }
    .hero-img { max-width: 260px; }
}
@media (max-width: 768px) {
    .kpi-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
    .hero { padding: 1.5rem 1.2rem; }
    .hero h1 { font-size: 1.5rem; letter-spacing: -0.5px; }
    .hero-desc { font-size: 0.82rem; }
    .hero-eyebrow { font-size: 0.58rem; letter-spacing: 2px; }
    .pill { font-size: 0.62rem; padding: 4px 10px; }
    .kpi { padding: 1rem 0.7rem; border-radius: 14px; }
    .kpi-num { font-size: 1.35rem; }
    .kpi-emoji { font-size: 1.2rem; }
    .kpi-text { font-size: 0.55rem; }
    .sec-title { font-size: 0.7rem; letter-spacing: 1.5px; }
    .ins { padding: 0.9rem 1rem; }
    .ins-title { font-size: 0.82rem; }
    .stTabs [data-baseweb="tab"] { font-size: 0.7rem; padding: 7px 12px; }
    
    /* Hero layout stack on mobile */
    .hero-layout {
        flex-direction: column;
        gap: 1.5rem;
        text-align: center;
    }
    .hero-img {
        max-width: 220px;
    }
    .hero-pills {
        justify-content: center;
    }
}
@media (max-width: 480px) {
    .kpi-grid { grid-template-columns: repeat(2, 1fr); gap: 8px; }
    .hero h1 { font-size: 1.25rem; }
    .hero { padding: 1.2rem 1rem; }
    .hero-wrap { margin-bottom: 1.2rem; }
    .kpi { padding: 0.8rem 0.5rem; }
    .kpi-num { font-size: 1.1rem; }
    .kpi-text { font-size: 0.5rem; letter-spacing: 0.8px; }
    .pill { font-size: 0.58rem; padding: 3px 8px; }
    .hero-img {
        max-width: 180px;
    }
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
    st.markdown("## 🍽️ Filters")
    st.caption("Customize the dashboard view")
    st.markdown("---")

    all_cities = sorted(df['City'].unique().tolist())
    selected_cities = st.multiselect("🏙️ Cities", all_cities, default=all_cities)

    all_prices = sorted(df['Price_Category'].unique().tolist())
    selected_price = st.multiselect("💰 Price Segment", all_prices, default=all_prices)

    rating_min = st.slider("⭐ Min Rating", float(df['Rating'].min()), float(df['Rating'].max()), 2.5, step=0.1)

    online_filter = st.radio("📱 Online Order", ["All", "Yes", "No"], horizontal=True)

    st.markdown("---")
    st.caption(f"📊 {len(df):,} restaurants · {df['City'].nunique()} cities")
    st.markdown("[🔗 GitHub Repo](https://github.com/SELVAKUMAR-ANALYST/zomato-analytics)")

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
img_base64 = get_base64_image("hermione_analyst.jpg")

st.markdown(f"""
<div class="hero-wrap">
<div class="hero">
    <div class="hero-layout">
        <div class="hero-content">
            <div class="hero-eyebrow"><span class="hero-dot"></span> Tamil Nadu Food Analytics</div>
            <h1>Zomato Tamil Nadu<br><span>Restaurant Analytics</span></h1>
            <div class="hero-desc">
                Comprehensive exploratory data analysis on 1,260+ restaurants across
                12 major cities in Tamil Nadu — uncovering trends in pricing, customer engagement,
                cuisine popularity & local market opportunities.
            </div>
            <div class="hero-pills">
                <span class="pill">Python</span>
                <span class="pill">Pandas</span>
                <span class="pill">Plotly</span>
                <span class="pill">SQL</span>
                <span class="pill">Streamlit</span>
                <span class="pill">EDA</span>
                <span class="pill">Data Viz</span>
                <span class="pill">Statistics</span>
            </div>
        </div>
        <div class="hero-image-container">
            <img src="data:image/jpeg;base64,{img_base64}" class="hero-img" alt="Hermione Granger Data Scientist">
        </div>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────
total = len(df_f)
avg_rating = round(df_f['Rating'].mean(), 2) if total > 0 else 0
online_pct = round((df_f['Online_Order'] == 'Yes').mean() * 100, 1) if total > 0 else 0
avg_cost = int(round(df_f['Cost_For_Two'].mean())) if total > 0 else 0
total_votes = f"{int(df_f['Votes'].sum()):,}" if total > 0 else "0"

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi"><div class="kpi-emoji">🏪</div><div class="kpi-num">{total:,}</div><div class="kpi-text">Restaurants</div></div>
    <div class="kpi"><div class="kpi-emoji">⭐</div><div class="kpi-num">{avg_rating}</div><div class="kpi-text">Avg Rating</div></div>
    <div class="kpi"><div class="kpi-emoji">📱</div><div class="kpi-num">{online_pct}%</div><div class="kpi-text">Online Orders</div></div>
    <div class="kpi"><div class="kpi-emoji">💰</div><div class="kpi-num">₹{avg_cost}</div><div class="kpi-text">Avg Cost / 2</div></div>
    <div class="kpi"><div class="kpi-emoji">👍</div><div class="kpi-num">{total_votes}</div><div class="kpi-text">Total Votes</div></div>
</div>
""", unsafe_allow_html=True)

# ── Chart Theme Helper ────────────────────────────────────────
def style_fig(fig, height=380):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#666', size=11),
        margin=dict(l=10, r=10, t=30, b=10),
        height=height,
        coloraxis_showscale=False,
        xaxis=dict(gridcolor='rgba(255,255,255,0.03)', showline=False, zeroline=False),
        yaxis=dict(gridcolor='rgba(255,255,255,0.03)', showline=False, zeroline=False),
    )
    return fig

ZOMATO_REDS = [[0, '#1a0a0c'], [0.3, '#4a1520'], [0.6, '#E23744'], [1, '#ff8a80']]

# ── Tabs ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "🏙️ City Deep-Dive",
    "🍛 Cuisine Analysis",
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
        st.markdown('<div class="sec-title"><span class="sec-dot"></span>Restaurant Count by City</div>', unsafe_allow_html=True)
        city_data = df_f['City'].value_counts().reset_index()
        city_data.columns = ['City', 'Count']
        fig = px.bar(city_data, x='City', y='Count', color='Count',
                     color_continuous_scale=ZOMATO_REDS, template='plotly_dark')
        fig.update_traces(marker_line_width=0, marker_cornerradius=6)
        st.plotly_chart(style_fig(fig), use_container_width=True)

    with col2:
        st.markdown('<div class="sec-title"><span class="sec-dot"></span>Rating Distribution</div>', unsafe_allow_html=True)
        fig = px.histogram(df_f, x='Rating', nbins=30,
                           color_discrete_sequence=['#E23744'], template='plotly_dark')
        fig.update_traces(marker_line_width=0, marker_cornerradius=4)
        st.plotly_chart(style_fig(fig), use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="sec-title"><span class="sec-dot"></span>Online vs Offline</div>', unsafe_allow_html=True)
        fig = px.pie(df_f, names='Online_Order', color='Online_Order',
                     color_discrete_map={'Yes': '#E23744', 'No': '#1a1a30'},
                     hole=0.6, template='plotly_dark')
        fig.update_traces(
            textfont=dict(size=13, color='white'), textposition='inside',
            textinfo='label+percent',
            marker=dict(line=dict(color='#06060c', width=3))
        )
        st.plotly_chart(style_fig(fig, 350), use_container_width=True)

    with col4:
        st.markdown('<div class="sec-title"><span class="sec-dot"></span>Price vs Rating Bubble</div>', unsafe_allow_html=True)
        fig = px.scatter(df_f, x='Cost_For_Two', y='Rating', size='Votes',
                         color='Rating', color_continuous_scale='RdYlGn',
                         hover_name='Restaurant_Name', hover_data=['City'],
                         template='plotly_dark', opacity=0.7)
        st.plotly_chart(style_fig(fig, 350), use_container_width=True)

    # Treemap
    st.markdown('<div class="sec-title"><span class="sec-dot"></span>Price Category Market Share</div>', unsafe_allow_html=True)
    price_tree = df_f.groupby('Price_Category').size().reset_index(name='Count')
    fig = px.treemap(price_tree, path=['Price_Category'], values='Count',
                     color='Count', color_continuous_scale=ZOMATO_REDS,
                     template='plotly_dark')
    fig.update_traces(
        textfont=dict(size=16, color='white', family='Inter'),
        marker=dict(cornerradius=8),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'
    )
    st.plotly_chart(style_fig(fig, 280), use_container_width=True)

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
        st.markdown('<div class="sec-title"><span class="sec-dot"></span>City Rating Ranking</div>', unsafe_allow_html=True)
        s = city_stats.sort_values('Avg_Rating')
        fig = px.bar(s, x='Avg_Rating', y='City', orientation='h',
                     color='Avg_Rating', color_continuous_scale='RdYlGn',
                     template='plotly_dark',
                     text=s['Avg_Rating'].apply(lambda x: f'{x:.2f}'))
        fig.update_traces(textposition='outside', textfont_size=11, marker_cornerradius=6)
        h = max(380, len(s) * 34)
        st.plotly_chart(style_fig(fig, h), use_container_width=True)

    with col2:
        st.markdown('<div class="sec-title"><span class="sec-dot"></span>City Cost Comparison</div>', unsafe_allow_html=True)
        s = city_stats.sort_values('Avg_Cost')
        fig = px.bar(s, x='Avg_Cost', y='City', orientation='h',
                     color='Avg_Cost', color_continuous_scale=ZOMATO_REDS,
                     template='plotly_dark',
                     text=s['Avg_Cost'].apply(lambda x: f'₹{x:.0f}'))
        fig.update_traces(textposition='outside', textfont_size=11, marker_cornerradius=6)
        st.plotly_chart(style_fig(fig, h), use_container_width=True)

    # Online adoption
    st.markdown('<div class="sec-title"><span class="sec-dot"></span>Online Order Adoption %</div>', unsafe_allow_html=True)
    s = city_stats.sort_values('Online_Pct', ascending=True)
    fig = px.bar(s, x='Online_Pct', y='City', orientation='h',
                 color='Online_Pct',
                 color_continuous_scale=[[0, '#1a1a30'], [0.5, '#E23744'], [1, '#2ecc71']],
                 template='plotly_dark',
                 text=s['Online_Pct'].apply(lambda x: f'{x}%'))
    fig.update_traces(textposition='outside', textfont_size=11, marker_cornerradius=6)
    st.plotly_chart(style_fig(fig, h), use_container_width=True)

    # Table
    st.markdown('<div class="sec-title"><span class="sec-dot"></span>Performance Summary</div>', unsafe_allow_html=True)
    d = city_stats.sort_values('Restaurants', ascending=False).copy()
    d.columns = ['City', 'Restaurants', 'Avg Rating', 'Avg Cost (₹)', 'Total Votes', 'Online %']
    st.dataframe(d, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# TAB 3 — CUISINE ANALYSIS (NEW!)
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<br>', unsafe_allow_html=True)

    # Parse cuisines
    @st.cache_data
    def get_cuisine_data(data):
        cuisines_split = data['Cuisines'].dropna().str.split(',').explode().str.strip()
        cuisine_counts = cuisines_split.value_counts().head(15).reset_index()
        cuisine_counts.columns = ['Cuisine', 'Count']
        return cuisine_counts, cuisines_split

    cuisine_counts, all_cuisines = get_cuisine_data(df_f)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sec-title"><span class="sec-dot"></span>Top 15 Most Popular Cuisines</div>', unsafe_allow_html=True)
        fig = px.bar(cuisine_counts, x='Count', y='Cuisine', orientation='h',
                     color='Count', color_continuous_scale=ZOMATO_REDS,
                     template='plotly_dark',
                     text='Count')
        fig.update_traces(textposition='outside', textfont_size=11, marker_cornerradius=6)
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(style_fig(fig, 480), use_container_width=True)

    with col2:
        st.markdown('<div class="sec-title"><span class="sec-dot"></span>Cuisine Market Share</div>', unsafe_allow_html=True)
        top8 = cuisine_counts.head(8)
        fig = px.pie(top8, names='Cuisine', values='Count', hole=0.5,
                     color_discrete_sequence=px.colors.sequential.Reds_r,
                     template='plotly_dark')
        fig.update_traces(
            textfont=dict(size=11, color='white'), textposition='inside',
            textinfo='label+percent',
            marker=dict(line=dict(color='#06060c', width=2))
        )
        st.plotly_chart(style_fig(fig, 480), use_container_width=True)

    # Cuisine by city heatmap
    st.markdown('<div class="sec-title"><span class="sec-dot"></span>Top Cuisines × City Heatmap</div>', unsafe_allow_html=True)
    top_cuisines_list = cuisine_counts.head(8)['Cuisine'].tolist()
    cuisine_expanded = df_f.dropna(subset=['Cuisines']).copy()
    cuisine_expanded['Cuisine_List'] = cuisine_expanded['Cuisines'].str.split(',')
    cuisine_expanded = cuisine_expanded.explode('Cuisine_List')
    cuisine_expanded['Cuisine_List'] = cuisine_expanded['Cuisine_List'].str.strip()
    cuisine_city = cuisine_expanded[cuisine_expanded['Cuisine_List'].isin(top_cuisines_list)]
    heatmap_data = cuisine_city.groupby(['City', 'Cuisine_List']).size().reset_index(name='Count')
    heatmap_pivot = heatmap_data.pivot_table(index='City', columns='Cuisine_List', values='Count', fill_value=0)

    fig = px.imshow(heatmap_pivot,
                    color_continuous_scale=ZOMATO_REDS,
                    template='plotly_dark',
                    aspect='auto',
                    labels=dict(color='Restaurants'))
    fig.update_layout(
        xaxis_title='', yaxis_title='',
        xaxis=dict(side='top', tickangle=-30),
    )
    st.plotly_chart(style_fig(fig, max(350, len(heatmap_pivot) * 30)), use_container_width=True)

    # Correlation Heatmap
    st.markdown('<div class="sec-title"><span class="sec-dot"></span>📊 Correlation Heatmap</div>', unsafe_allow_html=True)
    numeric_cols = ['Rating', 'Votes', 'Cost_For_Two', 'Value_Score']
    corr_matrix = df_f[numeric_cols].corr().round(2)
    fig = px.imshow(corr_matrix,
                    text_auto=True,
                    color_continuous_scale=[[0, '#1a1a30'], [0.5, '#4a1520'], [1, '#E23744']],
                    template='plotly_dark',
                    aspect='auto')
    fig.update_layout(xaxis_title='', yaxis_title='')
    fig.update_traces(textfont=dict(size=14, color='white'))
    st.plotly_chart(style_fig(fig, 380), use_container_width=True)

# ══════════════════════════════════════════════════════════════
# TAB 4 — INSIGHTS & IMPACT
# ══════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<br>', unsafe_allow_html=True)

    st.markdown('<div class="sec-title"><span class="sec-dot"></span>Key Business Findings</div>', unsafe_allow_html=True)

    insights = [
        ("🏙️ Chennai Market Saturation", "300+ restaurants — highest competition. New entrants face maximum barrier to entry here."),
        ("📱 Online Order Traction", "Restaurants with online ordering get +25% higher customer engagement and vote volumes in TN."),
        ("💰 Mid-Range Gold Sweetspot", "40% of market is affordable/mid-range (₹300–₹600). Premium segment is growing rapidly in Coimbatore."),
        ("⭐ Fine Dining Premium", "Fine dining restaurants average 0.5 higher ratings. Tamil Nadu customers highly value premium hospitality."),
        ("🌆 Tier-2 Growth Opportunities", "Madurai, Trichy, and Salem show low competition + high value scores. Best cities for local food startups."),
        ("🍛 South Indian & Chettinad Dominance", "This culinary combination dominates all 12 cities, followed closely by Fast Food & Biryani."),
    ]

    ins_html = ""
    for i, (title, desc) in enumerate(insights, 1):
        ins_html += f"""<div class="ins"><div class="ins-num">0{i}</div><div class="ins-title">{title}</div><div class="ins-desc">{desc}</div></div>"""
    st.markdown(ins_html, unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sec-title"><span class="sec-dot"></span>Price Category Analysis</div>', unsafe_allow_html=True)
        ps = df_f.groupby('Price_Category').agg(
            Count=('Restaurant_Name', 'count'),
            Avg_Rating=('Rating', 'mean')
        ).reset_index().round(2)
        fig = px.bar(ps, x='Price_Category', y='Count', color='Avg_Rating',
                     color_continuous_scale='RdYlGn', text='Count', template='plotly_dark')
        fig.update_traces(textposition='outside', textfont_size=12, marker_cornerradius=6)
        st.plotly_chart(style_fig(fig), use_container_width=True)

    with col2:
        st.markdown('<div class="sec-title"><span class="sec-dot"></span>Online Order Impact</div>', unsafe_allow_html=True)
        os_data = df_f.groupby('Online_Order').agg(
            Avg_Votes=('Votes', 'mean'),
            Avg_Rating=('Rating', 'mean')
        ).reset_index().round(1)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=os_data['Online_Order'], y=os_data['Avg_Votes'], name='Avg Votes',
            marker_color=['#E23744', '#1a1a30'],
            text=os_data['Avg_Votes'].apply(lambda x: f'{x:.0f}'),
            textposition='outside', marker_cornerradius=6))
        fig.update_layout(template='plotly_dark', showlegend=False)
        st.plotly_chart(style_fig(fig), use_container_width=True)

    # Restaurant Type
    if 'Restaurant_Type' in df_f.columns:
        st.markdown('<div class="sec-title"><span class="sec-dot"></span>Restaurant Type Distribution</div>', unsafe_allow_html=True)
        td = df_f['Restaurant_Type'].value_counts().head(8).reset_index()
        td.columns = ['Type', 'Count']
        fig = px.bar(td, x='Count', y='Type', orientation='h', color='Count',
                     color_continuous_scale=ZOMATO_REDS, template='plotly_dark', text='Count')
        fig.update_traces(textposition='outside', textfont_size=11, marker_cornerradius=6)
        st.plotly_chart(style_fig(fig, 340), use_container_width=True)

# ══════════════════════════════════════════════════════════════
# TAB 5 — TOP PERFORMERS
# ══════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<br>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sec-title"><span class="sec-dot"></span>Top 10 Highest Rated</div>', unsafe_allow_html=True)
        tr = df_f[df_f['Votes'] >= 50].nlargest(10, 'Rating')[
            ['Restaurant_Name', 'City', 'Rating', 'Cost_For_Two', 'Votes']
        ].reset_index(drop=True)
        tr.index += 1
        st.dataframe(tr, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-title"><span class="sec-dot"></span>Top 10 Value-for-Money</div>', unsafe_allow_html=True)
        tv = df_f[df_f['Votes'] > 50].nlargest(10, 'Value_Score')[
            ['Restaurant_Name', 'City', 'Rating', 'Cost_For_Two', 'Value_Score']
        ].reset_index(drop=True)
        tv.index += 1
        st.dataframe(tv, use_container_width=True)

    # Most Voted Chart
    st.markdown('<div class="sec-title"><span class="sec-dot"></span>Most Popular by Votes</div>', unsafe_allow_html=True)
    top_v = df_f.nlargest(10, 'Votes')
    fig = px.bar(top_v, x='Votes', y='Restaurant_Name', orientation='h',
                 color='Rating', color_continuous_scale='RdYlGn',
                 hover_data=['City', 'Cost_For_Two'], template='plotly_dark',
                 text=top_v['Votes'].apply(lambda x: f'{x:,}'))
    fig.update_traces(textposition='outside', textfont_size=11, marker_cornerradius=6)
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(style_fig(fig, 420), use_container_width=True)

    # Search
    st.markdown('<div class="sec-title"><span class="sec-dot"></span>🔍 Search Restaurant</div>', unsafe_allow_html=True)
    search = st.text_input("Search...", label_visibility="collapsed", placeholder="Type restaurant name...")
    if search:
        res = df_f[df_f['Restaurant_Name'].str.contains(search, case=False, na=False)]
        if len(res) > 0:
            st.dataframe(res[['Restaurant_Name', 'City', 'Area', 'Rating', 'Cost_For_Two', 'Online_Order', 'Votes']],
                        use_container_width=True, hide_index=True)
        else:
            st.warning("No restaurants found.")

    # Download CSV
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title"><span class="sec-dot"></span>📥 Export Data</div>', unsafe_allow_html=True)
    col_dl1, col_dl2, col_dl3 = st.columns(3)
    with col_dl1:
        csv_filtered = df_f.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_filtered,
            file_name="zomato_filtered_data.csv",
            mime="text/csv"
        )
    with col_dl2:
        csv_full = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Full Dataset (CSV)",
            data=csv_full,
            file_name="zomato_full_data.csv",
            mime="text/csv"
        )

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    <div class="footer-brand">🍽️ Zomato India Analytics</div>
    <div class="footer-sub">Built by Selvakumar · Data Analyst Portfolio Project</div>
    <div class="footer-links">
        <a href="https://github.com/SELVAKUMAR-ANALYST/zomato-analytics" target="_blank">GitHub</a>
        <a href="#">LinkedIn</a>
        <a href="#">Resume</a>
    </div>
    <div class="footer-tech">Python · Pandas · NumPy · Plotly · SQL · Streamlit · EDA · Data Visualization</div>
</div>
""", unsafe_allow_html=True)
