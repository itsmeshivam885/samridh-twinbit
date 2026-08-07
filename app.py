import streamlit as st
import pandas as pd
import datetime
import os
import time
import base64
import plotly.express as px
import plotly.graph_objects as bg

# ==============================================================================
# 1. PAGE CONFIGURATION & ENTERPRISE DESIGN SYSTEM (WCAG 2.2 / MATERIAL 3)
# ==============================================================================
st.set_page_config(
    page_title="SAMRIDH | National AI Crop Analytics & PMFBY Visual Portal",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Design System — Glassmorphism, Motion, Government Branding
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Manrope:wght@400;600;700;800&family=Poppins:wght@500;600;700;800&display=swap');

    /* ---------- Global Design Tokens ---------- */
    :root {
        --primary: #2563EB;
        --primary-dark: #1D4ED8;
        --primary-light: #60A5FA;
        --secondary: #0F172A;
        --success: #22C55E;
        --success-dark: #15803D;
        --warning: #F59E0B;
        --danger: #EF4444;
        --accent: #14B8A6;
        --purple: #8B5CF6;
        --bg-main: #F8FAFC;
        --card-bg: #FFFFFF;
        --text-main: #111827;
        --text-muted: #64748B;
        --border-color: #E2E8F0;
        --glass-bg: rgba(255, 255, 255, 0.72);
        --glass-border: rgba(226, 232, 240, 0.8);
        --shadow-sm: 0 1px 2px 0 rgba(15, 23, 42, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(15, 23, 42, 0.1), 0 2px 4px -1px rgba(15, 23, 42, 0.06);
        --shadow-lg: 0 10px 20px -4px rgba(15, 23, 42, 0.15), 0 4px 8px -3px rgba(15, 23, 42, 0.08);
        --shadow-glow: 0 0 0 4px rgba(37, 99, 235, 0.12);
        --radius-lg: 20px;
        --radius-md: 14px;
        --radius-sm: 10px;
    }

    /* ---------- Base Reset ---------- */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp {
        background:
            radial-gradient(circle at 8% 0%, rgba(37,99,235,0.06) 0%, transparent 45%),
            radial-gradient(circle at 95% 12%, rgba(20,184,166,0.06) 0%, transparent 40%),
            var(--bg-main);
        color: var(--text-main);
    }
    #MainMenu, footer, header[data-testid="stHeader"] { background: transparent; }
    .block-container { padding-top: 1.2rem; max-width: 1300px; }

    /* ---------- Theme-Lock ---------- */
    html { color-scheme: light; }
    .stApp, .stApp * { color: var(--text-main); }
    [data-testid="stAppViewContainer"], [data-testid="stMain"],
    section[data-testid="stSidebar"], div[data-testid="stForm"] { color-scheme: light; }
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * { color: var(--text-muted) !important; }
    [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span, [data-testid="stText"] { color: var(--text-main); }
    [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label { color: var(--text-main) !important; }
    div[data-testid="stJson"], div[data-testid="stJson"] * { color: var(--text-main) !important; }
    div[data-testid="stDataFrame"] * , div[data-testid="stTable"] * { color: var(--text-main) !important; }

    ::-webkit-scrollbar { width: 9px; height: 9px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 20px; }
    ::-webkit-scrollbar-thumb:hover { background: #94A3B8; }

    /* ---------- Keyframes ---------- */
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(14px);} to { opacity: 1; transform: translateY(0);} }
    @keyframes fadeIn { from { opacity: 0;} to { opacity: 1;} }
    @keyframes gradientFlow { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    @keyframes pulseDot { 0% { box-shadow: 0 0 0 0 rgba(34,197,94,0.55);} 70% { box-shadow: 0 0 0 8px rgba(34,197,94,0);} 100% { box-shadow: 0 0 0 0 rgba(34,197,94,0);} }
    @keyframes floatSlow { 0%,100% { transform: translateY(0);} 50% { transform: translateY(-6px);} }
    @keyframes scanline { 0% { top: -10%; } 100% { top: 110%; } }

    .fade-up { animation: fadeInUp 0.55s cubic-bezier(0.16, 1, 0.3, 1) both; }
    .fade-in { animation: fadeIn 0.6s ease both; }

    /* ---------- Government Utility Bar ---------- */
    .gov-utility-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 10px;
        background: #0B1F3A;
        color: #E2E8F0;
        padding: 6px 22px;
        font-size: 0.74rem;
        font-weight: 500;
        border-radius: 8px 8px 0 0;
    }
    .gov-utility-bar a, .gov-utility-bar .util-btn {
        color: #CBD5E1;
        text-decoration: none;
        margin-right: 14px;
        cursor: default;
    }
    .gov-utility-bar .util-btn {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 5px;
        padding: 1px 8px;
        font-size: 0.7rem;
        font-weight: 700;
        margin-right: 6px;
    }
    .gov-utility-left, .gov-utility-right { display: flex; align-items: center; flex-wrap: wrap; }

    /* ---------- Animated Tricolor Accent ---------- */
    .tricolor-bar {
        height: 5px;
        width: 100%;
        border-radius: 6px;
        background: linear-gradient(90deg, #FF9933 0%, #FF9933 33.3%, #FFFFFF 33.3%, #FFFFFF 66.6%, #138808 66.6%, #138808 100%);
        background-size: 200% 100%;
        animation: gradientFlow 6s ease infinite;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        margin-bottom: 16px;
    }

    /* ---------- Sticky Glass Hero Header ---------- */
    .gov-hero-header {
        position: sticky;
        top: 0.4rem;
        z-index: 999;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.97) 0%, rgba(29, 58, 130, 0.95) 55%, rgba(20, 100, 130, 0.93) 100%);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 22px 30px;
        border-radius: var(--radius-lg);
        color: #FFFFFF;
        box-shadow: var(--shadow-lg);
        margin-bottom: 22px;
        transition: box-shadow 0.35s ease, transform 0.35s ease;
    }
    .gov-hero-header:hover {
        box-shadow: 0 16px 34px -6px rgba(20, 184, 166, 0.35), var(--shadow-lg);
        transform: translateY(-2px);
    }

    .gov-chip {
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.28);
        color: #F8FAFC;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        backdrop-filter: blur(6px);
    }

    .hero-title {
        margin: 12px 0 6px 0;
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 2.5rem;
        letter-spacing: -0.02em;
        line-height: 1.15;
    }
    .hero-title .hindi-part {
        color: #FFFFFF;
        text-shadow: 0 2px 14px rgba(0,0,0,0.35);
    }
    .hero-title .brand-part {
        background: linear-gradient(90deg, #FFA940 0%, #FFD873 30%, #5EEAD4 65%, #38BDF8 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        color: #FFD873;
        animation: gradientFlow 5s ease infinite;
        filter: drop-shadow(0 2px 10px rgba(94, 234, 212, 0.35));
    }
    .hero-subtitle {
        margin: 0;
        color: #7DD3FC;
        font-weight: 700;
        font-size: 1.06rem;
        letter-spacing: 0.01em;
    }
    .hero-caption {
        margin-top: 8px;
        color: rgba(226, 232, 240, 0.82);
        font-size: 0.83rem;
        font-weight: 500;
    }
    .scheme-ribbon {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: center;
        margin-top: 14px;
    }
    .scheme-chip {
        background: rgba(255, 255, 255, 0.10);
        border: 1px solid rgba(255, 255, 255, 0.22);
        color: #E2E8F0;
        padding: 5px 13px;
        border-radius: 50px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        backdrop-filter: blur(4px);
    }

    /* ---------- Premium Cards ---------- */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 22px 26px;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    }
    .glass-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }

    .session-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F0FDF4 120%);
        border-left: 4px solid var(--success);
        padding: 16px 22px;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-sm);
        margin-bottom: 22px;
        animation: fadeInUp 0.5s ease both;
    }

    /* ---------- Metric Cards ---------- */
    .metric-card-wrapper {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 18px 20px;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.5s ease both;
    }
    .metric-card-wrapper::before {
        content: "";
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 4px;
        background: var(--accent-color, var(--primary));
        border-radius: 0 4px 4px 0;
    }
    .metric-card-wrapper:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-md);
        border-color: var(--accent-color, var(--primary));
    }
    .metric-icon { font-size: 1.4rem; opacity: 0.9; }
    .metric-title {
        font-size: 0.78rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 6px;
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: var(--text-main);
        margin: 4px 0 0 0;
        font-family: 'Manrope', sans-serif;
    }
    .metric-delta { font-size: 0.8rem; font-weight: 700; margin-left: 6px; }

    /* ---------- Status Badges ---------- */
    .badge-status {
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.76rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 5px;
        letter-spacing: 0.02em;
        white-space: nowrap;
    }
    .badge-approved { background-color: #DCFCE7; color: #15803D; border: 1px solid #86EFAC; }
    .badge-pending  { background-color: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
    .badge-rejected { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }
    .badge-fraud    { background-color: #F3E8FF; color: #6B21A8; border: 1px solid #E9D5FF; }
    .badge-verified { background-color: #DBEAFE; color: #1D4ED8; border: 1px solid #BFDBFE; }

    /* ---------- Buttons ---------- */
    div.stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: #FFFFFF !important;
        border: none;
        border-radius: var(--radius-sm);
        padding: 11px 26px;
        font-weight: 700;
        font-size: 0.94rem;
        letter-spacing: 0.01em;
        box-shadow: 0 3px 8px rgba(37, 99, 235, 0.28);
        transition: all 0.22s cubic-bezier(0.4,0,0.2,1);
    }
    div.stButton > button:hover, .stFormSubmitButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.35), var(--shadow-glow);
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
    }

    /* ---------- Form Cards ---------- */
    div[data-testid="stForm"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #FAFBFF 100%);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 28px 30px 18px 30px;
        box-shadow: var(--shadow-md);
        animation: fadeInUp 0.5s ease both;
    }

    /* ---------- Inputs ---------- */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stDateInput>div>div>input,
    .stSelectbox>div>div>div,
    .stTextArea>div>div>textarea {
        border-radius: var(--radius-sm) !important;
        border: 1.5px solid var(--border-color) !important;
        background-color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%) !important;
        border-right: 1px solid var(--border-color);
    }
    section[data-testid="stSidebar"] .stRadio label {
        background: #FFFFFF;
        border: 1px solid var(--border-color);
        border-radius: var(--radius-sm);
        padding: 10px 14px !important;
        margin-bottom: 8px;
        display: flex;
        width: 100%;
        transition: all 0.2s ease;
        font-weight: 600;
        font-size: 0.86rem;
    }

    .sidebar-section-title {
        margin: 4px 0 10px 0;
        color: var(--text-main);
        font-size: 1.02rem;
        font-weight: 800;
        font-family: 'Poppins', sans-serif;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .sidebar-caption { margin: -6px 0 14px 0; color: var(--text-muted); font-size: 0.78rem; }

    .profile-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        border-radius: var(--radius-md);
        padding: 16px 18px;
        color: #FFFFFF;
        margin-bottom: 16px;
        box-shadow: var(--shadow-md);
    }
    .profile-avatar {
        width: 42px; height: 42px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--accent), var(--primary));
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; font-size: 1.05rem; color: #FFF;
    }
    .status-dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: var(--success);
        display: inline-block;
        animation: pulseDot 1.8s infinite;
        margin-right: 6px;
    }
    .health-item {
        display: flex; align-items: center;
        font-size: 0.78rem; color: var(--text-muted);
        padding: 5px 0;
    }

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; border-bottom: 2px solid var(--border-color); }
    .stTabs [data-baseweb="tab"] {
        height: 46px;
        border-radius: 10px 10px 0 0;
        padding: 0 20px;
        font-weight: 700;
        font-size: 0.88rem;
        color: var(--text-muted);
        background-color: transparent;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        color: var(--primary) !important;
        border-bottom: 3px solid var(--primary) !important;
        background: linear-gradient(180deg, rgba(37,99,235,0.08), transparent) !important;
    }

    /* Custom HTML Table Styling */
    .premium-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: var(--radius-md);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
        margin: 16px 0;
        background: #FFFFFF;
    }
    .premium-table thead th {
        background: linear-gradient(135deg, #0F172A, #1E3A8A);
        color: #FFFFFF; text-align: left; padding: 12px 16px;
        font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em;
    }
    .premium-table tbody td {
        padding: 12px 16px;
        font-size: 0.86rem;
        border-bottom: 1px solid var(--border-color);
        color: var(--text-main);
    }
    .premium-table tbody tr:hover { background: rgba(37, 99, 235, 0.05); }
    .premium-table tbody tr:last-child td { border-bottom: none; }

    /* ---------- AI Scan Effect ---------- */
    .ai-scan-box {
        position: relative;
        overflow: hidden;
        border-radius: var(--radius-md);
        border: 1px solid var(--border-color);
        background: linear-gradient(135deg, #0F172A, #1E293B);
        padding: 24px;
        color: #E2E8F0;
        margin: 14px 0;
    }

    /* ---------- Footer ---------- */
    .footer-box {
        text-align: center;
        padding: 26px 20px 18px 20px;
        color: var(--text-muted);
        font-size: 0.85rem;
        border-top: 1px solid var(--border-color);
        margin-top: 36px;
    }
    .footer-links { margin-top: 10px; display: flex; justify-content: center; gap: 18px; flex-wrap: wrap; }
    .footer-links a { color: var(--primary); text-decoration: none; font-weight: 600; font-size: 0.8rem; }
    .footer-badges { display: flex; justify-content: center; gap: 8px; margin-top: 12px; flex-wrap: wrap; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SHARED SESSION STATE DATA (EXACT UNTOUCHED BACKEND LOGIC)
# ==============================================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "claims_db" not in st.session_state:
    st.session_state.claims_db = [
        {
            "Claim_ID": "CLM-2026-8812",
            "Farmer_Name": "Ramesh Kumar",
            "Village": "Kalyanpur (Kanpur Nagar)",
            "Crop": "Wheat (गेहूँ)",
            "Area": "2.5 Acres",
            "Loss_Type": "Flood Inundation",
            "Loss_Date": "2026-02-28",
            "Reported_Damage_Pct": 65,
            "AI_SegFormer_Loss_Pct": 62.4,
            "NDVI_Drop_Pct": -34.5,
            "Weather_Event": "IMD 112mm Precipitation Logged",
            "Edge_Blur_Score": 142.5,
            "pHash_Match": "PASSED (Unique Image)",
            "GPS_Geofence": "PASSED (Inside Cadastral Plot 18B)",
            "Status": "Pending Review",
            "AI_Confidence": "94.8% High Confidence Genuine"
        },
        {
            "Claim_ID": "CLM-2026-8813",
            "Farmer_Name": "Suresh Singh",
            "Village": "Bitis (Kanpur Nagar)",
            "Crop": "Mustard (सरसों)",
            "Area": "1.8 Acres",
            "Loss_Type": "Hailstorm Damage",
            "Loss_Date": "2026-02-25",
            "Reported_Damage_Pct": 40,
            "AI_SegFormer_Loss_Pct": 41.2,
            "NDVI_Drop_Pct": -28.0,
            "Weather_Event": "IMD Local Hailstorm Alert",
            "Edge_Blur_Score": 188.0,
            "pHash_Match": "PASSED (Unique Image)",
            "GPS_Geofence": "PASSED (Inside Cadastral Plot 04A)",
            "Status": "Approved",
            "AI_Confidence": "91.2% High Confidence Genuine"
        },
        {
            "Claim_ID": "CLM-2026-9001",
            "Farmer_Name": "Amit Patel",
            "Village": "Rania (Kanpur Nagar)",
            "Crop": "Paddy (धान)",
            "Area": "3.0 Acres",
            "Loss_Type": "Crop Lodging",
            "Loss_Date": "2026-02-20",
            "Reported_Damage_Pct": 80,
            "AI_SegFormer_Loss_Pct": 12.0,
            "NDVI_Drop_Pct": -3.1,
            "Weather_Event": "Normal Weather (No Rain/Storm)",
            "Edge_Blur_Score": 45.2,
            "pHash_Match": "FAILED 🚨 (Duplicate Hash Detected)",
            "GPS_Geofence": "FAILED 🚨 (12.4 km Outside Boundary)",
            "Status": "Rejected",
            "AI_Confidence": "12.4% Fraud Alert Flagged"
        }
    ]

# ==============================================================================
# 3. ENTERPRISE HERO HEADER BANNER
# ==============================================================================
def _img_data_uri(path):
    try:
        if not os.path.exists(path):
            return None
        ext = os.path.splitext(path)[1].lower().replace(".", "")
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/{mime};base64,{encoded}"
    except Exception:
        return None

def _find_logo(*candidate_paths):
    for p in candidate_paths:
        uri = _img_data_uri(p)
        if uri:
            return uri
    return None

samridh_logo_uri = _find_logo(os.path.join("images", "samridh_logo.png"), "samridh_logo.png")
twinbit_logo_uri = _find_logo(
    os.path.join("images", "twinbit_logo.jpeg"),
    os.path.join("images", "twinbit_logo.jpg"),
    "twinbit_logo.jpeg",
    "twinbit_logo.jpg"
)

samridh_logo_html = (
    f'<img src="{samridh_logo_uri}" style="width:110px; height:110px; object-fit:contain; border-radius:16px; background:#FFFFFF; padding:6px; box-shadow: var(--shadow-md);">'
    if samridh_logo_uri else
    '<div style="font-size:3.2rem; text-align:center;">🌾</div>'
)
twinbit_logo_html = (
    f'<img src="{twinbit_logo_uri}" style="width:100px; height:100px; object-fit:contain; border-radius:16px; background:#FFFFFF; padding:6px; box-shadow: var(--shadow-md);">'
    if twinbit_logo_uri else
    '<div style="font-size:2.6rem; text-align:right;">⚡</div>'
)

st.markdown("""
    <div class="gov-utility-bar">
        <div class="gov-utility-left">
            <a>Skip to Main Content</a>
            <a>Screen Reader Access</a>
            <span class="util-btn">A-</span><span class="util-btn">A</span><span class="util-btn">A+</span>
        </div>
        <div class="gov-utility-right">
            <a>हिंदी | English</a>
            <a>Sitemap</a>
            <a>Helpline: 14447</a>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="tricolor-bar"></div>', unsafe_allow_html=True)

st.markdown(f"""
    <div class="gov-hero-header">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:20px; flex-wrap:wrap;">
            <div style="flex:0 0 auto;">{samridh_logo_html}</div>
            <div style="flex:1 1 auto; text-align:center; min-width:280px;">
                <div class="gov-chip">🇮🇳&nbsp; GOVERNMENT OF INDIA &nbsp;|&nbsp; MINISTRY OF AGRICULTURE &amp; FARMERS WELFARE</div>
                <div class="hero-title"><span class="hindi-part">समृद्ध</span> <span class="brand-part">SAMRIDH</span> <span class="hindi-part">PORTAL</span></div>
                <p class="hero-subtitle">AI-Based Real-Time Crop Visual Analytics &amp; Fraud-Resistant Loss Verification Platform</p>
                <p class="hero-caption">An Initiative under Pradhan Mantri Fasal Bima Yojana (PMFBY) &nbsp;•&nbsp; Developed &amp; Maintained by <b>Team TwinBit</b></p>
                <div class="scheme-ribbon">
                    <span class="scheme-chip">🌾 PMFBY</span>
                    <span class="scheme-chip">💰 PM-KISAN</span>
                    <span class="scheme-chip">🧪 Soil Health Card</span>
                    <span class="scheme-chip">🛰️ CROPIC Satellite Mission</span>
                    <span class="scheme-chip">🖥️ Digital India</span>
                    <span class="scheme-chip">🏦 Direct Benefit Transfer</span>
                </div>
            </div>
            <div style="flex:0 0 auto;">{twinbit_logo_html}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

twinbit_jpeg = os.path.join("images", "twinbit_logo.jpeg")
if not os.path.exists(twinbit_jpeg):
    _alt = os.path.join("images", "twinbit_logo.jpg")
    if os.path.exists(_alt):
        twinbit_jpeg = _alt

# ==============================================================================
# 4. SIDEBAR NAVIGATION & PORTAL SELECTOR
# ==============================================================================
st.sidebar.markdown("""
    <div class="sidebar-section-title">🏛️ National Portal Gateway</div>
    <p class="sidebar-caption">Select your access portal role below</p>
""", unsafe_allow_html=True)

if os.path.exists(twinbit_jpeg):
    st.sidebar.image(twinbit_jpeg, width=90)

if st.session_state.authenticated:
    _initials = "".join([p[0] for p in st.session_state.current_user.split()[:2]]).upper() if st.session_state.current_user else "U"
    st.sidebar.markdown(f"""
        <div class="profile-card">
            <div style="display:flex; align-items:center; gap:12px;">
                <div class="profile-avatar">{_initials}</div>
                <div>
                    <div style="font-size:0.95rem; font-weight:700;">{st.session_state.current_user}</div>
                    <div style="font-size:0.75rem; color:#93C5FD;">{st.session_state.user_role}</div>
                </div>
            </div>
            <div style="margin-top:10px; font-size:0.72rem; color:#86EFAC; display:flex; align-items:center;">
                <span class="status-dot"></span> Session Active &amp; Verified
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("🔒 Logout / Switch Portal", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.current_user = None
        st.rerun()

portal_choice = st.sidebar.radio(
    "Choose User Role Portal:",
    ["🧑‍🌾 Farmer Portal (किसान पोर्टल)", "👮 Field Officer Portal (अधिकारी पोर्टल)", "🛠️ National Admin Console (राष्ट्रीय एडमिन)"],
    label_visibility="collapsed"
)

st.sidebar.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.sidebar.markdown("""
    <div class="sidebar-section-title" style="font-size:0.92rem;">📡 System Health</div>
    <div class="health-item"><span class="status-dot"></span> PMFBY Gateway Connected</div>
    <div class="health-item"><span class="status-dot"></span> PostGIS Spatial Engine Online</div>
    <div class="health-item"><span class="status-dot"></span> 64-bit pHash Verification Active</div>
    <div class="health-item"><span class="status-dot"></span> C++ OpenCV Edge Gate Active</div>
""", unsafe_allow_html=True)

# Helper Functions
def render_metric_card(title, value, delta=None, delta_color="green", icon="📊", accent="#2563EB"):
    delta_html = ""
    if delta:
        color = "#15803D" if delta_color == "green" else "#DC2626"
        arrow = "▲" if delta_color == "green" else "▼"
        delta_html = f"<span class='metric-delta' style='color: {color};'>{arrow} {delta}</span>"

    return f"""
        <div class="metric-card-wrapper" style="--accent-color:{accent};">
            <div class="metric-icon">{icon}</div>
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}{delta_html}</div>
        </div>
    """

def render_badge(status_text):
    mapping = {
        "Approved": ("badge-approved", "✅"),
        "Pending Review": ("badge-pending", "⏳"),
        "Rejected": ("badge-rejected", "❌"),
        "Fraud": ("badge-fraud", "🚨"),
    }
    css_class, icon = mapping.get(status_text, ("badge-pending", "•"))
    return f'<span class="badge-status {css_class}">{icon} {status_text}</span>'

def render_claims_table(claims_list):
    rows = ""
    for c in claims_list:
        rows += f"""
            <tr>
                <td><b>{c['Claim_ID']}</b></td>
                <td>{c['Farmer_Name']}</td>
                <td>{c['Village']}</td>
                <td>{c['Crop']}</td>
                <td>{c['Loss_Type']}</td>
                <td>{c['Reported_Damage_Pct']}%</td>
                <td>{render_badge(c['Status'])}</td>
                <td>{c['AI_Confidence']}</td>
            </tr>
        """
    table_html = f"""
        <table class="premium-table">
            <thead>
                <tr>
                    <th>Claim ID</th><th>Farmer</th><th>Village</th><th>Crop</th>
                    <th>Loss Type</th><th>Damage %</th><th>Status</th><th>AI Confidence</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    """
    return table_html

# ==============================================================================
# 🧑‍🌾 1. FARMER PORTAL
# ==============================================================================
if portal_choice == "🧑‍🌾 Farmer Portal (किसान पोर्टल)":
    st.markdown('<div class="section-heading" style="font-size:1.5rem;">🧑‍🌾 Farmer Registration &amp; Crop Loss Claims Portal</div>', unsafe_allow_html=True)
    st.caption("Pradhan Mantri Fasal Bima Yojana (PMFBY) — Direct Farmer Services")

    if not st.session_state.authenticated or st.session_state.user_role != "Farmer":
        st.info("🔐 Complete the required fields to authenticate through the PMFBY Gateway.")

        with st.form("farmer_full_login"):
            st.markdown("#### 🌾 Farmer Authentication Gateway")
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                f_id = st.text_input("Farmer Registration ID:", value="FARM-UP-2026-8812")
                f_name = st.text_input("Full Name (as per PMFBY records):", value="Ramesh Kumar")
                f_mobile = st.text_input("Aadhaar-Linked Mobile Number:", value="+91 9876543210")
            with f_col2:
                f_pass = st.text_input("Account Password:", type="password", value="••••••••")
                f_aadhaar = st.text_input("12-Digit Aadhaar Number:", type="password", placeholder="Enter 12-digit Aadhaar number")
                f_otp = st.text_input("Aadhaar OTP (Received via SMS):", value="882190")

            submit_farmer_login = st.form_submit_button("🔑 Authenticate & Access Portal", type="primary", use_container_width=True)
            if submit_farmer_login:
                if f_id and f_name and f_mobile and f_pass and f_aadhaar and f_otp:
                    with st.spinner("Verifying Aadhaar OTP via PMFBY Gateway..."):
                        time.sleep(0.6)
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Farmer"
                    st.session_state.current_user = f_name
                    st.success("✅ Farmer identity & Aadhaar OTP verified via PMFBY Gateway!")
                    st.rerun()
                else:
                    st.error("Please complete all authentication fields.")

    else:
        st.markdown(f"""
            <div class="session-card">
                <h4 style="margin: 0; color: #0F172A;">✅ Authenticated Farmer Session</h4>
                <p style="margin: 4px 0 0 0; color: #475569; font-size: 0.9rem;">
                    Welcome, <b>{st.session_state.current_user}</b> | Farmer ID: <b>FARM-UP-2026-8812</b> | Registered Parcel: <b>Khata No. 442, Plot 18B (Kalyanpur)</b>
                </p>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3, tab4 = st.tabs([
            "📍 Land Geofence Verification",
            "📸 Capture Crop & Edge Check",
            "📑 File PMFBY Claim",
            "📜 Continuous Visual History"
        ])

        with tab1:
            st.markdown('<div class="section-heading">📍 PostGIS Cadastral Geofence Boundary Check</div>', unsafe_allow_html=True)
            st.write("The system locks image acquisition to your registered farm polygon to prevent off-target or neighbor field submissions.")

            col_a, col_b = st.columns(2)
            with col_a:
                st.text_input("Cadastral Land Record:", value="Khata No. 442 / Plot 18B (Kanpur Nagar)", disabled=True)
                st.text_input("Registered Parcel Size:", value="2.5 Acres (1.01 Hectares)", disabled=True)

                if st.button("📡 Acquire Live GPS Coordinates", type="primary", use_container_width=True):
                    with st.spinner("Triangulating satellite GPS lock..."):
                        time.sleep(0.6)
                    st.success("📍 Live GPS Captured: **26.8467° N, 80.9462° E**")
                    st.json({
                        "Geofence Status": "MATCHED_REGISTERED_PARCEL_POLYGON",
                        "PostGIS Spatial Query": "ST_Contains(Plot_18B_Polygon, Captured_Point) == TRUE",
                        "Centroid Offset Distance": "0.02 meters",
                        "Accuracy Level": "High Confidence (99.9%)"
                    })
            with col_b:
                st.markdown("**Registered Parcel Cadastral Map (PostGIS Polygon):**")

                fig_geo = px.scatter_mapbox(
                    pd.DataFrame({"lat": [26.8467], "lon": [80.9462], "label": ["Plot 18B Centroid"]}),
                    lat="lat", lon="lon", hover_name="label", zoom=14, height=280
                )
                fig_geo.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
                st.plotly_chart(fig_geo, use_container_width=True)

        with tab2:
            st.markdown('<div class="section-heading">📸 Periodic Crop Image Capture &amp; Edge Quality Gate</div>', unsafe_allow_html=True)
            st.caption("On-device C++ OpenCV modules inspect images for blur, exposure, and lighting before uploading.")

            c1, c2 = st.columns(2)
            with c1:
                growth_stage = st.selectbox(
                    "Select Current Growth Stage:",
                    ["1. Baseline / Sowing", "2. Vegetative Stage", "3. Flowering Stage", "4. Maturity Stage", "5. Post-Disaster Damage / Loss"]
                )
                crop_name = st.selectbox("Select Crop Type:", ["Wheat (गेहूँ)", "Paddy (धान)", "Mustard (सरसों)", "Sugarcane (गन्ना)"])
                notes = st.text_area("Farmer Field Observations / Notes:", placeholder="Describe crop health, irrigation status, or weather impact...")

            with c2:
                uploaded_photo = st.file_uploader("Upload Crop Photo (or capture with smartphone):", type=["jpg", "png", "jpeg"])
                if uploaded_photo:
                    st.image(uploaded_photo, caption="Uploaded Image Preview", use_container_width=True)

            if st.button("🚀 Run Quality Gate & Save to Ledger", type="primary", use_container_width=True):
                if uploaded_photo:
                    scan_placeholder = st.empty()
                    scan_placeholder.markdown("""
                        <div class="ai-scan-box">
                            🛰️ Running multi-layer AI inspection — Edge Quality Gate, pHash Duplicate Check, YOLOv11 Canopy Detection...
                        </div>
                    """, unsafe_allow_html=True)
                    progress = st.progress(0, text="Initializing AI pipeline...")
                    stages = ["Checking blur & luminance...", "Running pHash duplicate scan...", "YOLOv11 canopy detection...", "EfficientNet stage classification...", "Finalizing report..."]
                    for i, stage_msg in enumerate(stages):
                        time.sleep(0.15)
                        progress.progress(int((i + 1) / len(stages) * 100), text=stage_msg)
                    scan_placeholder.empty()
                    progress.empty()

                    st.balloons()
                    st.success("✅ Passed On-Device Edge Quality Gate & Multi-Layer Anti-Fraud Inspection!")

                    d1, d2, d3 = st.columns(3)
                    d1.markdown(render_metric_card("Laplacian Blur Variance", "142.5", "PASSED (>100)", "green", "🔍", "#22C55E"), unsafe_allow_html=True)
                    d2.markdown(render_metric_card("YUV Mean Luminance", "135 Y", "PASSED (40-220)", "green", "💡", "#22C55E"), unsafe_allow_html=True)
                    d3.markdown(render_metric_card("pHash Duplicate Check", "64-bit", "PASSED (Dh=18)", "green", "🛡️", "#22C55E"), unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("""
                        <div class="glass-card" style="border-top: 4px solid #22C55E;">
                            <h4 style="margin: 0 0 8px 0; color: #0F172A;">🟢 AI Crop Advisory Feedback (Real-Time Engine)</h4>
                            <p style="margin: 4px 0;"><strong>YOLOv11 Canopy Detection:</strong> Healthy Wheat Structure Identified (98.2% Confidence)</p>
                            <p style="margin: 4px 0;"><strong>EfficientNet Stage Classifier:</strong> Flowering Stage Confirmed</p>
                            <p style="margin: 4px 0;"><strong>Vision Transformer (ViT) Disease Scan:</strong> No severe pest infestation or fungal disease detected.</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Please upload a crop image first.")

        with tab3:
            st.markdown('<div class="section-heading">📑 File Instant Localized Crop Loss Claim</div>', unsafe_allow_html=True)
            st.write("Submit a claim for crop damage caused by natural calamities. Your entire season's visual ledger will be automatically attached.")

            with st.form("file_claim_form"):
                l_type = st.selectbox("Cause of Loss / Damage Event:", ["Flood Inundation", "Hailstorm Damage", "Crop Lodging (High Wind)", "Pest / Disease Attack", "Drought / Water Stress"])
                l_date = st.date_input("Date of Loss Event:", datetime.date.today())
                l_pct = st.slider("Estimated Damage Percentage (%):", 10, 100, 50)
                l_desc = st.text_area("Detailed Loss Summary:")

                sub_c = st.form_submit_button("📩 Submit Claim to Officer Queue", type="primary", use_container_width=True)
                if sub_c:
                    new_cid = f"CLM-2026-{len(st.session_state.claims_db)+8815}"
                    new_entry = {
                        "Claim_ID": new_cid,
                        "Farmer_Name": st.session_state.current_user,
                        "Village": "Kalyanpur (Kanpur Nagar)",
                        "Crop": "Wheat (गेहूँ)",
                        "Area": "2.5 Acres",
                        "Loss_Type": l_type,
                        "Loss_Date": str(l_date),
                        "Reported_Damage_Pct": l_pct,
                        "AI_SegFormer_Loss_Pct": float(l_pct) - 2.5,
                        "NDVI_Drop_Pct": -30.0,
                        "Weather_Event": "IMD Weather Event Logged",
                        "Edge_Blur_Score": 150.0,
                        "pHash_Match": "PASSED (Unique Image)",
                        "GPS_Geofence": "PASSED (Inside Cadastral Plot 18B)",
                        "Status": "Pending Review",
                        "AI_Confidence": "93.5% High Confidence Genuine"
                    }
                    st.session_state.claims_db.append(new_entry)
                    st.success(f"✅ Claim **{new_cid}** successfully generated and submitted to Field Officer Queue!")

        with tab4:
            st.markdown('<div class="section-heading">📜 Continuous Visual Ledger (Season Timeline)</div>', unsafe_allow_html=True)
            st.write("Tamper-proof visual chain of custody registered under PMFBY from baseline onboarding to loss claim:")

            timeline_html = """
            <table class="premium-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Stage</th>
                        <th>360° Onboarding Reference</th>
                        <th>GPS Match</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>2026-01-10</td>
                        <td>Sowing Baseline</td>
                        <td>Recorded</td>
                        <td>100%</td>
                        <td><span class="badge-status badge-verified">Verified Baseline</span></td>
                    </tr>
                    <tr>
                        <td>2026-02-01</td>
                        <td>Vegetative Check</td>
                        <td>Uploaded</td>
                        <td>99.8%</td>
                        <td><span class="badge-status badge-verified">Verified Stage 1</span></td>
                    </tr>
                    <tr>
                        <td>2026-02-20</td>
                        <td>Flowering Check</td>
                        <td>Uploaded</td>
                        <td>100%</td>
                        <td><span class="badge-status badge-verified">Verified Stage 2</span></td>
                    </tr>
                    <tr>
                        <td>2026-02-28</td>
                        <td>Post-Disaster Damage</td>
                        <td>Uploaded</td>
                        <td>100%</td>
                        <td><span class="badge-status badge-pending">Claim Filed</span></td>
                    </tr>
                </tbody>
            </table>
            """
            st.markdown(timeline_html, unsafe_allow_html=True)

# ==============================================================================
# 👮 2. FIELD OFFICER PORTAL
# ==============================================================================
elif portal_choice == "👮 Field Officer Portal (अधिकारी पोर्टल)":
    st.markdown('<div class="section-heading" style="font-size:1.5rem;">👮 Field Officer Claims Verification &amp; Assessment Dashboard</div>', unsafe_allow_html=True)
    st.caption("Pradhan Mantri Fasal Bima Yojana (PMFBY) — District Verification Office")

    if not st.session_state.authenticated or st.session_state.user_role != "Field Officer":
        st.info("🔐 Authenticate using your Official Government Officer Credentials.")

        with st.form("officer_login_form"):
            st.markdown("#### 👮 Officer Authentication Gateway")
            o_col1, o_col2 = st.columns(2)
            with o_col1:
                o_id = st.text_input("Officer Government ID Code:", value="OFF-UP-2026-104")
                o_name = st.text_input("Officer Full Name:", value="Dr. Vikramaditya Sharma")
            with o_col2:
                o_mobile = st.text_input("Official Registered Mobile Number:", value="+91 9811223344")
                o_pass = st.text_input("Secure Password:", type="password", value="••••••••")

            submit_officer_login = st.form_submit_button("🔑 Login to Officer Dashboard", type="primary", use_container_width=True)
            if submit_officer_login:
                if o_id and o_name and o_mobile and o_pass:
                    with st.spinner("Verifying officer credentials..."):
                        time.sleep(0.6)
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Field Officer"
                    st.session_state.current_user = o_name
                    st.success("✅ Officer Credentials Verified!")
                    st.rerun()
                else:
                    st.error("Please enter all required officer credentials.")

    else:
        st.caption(f"Authenticated Officer: **{st.session_state.current_user}** | ID: **OFF-UP-2026-104** | District: **Kanpur Nagar (UP)**")

        pending_count = len([c for c in st.session_state.claims_db if c['Status'] == 'Pending Review'])
        approved_count = len([c for c in st.session_state.claims_db if c['Status'] == 'Approved'])
        rejected_count = len([c for c in st.session_state.claims_db if c['Status'] == 'Rejected'])

        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(render_metric_card("Assigned Villages", "12 Villages", icon="🗺️", accent="#2563EB"), unsafe_allow_html=True)
        m2.markdown(render_metric_card("Pending Queue", f"{pending_count} Claims", icon="⏳", accent="#F59E0B"), unsafe_allow_html=True)
        m3.markdown(render_metric_card("Approved Claims", f"{approved_count} Claims", "Active Payouts", "green", "✅", "#22C55E"), unsafe_allow_html=True)
        m4.markdown(render_metric_card("Fraud Flagged", f"{rejected_count} Cases", "Blocked", "red", "🚨", "#EF4444"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="section-heading">📋 AI-Ranked Priority Claim Review Queue</div>', unsafe_allow_html=True)
        
        # PROPERLY RENDERED HTML TABLE (CRITICAL FIX FOR UNSAFE HTML)
        st.markdown(render_claims_table(st.session_state.claims_db), unsafe_allow_html=True)

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        st.markdown('<div class="section-heading">🔍 Side-by-Side Assessment &amp; Triangulation Review</div>', unsafe_allow_html=True)

        selected_cid = st.selectbox("Select Claim ID to Process:", [c["Claim_ID"] for c in st.session_state.claims_db])
        c_data = next(item for item in st.session_state.claims_db if item["Claim_ID"] == selected_cid)

        col_x, col_y = st.columns(2)

        with col_x:
            st.markdown("#### 1. Farmer Upload vs AI SegFormer Loss Assessment")

            fig_loss = px.imshow(
                [[0.1, 0.8, 0.9], [0.2, 0.7, 0.8], [0.1, 0.3, 0.6]],
                labels=dict(color="Damage Severity"),
                x=['Sector A', 'Sector B', 'Sector C'],
                y=['Row 1', 'Row 2', 'Row 3'],
                color_continuous_scale="Reds", height=260
            )
            fig_loss.update_layout(margin={"r":0,"t":25,"l":0,"b":0})
            st.plotly_chart(fig_loss, use_container_width=True)

            st.write(f"**Farmer Name:** {c_data['Farmer_Name']}")
            st.write(f"**Village:** {c_data['Village']}")
            st.write(f"**Reported Damage:** {c_data['Reported_Damage_Pct']}%")
            st.write(f"**SegFormer Damage Area:** {c_data['AI_SegFormer_Loss_Pct']}% Impacted")
            st.markdown(render_badge(c_data['Status']), unsafe_allow_html=True)

        with col_y:
            st.markdown("#### 2. Satellite & Weather Triangulation")

            ndvi_df = pd.DataFrame({
                "Date": ["Jan 10", "Jan 25", "Feb 10", "Feb 28"],
                "NDVI Index": [0.78, 0.82, 0.85, 0.42]
            })
            fig_ndvi = px.line(ndvi_df, x="Date", y="NDVI Index", markers=True, title="Sentinel-2 Temporal Vegetation Drop", height=260)
            fig_ndvi.update_traces(line_color="#EF4444", line_width=3)
            fig_ndvi.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
            st.plotly_chart(fig_ndvi, use_container_width=True)

            st.write(f"**Satellite NDVI Drop:** {c_data['NDVI_Drop_Pct']}% (Anomalous Vegetation Drop)")
            st.write(f"**IMD Weather Event:** {c_data['Weather_Event']}")
            st.write(f"**Anti-Fraud pHash Check:** {c_data['pHash_Match']}")
            st.write(f"**PostGIS Geofence Check:** {c_data['GPS_Geofence']}")

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        st.markdown('<div class="section-heading">⚡ Official Claim Settlement Action</div>', unsafe_allow_html=True)
        b1, b2, _ = st.columns([1, 1, 2])

        with b1:
            if st.button("✅ Approve Claim for Payout", type="primary", use_container_width=True):
                c_data["Status"] = "Approved"
                st.success(f"Claim **{selected_cid}** Approved! Transferred to Direct Benefit Transfer (DBT) Payout Queue.")
                st.rerun()

        with b2:
            if st.button("❌ Reject Claim", use_container_width=True):
                c_data["Status"] = "Rejected"
                st.error(f"Claim **{selected_cid}** Rejected due to discrepancy or fraud alert.")
                st.rerun()

# ==============================================================================
# 🛠️ 3. NATIONAL ADMIN PORTAL
# ==============================================================================
elif portal_choice == "🛠️ National Admin Console (राष्ट्रीय एडमिन)":
    st.markdown('<div class="section-heading" style="font-size:1.5rem;">🛠️ Ministry of Agriculture National PMFBY Oversight Console</div>', unsafe_allow_html=True)
    st.caption("Department of Agriculture & Farmers Welfare (DoA&FW) — National Command Center")

    if not st.session_state.authenticated or st.session_state.user_role != "National Admin":
        st.info("🔐 Secure Administrative Gateway. Restricted Access.")

        with st.form("admin_login_form"):
            st.markdown("#### 🛠️ Administrator Authentication Gateway")
            a_col1, a_col2 = st.columns(2)
            with a_col1:
                a_id = st.text_input("National Admin ID Code:", value="ADM-MOA-2026-001")
                a_name = st.text_input("Administrator Name:", value="Rajeshwardas Patel (IAS)")
            with a_col2:
                a_mobile = st.text_input("Secure Mobile Number:", value="+91 9900112233")
                a_pass = st.text_input("Admin Security Password:", type="password", value="••••••••")

            submit_admin_login = st.form_submit_button("🔑 Login to National Console", type="primary", use_container_width=True)
            if submit_admin_login:
                if a_id and a_name and a_mobile and a_pass:
                    with st.spinner("Authenticating administrator session..."):
                        time.sleep(0.6)
                    st.session_state.authenticated = True
                    st.session_state.user_role = "National Admin"
                    st.session_state.current_user = a_name
                    st.success("✅ National Administrator Authenticated!")
                    st.rerun()
                else:
                    st.error("Please enter all required administrator credentials.")

    else:
        st.caption(f"Authenticated Administrator: **{st.session_state.current_user}** | Admin Code: **ADM-MOA-2026-001**")

        a1, a2, a3, a4 = st.columns(4)
        a1.markdown(render_metric_card("Pilot Districts", "50 / 50", icon="🗂️", accent="#2563EB"), unsafe_allow_html=True)
        a2.markdown(render_metric_card("Enrolled Farmers", "482,190", icon="🧑‍🌾", accent="#14B8A6"), unsafe_allow_html=True)
        a3.markdown(render_metric_card("Fraud Interception", "98.4%", "+2.1%", "green", "🛡️", "#22C55E"), unsafe_allow_html=True)
        a4.markdown(render_metric_card("Settlement Speed", "3.2 Days", "-11.8 Days", "green", "⚡", "#22C55E"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        admin_tab1, admin_tab2 = st.tabs(["📊 District Loss & Crop Health Analytics", "🛡️ Multi-Layer Fraud Prevention Performance"])

        with admin_tab1:
            st.markdown('<div class="section-heading">🌐 District-Wise PMFBY Monitoring Status</div>', unsafe_allow_html=True)

            district_summary = pd.DataFrame({
                "District": ["Kanpur Nagar (UP)", "Lucknow (UP)", "Agra (UP)", "Varanasi (UP)", "Gorakhpur (UP)"],
                "Active Farmers": [12400, 9800, 15600, 8700, 11200],
                "Claims Submitted": [340, 120, 890, 45, 610],
                "Reported Loss %": [14.2, 8.1, 28.5, 4.2, 22.1],
                "System Alert": ["Normal Operations", "Normal Operations", "⚠️ High Loss (Flood)", "Normal Operations", "⚠️ High Loss (Rain)"]
            })

            col_d1, col_d2 = st.columns([1.5, 1])
            with col_d1:
                st.dataframe(district_summary, use_container_width=True)
            with col_d2:
                fig_dist = px.pie(district_summary, values="Claims Submitted", names="District", title="National Claim Volume Share", hole=0.4, height=280)
                fig_dist.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
                st.plotly_chart(fig_dist, use_container_width=True)

        with admin_tab2:
            st.markdown('<div class="section-heading">🛡️ Multi-Layer Anti-Fraud Gateway Summary</div>', unsafe_allow_html=True)
            st.write("Summary of non-genuine claim submissions blocked at cloud ingestion:")

            fraud_html = """
            <table class="premium-table">
                <thead>
                    <tr>
                        <th>Anti-Fraud Defense Layer</th>
                        <th>Submissions Intercepted</th>
                        <th>Action Executed</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>PostGIS Geofence Boundary Violation</td>
                        <td>1,240</td>
                        <td><span class="badge-status badge-rejected">Auto-Rejected at Ingestion Gateway</span></td>
                    </tr>
                    <tr>
                        <td>pHash Duplicate Image Detection (64-bit Hash)</td>
                        <td>890</td>
                        <td><span class="badge-status badge-pending">Flagged to Officer Queue</span></td>
                    </tr>
                    <tr>
                        <td>Edge Quality Gate (Blur / Illumination Failure)</td>
                        <td>420</td>
                        <td><span class="badge-status badge-verified">On-Device Retake Prompted</span></td>
                    </tr>
                    <tr>
                        <td>EXIF Timestamp / Device Mismatch</td>
                        <td>142</td>
                        <td><span class="badge-status badge-rejected">Auto-Rejected at Ingestion Gateway</span></td>
                    </tr>
                </tbody>
            </table>
            """
            st.markdown(fraud_html, unsafe_allow_html=True)

# ==============================================================================
# 5. ENTERPRISE FOOTER
# ==============================================================================
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("""
    <div class="footer-box">
        <p style="margin: 0; font-weight: 700; color: #0F172A;">
            🌾 SAMRIDH — Continuous Visual Ledger Platform | PMFBY CROPIC Initiative
        </p>
        <p style="margin: 4px 0 0 0; color: #64748B;">
            Department of Agriculture &amp; Farmers Welfare, Ministry of Agriculture, Government of India<br>
            Designed, Developed &amp; Maintained by <b>Team TwinBit</b>
        </p>
        <div class="footer-links">
            <a href="#">About PMFBY</a>
            <a href="#">Farmer Grievance Portal</a>
            <a href="#">Terms of Use</a>
            <a href="#">Privacy Policy</a>
            <a href="#">Accessibility Statement</a>
            <a href="#">RTI &amp; Citizen Charter</a>
        </div>
        <div class="footer-badges">
            <span class="badge-status badge-verified">🇮🇳 Government of India Portal</span>
            <span class="badge-status badge-approved">🛡️ WCAG 2.2 Accessible</span>
            <span class="badge-status badge-pending">🔒 Aadhaar-Secured Gateway</span>
        </div>
        <p style="margin-top: 14px; color: #94A3B8; font-size: 0.72rem;">
            © 2026 SAMRIDH Portal, Government of India. All Rights Reserved. | Best viewed in latest browser versions.
        </p>
    </div>
""", unsafe_allow_html=True)