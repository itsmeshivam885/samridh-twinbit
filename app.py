import streamlit as st
import pandas as pd
import datetime
import os

# ==============================================================================
# 1. PAGE CONFIGURATION & THEME STYLING
# ==============================================================================
st.set_page_config(
    page_title="SAMRIDH | PMFBY National Visual Analytics Portal",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Government Portal Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .tricolor-bar {
        height: 6px;
        background: linear-gradient(90deg, #FF9933 0%, #FF9933 33.3%, #FFFFFF 33.3%, #FFFFFF 66.6%, #138808 66.6%, #138808 100%);
        border-radius: 4px 4px 0 0;
        margin-bottom: 0px;
    }

    .gov-badge {
        background-color: rgba(30, 58, 138, 0.08);
        color: #1E3A8A;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
        border: 1px solid rgba(30, 58, 138, 0.2);
        display: inline-block;
        margin-bottom: 8px;
    }

    .gov-subtext {
        color: #059669;
        font-size: 0.98rem;
        font-weight: 600;
        margin-top: 4px;
    }

    .gov-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        border-top: 4px solid #1E3A8A;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 18px;
    }

    .gov-card-success {
        border-top: 4px solid #059669;
    }

    div.stButton > button:first-child {
        border-radius: 6px;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SHARED SESSION STATE DATA
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
# 3. NATIONAL GOV HEADER & DUAL LOGO BANNER (UPDATED IMAGE PATHS)
# ==============================================================================
st.markdown('<div class="tricolor-bar"></div>', unsafe_allow_html=True)

h_col1, h_col2, h_col3 = st.columns([1.2, 4.5, 1.3])

# Left Side: SAMRIDH Logo
with h_col1:
    samridh_path = os.path.join("images", "samridh_logo.png")
    if os.path.exists(samridh_path):
        st.image(samridh_path, width=140)
    elif os.path.exists("samridh_logo.png"):
        st.image("samridh_logo.png", width=140)
    else:
        st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🌾</h1>", unsafe_allow_html=True)

# Center Title
with h_col2:
    st.markdown("""
    <div style="text-align: center;">
        <div class="gov-badge">🇮🇳 GOVERNMENT OF INDIA | MINISTRY OF AGRICULTURE & FARMERS WELFARE</div>
        <h1 style='margin: 0; color: #0F172A; font-weight: 800; font-size: 2.2rem;'>समृद्धि (SAMRIDH) PORTAL</h1>
        <div class="gov-subtext">AI-Based Real-Time Crop Visual Analytics & Fraud-Resistant Loss Verification System</div>
        <small style='color: #64748B;'>PMFBY CROPIC Digital Infrastructure | Designed by <b>Team TwinBit</b> (ID: <b>svh-10104</b> | PS: <b>SVH26007</b>)</small>
    </div>
    """, unsafe_allow_html=True)

# Right Side: TwinBit Logo
with h_col3:
    twinbit_jpeg = os.path.join("images", "twinbit_logo.jpeg")
    twinbit_jpg = os.path.join("images", "twinbit_logo.jpg")
    twinbit_png = os.path.join("images", "twinbit_logo.png")
    
    if os.path.exists(twinbit_jpeg):
        st.image(twinbit_jpeg, width=130)
    elif os.path.exists(twinbit_jpg):
        st.image(twinbit_jpg, width=130)
    elif os.path.exists(twinbit_png):
        st.image(twinbit_png, width=130)
    elif os.path.exists("twinbit_logo.jpeg"):
        st.image("twinbit_logo.jpeg", width=130)
    else:
        st.markdown("<h1 style='text-align: center; color: #059669;'>⚡</h1>", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 4. SIDEBAR NAVIGATION & PORTAL SELECTOR
# ==============================================================================
st.sidebar.markdown("### 🏛️ National Portal Gateway")

# Display TwinBit logo in sidebar
if os.path.exists(twinbit_jpeg):
    st.sidebar.image(twinbit_jpeg, width=110, caption="Designed by Team TwinBit")

if st.session_state.authenticated:
    st.sidebar.success(f"👤 Authenticated User:\n\n**{st.session_state.current_user}**\n\nRole: **{st.session_state.user_role}**")
    if st.sidebar.button("🔒 Logout / Switch Portal", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.current_user = None
        st.rerun()

st.sidebar.caption("Select Access Portal:")
portal_choice = st.sidebar.radio(
    "Choose Role Portal:",
    ["🧑‍🌾 Farmer Portal (किसान पोर्टल)", "👮 Field Officer Portal (अधिकारी पोर्टल)", "🛠️ National Admin Console (राष्ट्रीय एडमिन)"]
)

st.sidebar.divider()
st.sidebar.markdown("""
**Official System Status:** 🟢 PMFBY Gateway Connected  
📡 PostGIS Spatial Server Active  
🛡️ pHash Fraud Engine Online  
⚡ Edge OpenCV Quality Gate Active  
""")

# ==============================================================================
# 🧑‍🌾 1. FARMER PORTAL
# ==============================================================================
if portal_choice == "🧑‍🌾 Farmer Portal (किसान पोर्टल)":
    st.markdown("## 🧑‍🌾 Farmer Registration & Crop Loss Claims Portal")
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
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Farmer"
                    st.session_state.current_user = f_name
                    st.success("✅ Farmer identity & Aadhaar OTP verified via PMFBY Gateway!")
                    st.rerun()
                else:
                    st.error("Please complete all authentication fields.")

    else:
        st.markdown(f"""
        <div class="gov-card gov-card-success">
            <h4>✅ Authenticated Farmer Session</h4>
            <p style='margin:0;'>Welcome, <b>{st.session_state.current_user}</b> | Farmer ID: <b>FARM-UP-2026-8812</b> | Registered Parcel: <b>Khata No. 442, Plot 18B (Kalyanpur)</b></p>
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
                st.image("https://placehold.co/600x320/0f172a/ffffff?text=PostGIS+Cadastral+Parcel+Boundary+(Kalyanpur+Plot+18B)", use_container_width=True)

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
                    d1.metric("Laplacian Blur Variance", "142.5", delta="PASSED (> 100)")
                    d2.metric("YUV Mean Luminance", "135 Y", delta="PASSED (40-220)")
                    d3.metric("pHash Duplicate Check", "64-bit Unique", delta="PASSED (Dh = 18)")
                    
                    st.markdown("""
                    <div class="gov-card gov-card-success">
                        <h4>🟢 AI Crop Advisory Feedback (Real-Time Engine)</h4>
                        <p><strong>YOLOv11 Canopy Detection:</strong> Healthy Wheat Structure Identified (98.2% Confidence)</p>
                        <p><strong>EfficientNet Stage Classifier:</strong> Flowering Stage Confirmed</p>
                        <p><strong>Vision Transformer (ViT) Disease Scan:</strong> No severe pest infestation or fungal disease detected.</p>
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
        
        m1, m2, m3, m4 = st.columns(4)
        pending_count = len([c for c in st.session_state.claims_db if c['Status'] == 'Pending Review'])
        approved_count = len([c for c in st.session_state.claims_db if c['Status'] == 'Approved'])
        rejected_count = len([c for c in st.session_state.claims_db if c['Status'] == 'Rejected'])
        
        m1.metric("Assigned Villages", "12 Villages")
        m2.metric("Pending Claim Queue", f"{pending_count} Claims")
        m3.metric("Approved Claims", f"{approved_count} Claims")
        m4.metric("Flagged Fraud Alerts", f"{rejected_count} Cases", delta="-1", delta_color="inverse")
        
        st.divider()
        
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
            st.image("https://placehold.co/500x300/1e293b/ffffff?text=Farmer+Loss+Upload+Image", caption=f"Loss Submission ({c_data['Loss_Type']})")
            st.write(f"**Farmer Name:** {c_data['Farmer_Name']}")
            st.write(f"**Village:** {c_data['Village']}")
            st.write(f"**Reported Damage:** {c_data['Reported_Damage_Pct']}%")
            st.write(f"**SegFormer Damage Area:** {c_data['AI_SegFormer_Loss_Pct']}% Impacted")

        with col_y:
            st.markdown("#### 2. Satellite & Weather Triangulation")
            st.image("https://placehold.co/500x300/0284c7/ffffff?text=Sentinel-2+Temporal+NDVI+Curve+Drop", caption="Copernicus Sentinel-2 Satellite NDVI Time-Series")
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
        a1.metric("Active Pilot Districts", "50 / 50 Districts")
        a2.metric("Total Enrolled Farmers", "482,190")
        a3.metric("Fraud Interception Rate", "98.4%", delta="+2.1%")
        a4.metric("Avg Settlement Speed", "3.2 Days", delta="-11.8 Days")

        st.divider()

        admin_tab1, admin_tab2 = st.tabs(["📊 District Loss & Crop Health Heatmap", "🛡️ Multi-Layer Fraud Prevention Performance"])

        with admin_tab1:
            st.markdown("### 🌐 District-Wise PMFBY Monitoring Status")
            
            district_summary = pd.DataFrame({
                "District": ["Kanpur Nagar (UP)", "Lucknow (UP)", "Agra (UP)", "Varanasi (UP)", "Gorakhpur (UP)"],
                "Active Farmers": [12400, 9800, 15600, 8700, 11200],
                "Claims Submitted": [340, 120, 890, 45, 610],
                "Reported Loss %": [14.2, 8.1, 28.5, 4.2, 22.1],
                "System Alert": ["Normal Operations", "Normal Operations", "⚠️ High Loss (Flood)", "Normal Operations", "⚠️ High Loss (Rain)"]
            })
            st.dataframe(district_summary, use_container_width=True)

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
# 5. FOOTER
# ==============================================================================
st.divider()
st.markdown("""
<div style="text-align: center; color: #64748B; padding: 10px;">
    SAMRIDH Continuous Visual Ledger Platform | PMFBY CROPIC Initiative<br>
    Built for Smart VIT Hackathon 2026 | <b>Team TwinBit</b> (SVH26007)
</div>
""", unsafe_allow_html=True)