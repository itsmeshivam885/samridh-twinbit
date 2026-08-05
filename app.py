import streamlit as st
import pandas as pd
import datetime
import os
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

# Custom Glassmorphism, Modern CSS Typography, Animations, and Government Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Manrope:wght@400;600;700;800&display=swap');

    /* Global CSS Variable System */
    :root {
        --primary: #2563EB;
        --primary-dark: #1D4ED8;
        --secondary: #0F172A;
        --success: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
        --accent: #14B8A6;
        --bg-main: #F8FAFC;
        --card-bg: #FFFFFF;
        --text-main: #0F172A;
        --text-muted: #64748B;
        --border-color: #E2E8F0;
        --glass-bg: rgba(255, 255, 255, 0.85);
        --glass-border: rgba(226, 232, 240, 0.8);
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    /* Reset Streamlit Base Appearance */
    .stApp {
        background: var(--bg-main);
        font-family: 'Inter', sans-serif;
        color: var(--text-main);
    }

    /* Animated Tricolor Top Accent Line */
    .tricolor-bar {
        height: 6px;
        width: 100%;
        background: linear-gradient(90deg, #FF9933 0%, #FF9933 33.3%, #FFFFFF 33.3%, #FFFFFF 66.6%, #138808 66.6%, #138808 100%);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-radius: 4px 4px 0 0;
    }

    /* Glassmorphic Government Banner Header */
    .gov-hero-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.98) 0%, rgba(30, 58, 138, 0.95) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px 32px;
        border-radius: 0 0 20px 20px;
        color: #FFFFFF;
        box-shadow: var(--shadow-lg);
        margin-bottom: 28px;
        transition: transform 0.3s ease;
    }
    
    .gov-hero-header:hover {
        border-color: rgba(20, 184, 166, 0.4);
    }

    /* Badge Pills */
    .gov-chip {
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.25);
        color: #F8FAFC;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Custom Metric Cards */
    .metric-card-wrapper {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 20px;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .metric-card-wrapper:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-md);
        border-color: var(--primary);
    }

    .metric-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .metric-value {
        font-size: 1.875rem;
        font-weight: 800;
        color: var(--text-main);
        margin: 6px 0;
        font-family: 'Manrope', sans-serif;
    }

    /* Status Badges */
    .badge-status {
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        display: inline-block;
    }
    .badge-approved { background-color: #D1FAE5; color: #065F46; border: 1px solid #A7F3D0; }
    .badge-pending { background-color: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
    .badge-rejected { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }
    .badge-fraud { background-color: #F3E8FF; color: #6B21A8; border: 1px solid #E9D5FF; }

    /* Custom Input & Button Styling Overrides */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);
        transition: all 0.2s ease-in-out;
    }

    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(37, 99, 235, 0.3);
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
    }

    /* Form Input Fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        border-radius: 10px !important;
        border: 1px solid var(--border-color) !important;
        background-color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus, .stTextArea>div>div>textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid var(--border-color);
    }

    /* Tab Custom Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        border-bottom: 2px solid var(--border-color);
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 8px 8px 0 0;
        padding: 0 20px;
        font-weight: 600;
        color: var(--text-muted);
        background-color: transparent;
        border: none;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        color: var(--primary) !important;
        border-bottom: 3px solid var(--primary) !important;
        background-color: rgba(37, 99, 235, 0.05) !important;
    }

    /* Footer Styling */
    .footer-box {
        text-align: center;
        padding: 24px;
        color: var(--text-muted);
        font-size: 0.875rem;
        border-top: 1px solid var(--border-color);
        margin-top: 40px;
    }
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
st.markdown('<div class="tricolor-bar"></div>', unsafe_allow_html=True)

header_left, header_mid, header_right = st.columns([1.2, 4.5, 1.3])

with header_left:
    samridh_path = os.path.join("images", "samridh_logo.png")
    if os.path.exists(samridh_path):
        st.image(samridh_path, width=130)
    elif os.path.exists("samridh_logo.png"):
        st.image("samridh_logo.png", width=130)
    else:
        st.markdown("<h1 style='font-size: 3rem; margin:0;'>🌾</h1>", unsafe_allow_html=True)

with header_mid:
    st.markdown("""
        <div style="text-align: center;">
            <div class="gov-chip">
                <span>🇮🇳</span> GOVERNMENT OF INDIA | MINISTRY OF AGRICULTURE & FARMERS WELFARE
            </div>
            <h1 style='margin: 8px 0 4px 0; color: #0F172A; font-family: "Manrope", sans-serif; font-weight: 800; font-size: 2.2rem; letter-spacing: -0.02em;'>
                समृद्धि (SAMRIDH) PORTAL
            </h1>
            <p style='margin: 0; color: #2563EB; font-weight: 600; font-size: 1.05rem;'>
                AI-Based Real-Time Crop Visual Analytics & Fraud-Resistant Loss Verification Platform
            </p>
            <p style='margin-top: 4px; color: #64748B; font-size: 0.85rem; font-weight: 500;'>
                PMFBY CROPIC Infrastructure | Designed by <b>Team TwinBit</b> (ID: <b>svh-10104</b> | PS: <b>SVH26007</b>)
            </p>
        </div>
    """, unsafe_allow_html=True)

with header_right:
    twinbit_jpeg = os.path.join("images", "twinbit_logo.jpeg")
    if os.path.exists(twinbit_jpeg):
        st.image(twinbit_jpeg, width=120)
    elif os.path.exists("twinbit_logo.jpeg"):
        st.image("twinbit_logo.jpeg", width=120)
    else:
        st.markdown("<h1 style='font-size: 3rem; margin:0; text-align:right;'>⚡</h1>", unsafe_allow_html=True)

st.markdown("<hr style='margin: 12px 0 24px 0; border: none; height: 1px; background-color: #E2E8F0;'>", unsafe_allow_html=True)

# ==============================================================================
# 4. SIDEBAR NAVIGATION & PORTAL SELECTOR
# ==============================================================================
st.sidebar.markdown("""
    <div style='padding: 8px 0;'>
        <h3 style='margin: 0; color: #0F172A; font-size: 1.1rem; font-weight: 700;'>🏛️ National Portal Gateway</h3>
        <p style='margin: 2px 0 12px 0; color: #64748B; font-size: 0.8rem;'>Select access portal role:</p>
    </div>
""", unsafe_allow_html=True)

if os.path.exists(twinbit_jpeg):
    st.sidebar.image(twinbit_jpeg, width=100)

if st.session_state.authenticated:
    st.sidebar.markdown(f"""
        <div style='background-color: #F0FDF4; border: 1px solid #BBF7D0; padding: 12px; border-radius: 10px; margin-bottom: 16px;'>
            <div style='font-size: 0.75rem; color: #166534; font-weight: 700; text-transform: uppercase;'>Session Active</div>
            <div style='font-size: 0.95rem; color: #0F172A; font-weight: 700;'>{st.session_state.current_user}</div>
            <div style='font-size: 0.8rem; color: #15803D;'>Role: {st.session_state.user_role}</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🔒 Logout / Switch Portal", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.current_user = None
        st.rerun()

portal_choice = st.sidebar.radio(
    "Choose User Role Portal:",
    ["🧑‍🌾 Farmer Portal (किसान पोर्टल)", "👮 Field Officer Portal (अधिकारी पोर्टल)", "🛠️ National Admin Console (राष्ट्रीय एडमिन)"]
)

st.sidebar.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
st.sidebar.markdown("""
    <div style='font-size: 0.8rem; color: #64748B;'>
        <strong>System Diagnostic:</strong><br>
        🟢 PMFBY Gateway Connected<br>
        📡 PostGIS Spatial Engine Online<br>
        🛡️ 64-bit pHash Verification Active<br>
        ⚡ C++ OpenCV Edge Gate Active
    </div>
""", unsafe_allow_html=True)

# Helper Function for Reusable Custom Metric Cards
def render_metric_card(title, value, delta=None, delta_color="green"):
    delta_html = ""
    if delta:
        color = "#10B981" if delta_color == "green" else "#EF4444"
        delta_html = f"<span style='color: {color}; font-size: 0.85rem; font-weight: 600; margin-left: 8px;'>{delta}</span>"
    
    return f"""
        <div class="metric-card-wrapper">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value} {delta_html}</div>
        </div>
    """

# ==============================================================================
# 🧑‍🌾 1. FARMER PORTAL
# ==============================================================================
if portal_choice == "🧑‍🌾 Farmer Portal (किसान पोर्टल)":
    st.markdown("## 🧑‍🌾 Farmer Registration & Crop Loss Claims Portal")
    st.caption("Pradhan Mantri Fasal Bima Yojana (PMFBY) — Direct Farmer Services")
    
    # FARMER LOGIN FORM
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
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Farmer"
                    st.session_state.current_user = f_name
                    st.success("✅ Farmer identity & Aadhaar OTP verified via PMFBY Gateway!")
                    st.rerun()
                else:
                    st.error("Please complete all authentication fields.")

    else:
        st.markdown(f"""
            <div style="background: #FFFFFF; border-left: 4px solid #10B981; padding: 16px 20px; border-radius: 12px; box-shadow: var(--shadow-sm); margin-bottom: 24px;">
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
            st.markdown("### 📍 PostGIS Cadastral Geofence Boundary Check")
            st.write("The system locks image acquisition to your registered farm polygon to prevent off-target or neighbor field submissions.")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.text_input("Cadastral Land Record:", value="Khata No. 442 / Plot 18B (Kanpur Nagar)", disabled=True)
                st.text_input("Registered Parcel Size:", value="2.5 Acres (1.01 Hectares)", disabled=True)
                
                if st.button("📡 Acquire Live GPS Coordinates", type="primary", use_container_width=True):
                    st.success("📍 Live GPS Captured: **26.8467° N, 80.9462° E**")
                    st.json({
                        "Geofence Status": "MATCHED_REGISTERED_PARCEL_POLYGON",
                        "PostGIS Spatial Query": "ST_Contains(Plot_18B_Polygon, Captured_Point) == TRUE",
                        "Centroid Offset Distance": "0.02 meters",
                        "Accuracy Level": "High Confidence (99.9%)"
                    })
            with col_b:
                st.markdown("**Registered Parcel Cadastral Map (PostGIS Polygon):**")
                
                # Interactive Geofence Plotly Visual
                fig_geo = px.scatter_mapbox(
                    pd.DataFrame({"lat": [26.8467], "lon": [80.9462], "label": ["Plot 18B Centroid"]}),
                    lat="lat", lon="lon", hover_name="label", zoom=14, height=280
                )
                fig_geo.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
                st.plotly_chart(fig_geo, use_container_width=True)

        with tab2:
            st.markdown("### 📸 Periodic Crop Image Capture & Edge Quality Gate")
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
                    st.balloons()
                    st.success("✅ Passed On-Device Edge Quality Gate & Multi-Layer Anti-Fraud Inspection!")
                    
                    d1, d2, d3 = st.columns(3)
                    d1.markdown(render_metric_card("Laplacian Blur Variance", "142.5", "PASSED (>100)", "green"), unsafe_allow_html=True)
                    d2.markdown(render_metric_card("YUV Mean Luminance", "135 Y", "PASSED (40-220)", "green"), unsafe_allow_html=True)
                    d3.markdown(render_metric_card("pHash Duplicate Check", "64-bit", "PASSED (Dh=18)", "green"), unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("""
                        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 4px solid #10B981; padding: 20px; border-radius: 12px;">
                            <h4 style="margin: 0 0 8px 0; color: #0F172A;">🟢 AI Crop Advisory Feedback (Real-Time Engine)</h4>
                            <p style="margin: 4px 0;"><strong>YOLOv11 Canopy Detection:</strong> Healthy Wheat Structure Identified (98.2% Confidence)</p>
                            <p style="margin: 4px 0;"><strong>EfficientNet Stage Classifier:</strong> Flowering Stage Confirmed</p>
                            <p style="margin: 4px 0;"><strong>Vision Transformer (ViT) Disease Scan:</strong> No severe pest infestation or fungal disease detected.</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Please upload a crop image first.")

        with tab3:
            st.markdown("### 📑 File Instant Localized Crop Loss Claim")
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
            st.markdown("### 📜 Continuous Visual Ledger (Season Timeline)")
            st.write("Tamper-proof visual chain of custody registered under PMFBY from baseline onboarding to loss claim:")
            
            timeline_data = [
                {"Date": "2026-01-10", "Stage": "Sowing Baseline", "360° Onboarding Reference": "Recorded", "GPS Match": "100%", "Status": "Verified Baseline"},
                {"Date": "2026-02-01", "Stage": "Vegetative Check", "Photo Upload": "Uploaded", "GPS Match": "99.8%", "Status": "Verified Stage 1"},
                {"Date": "2026-02-20", "Stage": "Flowering Check", "Photo Upload": "Uploaded", "GPS Match": "100%", "Status": "Verified Stage 2"},
                {"Date": "2026-02-28", "Stage": "Post-Disaster Damage", "Photo Upload": "Uploaded", "GPS Match": "100%", "Status": "Claim Filed"}
            ]
            st.table(pd.DataFrame(timeline_data))

# ==============================================================================
# 👮 2. FIELD OFFICER PORTAL
# ==============================================================================
elif portal_choice == "👮 Field Officer Portal (अधिकारी पोर्टल)":
    st.markdown("## 👮 Field Officer Claims Verification & Assessment Dashboard")
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
        m1.markdown(render_metric_card("Assigned Villages", "12 Villages"), unsafe_allow_html=True)
        m2.markdown(render_metric_card("Pending Queue", f"{pending_count} Claims"), unsafe_allow_html=True)
        m3.markdown(render_metric_card("Approved Claims", f"{approved_count} Claims", "Active Payouts", "green"), unsafe_allow_html=True)
        m4.markdown(render_metric_card("Fraud Flagged", f"{rejected_count} Cases", "Blocked", "red"), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("### 📋 AI-Ranked Priority Claim Review Queue")
        claims_df = pd.DataFrame(st.session_state.claims_db)
        st.dataframe(claims_df[["Claim_ID", "Farmer_Name", "Village", "Crop", "Loss_Type", "Reported_Damage_Pct", "Status", "AI_Confidence"]], use_container_width=True)
        
        st.divider()
        
        st.markdown("### 🔍 Side-by-Side Assessment & Triangulation Review")
        
        selected_cid = st.selectbox("Select Claim ID to Process:", [c["Claim_ID"] for c in st.session_state.claims_db])
        c_data = next(item for item in st.session_state.claims_db if item["Claim_ID"] == selected_cid)
        
        col_x, col_y = st.columns(2)
        
        with col_x:
            st.markdown("#### 1. Farmer Upload vs AI SegFormer Loss Assessment")
            
            # Simulated Computer Vision Damage Heatmap
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

        with col_y:
            st.markdown("#### 2. Satellite & Weather Triangulation")
            
            # Interactive Time-Series Satellite NDVI Curve
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

        st.divider()
        
        st.markdown("### ⚡ Official Claim Settlement Action")
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
    st.markdown("## 🛠️ Ministry of Agriculture National PMFBY Oversight Console")
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
        a1.markdown(render_metric_card("Pilot Districts", "50 / 50"), unsafe_allow_html=True)
        a2.markdown(render_metric_card("Enrolled Farmers", "482,190"), unsafe_allow_html=True)
        a3.markdown(render_metric_card("Fraud Interception", "98.4%", "+2.1%", "green"), unsafe_allow_html=True)
        a4.markdown(render_metric_card("Settlement Speed", "3.2 Days", "-11.8 Days", "green"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        admin_tab1, admin_tab2 = st.tabs(["📊 District Loss & Crop Health Analytics", "🛡️ Multi-Layer Fraud Prevention Performance"])

        with admin_tab1:
            st.markdown("### 🌐 District-Wise PMFBY Monitoring Status")
            
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
            st.markdown("### 🛡️ Multi-Layer Anti-Fraud Gateway Summary")
            st.write("Summary of non-genuine claim submissions blocked at cloud ingestion:")
            
            fraud_summary = pd.DataFrame({
                "Anti-Fraud Defense Layer": [
                    "PostGIS Geofence Boundary Violation", 
                    "pHash Duplicate Image Detection (64-bit Hash)", 
                    "Edge Quality Gate (Blur / Illumination Failure)", 
                    "EXIF Timestamp / Device Mismatch"
                ],
                "Submissions Intercepted": [1240, 890, 420, 142],
                "Action Executed": [
                    "Auto-Rejected at Ingestion Gateway", 
                    "Flagged to Officer Queue", 
                    "On-Device Retake Prompted", 
                    "Auto-Rejected at Ingestion Gateway"
                ]
            })
            st.table(fraud_summary)

# ==============================================================================
# 5. ENTERPRISE FOOTER
# ==============================================================================
st.divider()
st.markdown("""
    <div class="footer-box">
        <p style="margin: 0; font-weight: 600; color: #0F172A;">
            SAMRIDH Continuous Visual Ledger Platform | PMFBY CROPIC Initiative
        </p>
        <p style="margin: 4px 0 0 0; color: #64748B;">
            Ministry of Agriculture & Farmers Welfare, Government of India<br>
            Built for Smart VIT Hackathon 2026 | <b>Team TwinBit</b> (Team ID: <b>svh-10104</b> | Problem Statement: <b>SVH26007</b>)
        </p>
    </div>
""", unsafe_allow_html=True)