import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="GenAuto-SDV Studio | Tata Elxsi TELIPORT",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- World-Class Premium CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ===== GLOBAL ===== */
    .stApp {
        background: linear-gradient(160deg, #050810 0%, #0a0e1a 30%, #0d1220 60%, #080c15 100%);
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Hide Streamlit menu + footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        background: rgba(5,8,16,0.85);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(0,229,255,0.06);
    }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #080c18 0%, #0d1225 40%, #111830 100%);
        border-right: 1px solid rgba(0,229,255,0.08);
    }
    [data-testid="stSidebar"] .stRadio > div {
        gap: 2px;
    }
    [data-testid="stSidebar"] .stRadio label {
        padding: 8px 12px;
        border-radius: 8px;
        transition: all 0.2s ease;
        font-size: 0.92em;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(0,229,255,0.06);
    }
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] {
        background: linear-gradient(90deg, rgba(0,229,255,0.12), rgba(0,229,255,0.04));
        border-left: 3px solid #00e5ff;
    }
    
    /* ===== TYPOGRAPHY ===== */
    h1 {
        font-family: 'Inter', sans-serif !important;
        color: #e6edf3 !important;
        font-weight: 800 !important;
        font-size: 2em !important;
        letter-spacing: -0.5px !important;
    }
    h2 {
        color: #c9d1d9 !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px !important;
    }
    h3 {
        color: #b0bec5 !important;
        font-weight: 600 !important;
        font-size: 1.15em !important;
        letter-spacing: -0.2px !important;
    }
    p, li, span, label, .stMarkdown {
        color: #c9d1d9;
    }

    /* ===== METRICS (Glassmorphism) ===== */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(15,20,35,0.8), rgba(20,28,45,0.6));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0,229,255,0.1);
        padding: 14px 18px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.03);
        transition: all 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        border-color: rgba(0,229,255,0.25);
        box-shadow: 0 6px 30px rgba(0,229,255,0.08), inset 0 1px 0 rgba(255,255,255,0.05);
        transform: translateY(-2px);
    }
    div[data-testid="metric-container"] label {
        color: #6e7681 !important;
        font-weight: 500 !important;
        font-size: 0.82em !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.3em !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
        font-size: 0.8em !important;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #0d3b66 0%, #1565c0 100%);
        color: white;
        border: 1px solid rgba(0,229,255,0.15);
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.92em;
        padding: 0.55rem 1.6rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 12px rgba(13,59,102,0.4);
        letter-spacing: 0.3px;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1565c0 0%, #1e88e5 100%);
        box-shadow: 0 6px 25px rgba(21,101,192,0.5);
        transform: translateY(-2px);
        border-color: rgba(0,229,255,0.3);
    }
    .stButton > button:active {
        transform: translateY(0px);
    }
    button[kind="primary"] {
        background: linear-gradient(135deg, #1a6b3c 0%, #238636 50%, #2ea043 100%) !important;
        border: 1px solid rgba(46,160,67,0.3) !important;
        box-shadow: 0 2px 12px rgba(35,134,54,0.4) !important;
    }
    button[kind="primary"]:hover {
        box-shadow: 0 6px 25px rgba(35,134,54,0.5) !important;
    }

    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 3px;
        background: linear-gradient(90deg, rgba(15,20,30,0.9), rgba(20,25,40,0.9));
        border-radius: 12px;
        padding: 5px;
        border: 1px solid rgba(0,229,255,0.06);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: #6e7681;
        font-weight: 500;
        font-size: 0.88em;
        padding: 8px 16px;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #c9d1d9;
        background: rgba(0,229,255,0.05);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0,229,255,0.12), rgba(0,229,255,0.06)) !important;
        color: #00e5ff !important;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,229,255,0.1);
    }
    
    /* ===== CODE BLOCKS ===== */
    .stCodeBlock {
        border-radius: 12px !important;
        border: 1px solid rgba(0,229,255,0.06) !important;
    }
    code {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.88em;
    }

    /* ===== EXPANDERS ===== */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, rgba(15,20,30,0.8), rgba(20,25,40,0.6)) !important;
        border: 1px solid rgba(0,229,255,0.06);
        border-radius: 10px !important;
        color: #c9d1d9 !important;
        font-weight: 500;
    }
    .streamlit-expanderHeader:hover {
        border-color: rgba(0,229,255,0.15);
    }
    
    /* ===== BANNER ===== */
    .brand-banner {
        padding: 16px 28px;
        background: linear-gradient(135deg, #0a1628 0%, #0d2137 30%, #0f2d4a 60%, #0a2540 100%);
        border: 1px solid rgba(0,229,255,0.12);
        border-radius: 14px;
        margin-bottom: 24px;
        text-align: center;
        font-weight: 700;
        font-size: 1.05em;
        color: #e6edf3;
        letter-spacing: 1px;
        text-transform: uppercase;
        box-shadow: 0 4px 30px rgba(0,40,80,0.4), inset 0 1px 0 rgba(255,255,255,0.04);
        position: relative;
        overflow: hidden;
    }
    .brand-banner::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0,229,255,0.04), transparent);
        animation: shimmer 4s infinite;
    }
    @keyframes shimmer {
        0% { transform: translateX(-50%); }
        100% { transform: translateX(50%); }
    }

    /* ===== STATUS BADGES ===== */
    .badge-pass {
        background: linear-gradient(90deg, #1a6b3c, #238636);
        color: white; padding: 4px 12px; border-radius: 20px;
        font-size: 0.82em; font-weight: 600; letter-spacing: 0.3px;
        box-shadow: 0 2px 8px rgba(35,134,54,0.3);
    }
    .badge-fail {
        background: linear-gradient(90deg, #8b1a1a, #da3633);
        color: white; padding: 4px 12px; border-radius: 20px;
        font-size: 0.82em; font-weight: 600;
    }
    
    /* ===== CUSTOM CARDS ===== */
    .info-card {
        background: linear-gradient(135deg, rgba(15,20,35,0.7), rgba(20,28,45,0.5));
        backdrop-filter: blur(8px);
        border: 1px solid rgba(0,229,255,0.08);
        border-radius: 14px;
        padding: 20px;
        margin: 8px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    .info-card:hover {
        border-color: rgba(0,229,255,0.2);
        box-shadow: 0 6px 25px rgba(0,229,255,0.06);
    }

    /* ===== DIVIDERS ===== */
    hr {
        border-color: rgba(0,229,255,0.06) !important;
        margin: 20px 0 !important;
    }

    /* ===== SELECT BOX ===== */
    .stSelectbox div[data-baseweb="select"] > div {
        background: rgba(15,20,35,0.8);
        border-color: rgba(0,229,255,0.1);
        border-radius: 10px;
    }
    .stSelectbox div[data-baseweb="select"] > div:hover {
        border-color: rgba(0,229,255,0.25);
    }
    
    /* ===== MULTISELECT ===== */
    .stMultiSelect div[data-baseweb="select"] > div {
        background: rgba(15,20,35,0.8);
        border-color: rgba(0,229,255,0.1);
        border-radius: 10px;
    }
    
    /* ===== TEXT INPUT ===== */
    .stTextArea textarea, .stTextInput input {
        background: rgba(15,20,35,0.8) !important;
        border-color: rgba(0,229,255,0.1) !important;
        border-radius: 10px !important;
        color: #c9d1d9 !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: rgba(0,229,255,0.3) !important;
        box-shadow: 0 0 15px rgba(0,229,255,0.08) !important;
    }

    /* ===== PROGRESS BAR ===== */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00e5ff, #00bfa5) !important;
        border-radius: 6px;
    }

    /* ===== ALERT BOXES ===== */
    .stSuccess {
        background: linear-gradient(90deg, rgba(26,107,60,0.15), rgba(35,134,54,0.08)) !important;
        border-left: 3px solid #238636 !important;
        border-radius: 8px !important;
    }
    .stInfo {
        background: linear-gradient(90deg, rgba(13,59,102,0.15), rgba(21,101,192,0.08)) !important;
        border-left: 3px solid #1565c0 !important;
        border-radius: 8px !important;
    }
    .stWarning {
        background: linear-gradient(90deg, rgba(210,153,34,0.12), rgba(210,153,34,0.05)) !important;
        border-left: 3px solid #d29922 !important;
        border-radius: 8px !important;
    }
    
    /* ===== DOWNLOAD BUTTON ===== */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #0d3b66, #1565c0) !important;
        border: 1px solid rgba(0,229,255,0.2) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 12px rgba(13,59,102,0.4) !important;
    }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0a0e1a; }
    ::-webkit-scrollbar-thumb { background: rgba(0,229,255,0.15); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(0,229,255,0.25); }

    /* ===== SIDEBAR LOGO AREA ===== */
    .sidebar-logo {
        text-align: center;
        padding: 5px 0 10px 0;
    }
    .sidebar-logo h2 {
        background: linear-gradient(135deg, #00e5ff, #00bfa5, #69f0ae);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.5em !important;
        margin: 0 !important;
        letter-spacing: -0.5px !important;
    }
    .sidebar-version {
        font-size: 0.7em;
        color: #4a5568;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 2px;
    }
    
    /* ===== ANIMATED LIVE DOT ===== */
    .live-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #00ff88;
        margin-right: 6px;
        animation: pulse 1.5s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; box-shadow: 0 0 4px #00ff88; }
        50% { opacity: 0.4; box-shadow: 0 0 10px #00ff88; }
    }

    /* ===== PLOTLY CHART CONTAINER ===== */
    .stPlotlyChart {
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# --- LLM Engine Registry ---
LLM_ENGINES = {
    "Claude 3 Haiku (Anthropic)": {
        "provider": "anthropic",
        "model_id": "claude-3-haiku-20240307",
        "env_key": "ANTHROPIC_API_KEY",
        "speed": "⚡ Fast",
        "cost": "Reliable",
    },
    "Llama 3.3 70B (Groq)": {
        "provider": "groq",
        "model_id": "llama-3.3-70b-versatile",
        "env_key": "GROQ_API_KEY",
        "speed": "⚡⚡⚡ Ultra Fast",
        "cost": "Free (30 RPM)",
    },
    "Llama 4 Scout (Groq)": {
        "provider": "groq",
        "model_id": "meta-llama/llama-4-scout-17b-16e-instruct",
        "env_key": "GROQ_API_KEY",
        "speed": "⚡⚡ Fast",
        "cost": "Free (30 RPM)",
    },
}

COMPLIANCE_STANDARDS = {
    "MISRA C++:2023": "Latest MISRA C++ guidelines for safety-critical automotive software.",
    "MISRA C:2012": "C-language safety standard for embedded automotive ECU software.",
    "AUTOSAR C++14": "AUTOSAR Adaptive Platform coding guidelines (SOME/IP, ara::com).",
}

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h2>GenAuto-SDV</h2>
        <div class="sidebar-version">Studio v2.0</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
<div style="text-align:center;padding:6px 0;">
    <span style="background:linear-gradient(90deg,#1a6b3c,#238636);color:white;padding:3px 10px;border-radius:12px;font-size:0.75em;font-weight:600;">
        <span class="live-dot"></span> TEAM GREENBYTES — DTU
    </span>
</div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    selected_page = st.radio(
        "Navigate",
        ["🧠 AI Development Studio", "📊 Vehicle Health Dashboard", "📈 KPI & Benchmarks", "🔄 OTA & Subscriptions"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.divider()
    
    st.markdown("##### ⚙️ Configuration")
    
    llm_model = st.selectbox("LLM Engine", list(LLM_ENGINES.keys()), index=0)
    engine_info = LLM_ENGINES[llm_model]
    st.caption(f"{engine_info['speed']} | {engine_info['cost']}")
    
    target_lang = st.multiselect("Target Languages", ["C++14", "Kotlin", "Rust", "Python"], default=["C++14", "Kotlin", "Rust"])
    
    compliance = st.selectbox("Compliance Standard", list(COMPLIANCE_STANDARDS.keys()))
    st.caption(COMPLIANCE_STANDARDS[compliance])
    
    st.divider()
    
    # Active service indicator
    service_ctx = st.session_state.get('generated_service', None)
    if service_ctx:
        st.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(26,107,60,0.2),rgba(35,134,54,0.1));
border:1px solid rgba(35,134,54,0.3);border-radius:10px;padding:10px;text-align:center;">
    <small style="color:#6e7681;text-transform:uppercase;letter-spacing:1px;font-size:0.7em;">Active Service</small><br>
    <b style="color:#00ff88;font-size:0.9em;">{service_ctx['name'][:22]}</b><br>
    <small style="color:#6e7681;">{service_ctx['compliance']}</small>
</div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
<div style="background:rgba(15,20,35,0.5);border:1px solid rgba(0,229,255,0.08);
border-radius:10px;padding:10px;text-align:center;">
    <small style="color:#4a5568;text-transform:uppercase;letter-spacing:1px;font-size:0.7em;">No Service Active</small><br>
    <small style="color:#6e7681;">Generate via AI Studio</small>
</div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("""
<div style="text-align:center;color:#4a5568;font-size:0.72em;line-height:1.6;">
    Built for<br>
    <b style="color:#00e5ff;font-size:1.1em;">TATA ELXSI TELIPORT</b><br>
    Season 3 — Round 2<br><br>
    <span style="color:#6e7681;">Case Study 2</span><br>
    Predictable Code Development<br>for SoA using GenAI
</div>
    """, unsafe_allow_html=True)

# --- Import and Route ---
from modules import ai_studio, dashboard, kpi_page, ota_page

if selected_page == "🧠 AI Development Studio":
    st.markdown('<div class="brand-banner">🧠 GenAI Development Studio — Requirement to Deployment Pipeline</div>', unsafe_allow_html=True)
    ai_studio.render(llm_model, LLM_ENGINES[llm_model], target_lang, compliance)

elif selected_page == "📊 Vehicle Health Dashboard":
    st.markdown('<div class="brand-banner">📊 Vehicle Health & Diagnostics — Connected Dashboard</div>', unsafe_allow_html=True)
    dashboard.render()

elif selected_page == "📈 KPI & Benchmarks":
    st.markdown('<div class="brand-banner">📈 Performance Benchmarks — GenAI vs Manual Development</div>', unsafe_allow_html=True)
    kpi_page.render()

elif selected_page == "🔄 OTA & Subscriptions":
    st.markdown('<div class="brand-banner">🔄 Over-The-Air Updates & Feature Subscription Store</div>', unsafe_allow_html=True)
    ota_page.render()

# --- Footer ---
st.divider()
st.markdown("""
<div style="display:flex;justify-content:space-between;padding:8px 0;color:#4a5568;font-size:0.76em;">
    <span>© 2026 Team Greenbytes — DTU Delhi</span>
    <span>GenAuto-SDV Studio v2.0</span>
    <span>Tata Elxsi TELIPORT Season 3</span>
</div>
""", unsafe_allow_html=True)
