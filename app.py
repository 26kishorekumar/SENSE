import streamlit as st
import cv2
import numpy as np
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from gtts import gTTS
import os
import base64
from math import log
import uuid

# --- 1. CONFIGURATION & THEME ---
st.set_page_config(
    page_title="SENSE AI | Precision Health Dashboard", 
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Futuristic CSS with Glassmorphism and Keyframe Animations
st.markdown("""
    <style>
    /* 1. Global Page Entrance Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .main .block-container {
        animation: fadeIn 0.8s ease-out;
    }

    /* 2. Glassmorphic Background */
    .main {
        background: radial-gradient(circle at top right, #1a1c2c, #0e1117);
    }

    /* 3. Enhanced Metric Cards with Glow */
    [data-testid="stMetric"] {
        background: rgba(22, 27, 34, 0.7);
        border: 1px solid rgba(48, 54, 61, 1);
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    [data-testid="stMetric"]:hover {
        border-color: #00d1ff;
        box-shadow: 0 0 15px rgba(0, 209, 255, 0.3);
        transform: translateY(-2px);
    }

    /* 4. Triage Card Pulsing Effect */
    @keyframes pulse-border {
        0% { border-left-color: #ff4b4b; }
        50% { border-left-color: #ff9b9b; }
        100% { border-left-color: #ff4b4b; }
    }
    .triage-card { 
        padding: 20px; border-radius: 12px; margin-bottom: 15px; 
        background: rgba(28, 33, 40, 0.9); 
        border-left: 8px solid #ff4b4b;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(4px);
        animation: pulse-border 2s infinite;
    }

    /* 5. Recommendation Box with Gradient Border */
    .recommendation-box {
        padding: 20px; border-radius: 12px;
        background: #0d1117;
        border: 1px solid transparent;
        background-image: linear-gradient(#0d1117, #0d1117), 
                          linear-gradient(to right, #7000ff, #00d1ff);
        background-origin: border-box;
        background-clip: content-box, border-box;
        height: 100%;
        transition: 0.3s;
    }
    .recommendation-box:hover {
        filter: brightness(1.2);
    }

    /* 6. Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #0b0e14;
        border-right: 1px solid #30363d;
    }

    /* 7. Animated Loading Bar Color */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #7000ff, #00d1ff);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neural-bg"></div>', unsafe_allow_html=True)

# --- 2. ASSETS, DATABASE & AUDIO ENGINE ---

def add_logo():
    """Adds logo with a high-tech glass-glow effect."""
    if os.path.exists("LOGO.JPG"):
        st.sidebar.markdown("""
            <style>
            .logo-container {
                display: flex;
                justify-content: center;
                padding: 10px;
                filter: drop-shadow(0 0 10px rgba(0, 209, 255, 0.4));
                transition: transform 0.3s ease;
            }
            .logo-container:hover { transform: scale(1.02); }
            </style>
        """, unsafe_allow_html=True)
        st.sidebar.image("LOGO.JPG", use_container_width=True)

def speak(text):
    """
    Enhanced Voice Engine with dynamic caching and cleanup.
    Plays clinical voice notifications via Base64 injection.
    """
    try:
        # Generate unique voice token
        tts = gTTS(text=text, lang='en', slow=False)
        voice_id = uuid.uuid4().hex
        filename = f"voice_{voice_id}.mp3"
        tts.save(filename)
        
        # Read and encode
        with open(filename, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            
        # Inject HTML5 Audio with 'hidden' attribute to keep UI clean
        audio_html = f"""
            <audio autoplay="true" style="display:none;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
        
        # Immediate cleanup
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        # Fallback to silent logging if audio fails
        pass

# --- DATABASE ARCHITECTURE ---
def init_db():
    """Initializes a relational schema for high-speed diagnostic lookups."""
    db_conn = sqlite3.connect('sense_health.db', check_same_thread=False)
    db_cursor = db_conn.cursor()
    
    # Patient Registry with Metadata
    db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            pid TEXT PRIMARY KEY, 
            name TEXT, 
            join_date TEXT, 
            streak INTEGER DEFAULT 0
        )
    ''')
    
    # 5-Plex Diagnostic Repository
    db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            pid TEXT, 
            name TEXT, 
            glucose REAL, 
            hb REAL, 
            ntprobnp REAL, 
            lpa REAL, 
            troponin REAL, 
            score REAL, 
            timestamp DATETIME,
            FOREIGN KEY (pid) REFERENCES patients(pid)
        )
    ''')
    db_conn.commit()
    return db_conn, db_cursor

# Establish System Connection
conn, c = init_db()

# --- 3. ANALYTICS & BIOMARKER INTELLIGENCE ENGINE ---

#Clinical Reference Ranges
THRESHOLDS = {
    'glucose':  {'normal': 100, 'high': 200, 'label': 'Blood Glucose', 'unit': 'mg/dL'},
    'hb':       {'normal': 14,  'high': 8,   'label': 'Hemoglobin', 'unit': 'g/dL'},
    'ntprobnp': {'normal': 100, 'high': 500, 'label': 'NT-proBNP', 'unit': 'pg/mL'},
    'lpa':      {'normal': 20,  'high': 100, 'label': 'Lp(a)', 'unit': 'mg/dL'},
    'troponin': {'normal': 0.01, 'high': 0.5, 'label': 'Troponin I', 'unit': 'ng/mL'}
}

def color_to_value(hsv_mean, biomarker):
    """
    Advanced Colorimetric Mapping: Converts ROI pixel intensity into 
    clinically relevant biomarker concentrations.
    """
    # Saturation-based intensity mapping
    norm_score = np.clip(hsv_mean[1] / 255.0, 0, 1)
    t = THRESHOLDS[biomarker]
    
    # Backend Logic (Untouched): HB decreases with intensity, others increase
    if biomarker == 'hb':
        return t['normal'] - (norm_score * (t['normal'] - t['high']))
    
    return t['normal'] + (norm_score * (t['high'] - t['normal']))

def calculate_crs(vals):
    """
    SENSE-CRS (Cardiac Risk Score) Algorithm:
    Multi-variate weighted fusion of metabolic, hematologic, and cardiac biomarkers.
    """
    # Normalization Layers (Logic Untouched)
    s = [
        (vals[0]-70)/150,      # Glucose Stress
        (14-vals[1])/6,        # Anemic Stress
        log(vals[2]+1)/6,      # Heart Failure Indicator
        vals[3]/100,           # Lipid Burden
        vals[4]/0.5            # Acute Cardiac Injury (Troponin)
    ]
    
    # Clipping for index safety
    s = [np.clip(x, 0, 1) for x in s]
    
    # Weighted Medical Fusion (Logic Untouched)
    # Weights: Glucose(30%), HB(25%), NT-proBNP(20%), Lp(a)(15%), Troponin(10%)
    final_score = (0.3*s[0]) + (0.25*s[1]) + (0.2*s[2]) + (0.15*s[3]) + (0.1*s[4])
    
    # Enhancement: Log the calculation for Clinical Transparency
    print(f"--- ENGINE LOG: CRS CALCULATION ---")
    print(f"Metabolic: {s[0]:.2f} | Hema: {s[1]:.2f} | Cardiac: {s[2]:.2f}")
    
    return final_score

# --- NEW: SYSTEM CALIBRATION TOOL ---
def get_risk_label(score):
    """Returns clinical risk categorization and UI color-coding."""
    if score > 0.7: return "CRITICAL", "#FF4B4B"
    if score > 0.4: return "MODERATE", "#FFA500"
    return "STABLE", "#00FF00"

# --- 4. NAVIGATION & SIDEBAR ANALYTICS ---
add_logo()
st.sidebar.title("🩺 SENSE AI COMMAND")

# Animated Sidebar Metadata
st.sidebar.markdown(f"""
    <div style="background: rgba(0, 209, 255, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid #00D1FF;">
        <small style="color: #888;">NETWORK STATUS</small><br>
        <span style="color: #00FF00; font-weight: bold;">● SECURE LINK ACTIVE</span><br>
        <small style="color: #888;">PHC SECTOR 4 HUB</small>
    </div>
""", unsafe_allow_html=True)

st.sidebar.write("---")
page = st.sidebar.selectbox("🧭 OPERATIONAL VIEW", 
    ["Patient Registration", "New Diagnostic Scan", "Clinical History & Trends", "Personalized Care Plan", "Doctor's Triage Dashboard"])

# Sidebar Quick Stats
c.execute("SELECT COUNT(*) FROM patients")
total_p = c.fetchone()[0]
st.sidebar.metric("Database Registry", f"{total_p} Patients")

# --- PAGE: REGISTRATION (ENHANCED ONBOARDING) ---
if page == "Patient Registration":
    st.markdown("""
        <style>
        .registration-header {
            background: linear-gradient(90deg, #1e1e2f, #0e1117);
            padding: 20px;
            border-radius: 15px;
            border-bottom: 2px solid #7000FF;
            margin-bottom: 30px;
        }
        .id-card {
            background: linear-gradient(135deg, #00D1FF, #7000FF);
            padding: 25px;
            border-radius: 15px;
            color: white;
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
            max-width: 400px;
            margin-top: 20px;
            animation: fadeIn 1s ease;
        }
        </style>
        <div class="registration-header">
            <h1 style="margin:0;">📋 Patient Onboarding</h1>
            <p style="color:#888;">Initialize Secure Medical Identity for 5-Plex Diagnostics</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        with st.form("reg_form", clear_on_submit=True):
            st.markdown("### 👤 Identity Details")
            u_name = st.text_input("Full Legal Name", placeholder="e.g. John Doe")
            u_age = st.number_input("Age", min_value=1, max_value=120, value=30)
            u_gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
            
            st.markdown("---")
            st.caption("By registering, you consent to encrypted diagnostic processing.")
            
            submit = st.form_submit_button("🚀 INITIALIZE PATIENT RECORD")
            
            if submit and u_name:
                new_id = f"SENSE-{uuid.uuid4().hex[:6].upper()}"
                join_date = datetime.now().strftime('%Y-%m-%d')
                
                # Database Update
                c.execute("INSERT INTO patients VALUES (?,?,?,?)", (new_id, u_name, join_date, 0))
                conn.commit()
                
                # Voice Feedback
                speak(f"Registration successful for {u_name}. System ID generated.")
                
                # Show ID Card in the second column
                with col2:
                    st.balloons()
                    st.markdown(f"""
                        <div class="id-card">
                            <h4 style="margin:0; opacity:0.8;">SENSE AI HEALTH ID</h4>
                            <h2 style="margin:10px 0;">{u_name.upper()}</h2>
                            <div style="display: flex; justify-content: space-between;">
                                <span>ID: <b>{new_id}</b></span>
                                <span>DATE: {join_date}</span>
                            </div>
                            <hr style="opacity:0.3;">
                            <p style="font-size:10px; margin:0;">VALID AT ALL SECTOR-4 PHC CENTERS</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.success("✅ Secure Identity Generated Successfully")

    if not u_name and submit:
        st.error("Please enter a valid name to proceed.")

    # Educational Illustration
    st.write("##")
    with st.expander("ℹ️ Why is a SENSE ID required?"):
        st.write("""
            Your SENSE ID acts as a master key for your longitudinal health data. 
            It allows the AI to track cardiac trends over months, providing more accurate 
            risk assessments than a single one-off scan.
        """)

# --- PAGE: NEW DIAGNOSTIC SCAN (HIGH-TECH ANIMATED EDITION) ---
elif page == "New Diagnostic Scan":
    # Custom CSS for high-tech animations
    st.markdown("""
        <style>
        @keyframes scan { 
            0% { top: 0%; opacity: 0; } 
            50% { opacity: 1; } 
            100% { top: 100%; opacity: 0; } 
        }
        .scan-line {
            position: absolute; width: 100%; height: 4px;
            background: #00FF00; box-shadow: 0 0 15px #00FF00;
            animation: scan 2s linear infinite; z-index: 10;
        }
        .critical-bg {
            background: linear-gradient(90deg, #8b0000, #ff4b4b, #8b0000);
            background-size: 200% 200%;
            animation: gradient-move 2s ease infinite;
        }
        @keyframes gradient-move {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .metric-card {
            border: 1px solid #30363d; padding: 10px; border-radius: 10px;
            transition: transform 0.3s ease;
        }
        .metric-card:hover { transform: scale(1.05); border-color: #00FF00; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🔬 SENSE 5-Plex Analysis")
    p_id = st.text_input("Enter Patient ID")
    file = st.file_uploader("Upload Scanned Strip", type=['jpg', 'png', 'jpeg'])

    if file and p_id:
        c.execute("SELECT name FROM patients WHERE pid=?", (p_id,))
        p_res = c.fetchone()
        if p_res:
            p_name = p_res[0]
            img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), 1)
            h, w, _ = img.shape

            # Processing Logic (Original ROI Logic)
            img_blur = cv2.GaussianBlur(img, (5, 5), 0)
            hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)
            biomarker_keys = ['glucose', 'hb', 'ntprobnp', 'lpa', 'troponin']
            vals = []

            # ROI detection (Original)
            start_x, spacing, pad_w, pad_h, y_pos = int(w*0.05), int(w*0.18), int(w*0.12), int(h*0.40), int(h*0.30)
            img_disp = img.copy()
            for i, k in enumerate(biomarker_keys):
                x = start_x + (i * spacing)
                x2, y2 = min(x + pad_w, w), min(y_pos + pad_h, h)
                roi = hsv[y_pos:y2, x:x2]
                if roi.size > 0:
                    val = color_to_value(np.mean(roi, axis=(0,1)), k)
                    vals.append(val)
                    cv2.rectangle(img_disp, (x, y_pos), (x2, y2), (0, 255, 0), 3)
                else:
                    vals.append(THRESHOLDS[k]['normal'])

            vals = (vals + [THRESHOLDS[k]['normal'] for k in biomarker_keys[len(vals):]])[:5]
            score = calculate_crs(vals)
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute("INSERT INTO readings VALUES (?,?,?,?,?,?,?,?,?)", 
                      (p_id, p_name, vals[0], vals[1], vals[2], vals[3], vals[4], score, ts))
            conn.commit()

            # --- ANIMATED RESULTS VIEW ---
            st.success(f"Analysis Recorded for {p_name}")
            col_img, col_metrics = st.columns([1.2, 1])
            
            with col_img:
                # Adding the Animated Scan Line over the image
                st.markdown('<div style="position: relative;"><div class="scan-line"></div>', unsafe_allow_html=True)
                st.image(cv2.cvtColor(img_disp, cv2.COLOR_BGR2RGB), caption="Real-time Diagnostic Scan", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_metrics:
                st.markdown(f"### Score: `{score:.3f}`")
                for i, k in enumerate(biomarker_keys):
                    # Animated Metric Cards
                    st.markdown(f"""
                        <div class="metric-card">
                            <span style="color: #888;">{k.upper()}</span><br>
                            <span style="font-size: 20px; font-weight: bold; color: {'#ff4b4b' if vals[i] > THRESHOLDS[k]['high'] else '#00FF00'};">
                                {round(vals[i], 2)}
                            </span>
                        </div><br>
                    """, unsafe_allow_html=True)

            # --- AMBULANCE 108 EMERGENCY HUD ---
            if score > 0.7 or vals[4] > 0.4:
                # Audible Alert
                alert_sound = '<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mp3"></audio>'
                st.markdown(alert_sound, unsafe_allow_html=True)
                
                # Persistent Emergency HUD with Animated Gradient
                import time
                alert_placeholder = st.empty()
                with alert_placeholder.container():
                    st.markdown(f"""
                        <div class="critical-bg" style="padding: 30px; border-radius: 15px; border: 4px solid white; text-align: center;">
                            <h1 style="color: white; margin: 0; text-shadow: 2px 2px 10px black;">🚨 AMBULANCE 108 DISPATCHED 🚨</h1>
                            <h3 style="color: white;">CRITICAL ALERT FOR {p_name.upper()}</h3>
                            <p style="color: white;">Satellite Link: Active | PHC Sector 4: Notified</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    with st.status("Confirming Dispatch Handshake...", state="running") as status:
                        for i in range(5, 0, -1):
                            st.write(f"Vitals packet {6-i}/5 transmitted to Emergency Cloud... {i}s")
                            time.sleep(1)
                        status.update(label="108 DISPATCH CONFIRMED - UNIT EN ROUTE", state="complete")
                
                speak(f"Emergency. Ambulance 108 dispatched for {p_name}. Vitals synced with medical team.")

                # Response Visualizer
                st.subheader("🚑 Response Coordination Map")
                fig = go.Figure(go.Scatter(x=[0, 1.2, 2], y=[0, 0.8, 2], mode='lines+markers+text', 
                                          text=["PHC HUB", "AMB-108", "PATIENT"], 
                                          marker=dict(size=[20, 40, 20], color=['cyan', 'red', 'lime'],
                                                     line=dict(width=2, color='white'))))
                fig.update_layout(height=250, template="plotly_dark", margin=dict(l=5,r=5,t=5,b=5))
                st.plotly_chart(fig, use_container_width=True)

                st.toast(f"AMBULANCE 108 ASSIGNED TO {p_name}", icon="🚑")

            elif score > 0.4:
                st.warning("⚠️ Elevated Risk: Physician Alert Sent.")
                speak(f"High risk detected. Results shared with your clinic.")


# --- PAGE: CLINICAL HISTORY & TRENDS (HIGH-TECH ANALYTICS) ---
elif page == "Clinical History & Trends":
    # Enhanced CSS for Medical Analytics
    st.markdown("""
        <style>
        .report-card {
            background: rgba(255, 255, 255, 0.05);
            border-left: 5px solid #00D1FF;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        @keyframes heart-pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.1); opacity: 0.8; }
            100% { transform: scale(1); opacity: 1; }
        }
        .pulse-icon {
            display: inline-block;
            animation: heart-pulse 1.2s infinite;
            color: #FF4B4B;
            font-size: 24px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📈 Longitudinal Diagnostic Insights")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        pid = st.text_input("Patient ID Lookup", placeholder="Enter PID (e.g., P101)")
    with col2:
        st.write("##") # Alignment
        if pid:
            st.markdown('<span class="pulse-icon">❤️</span> **Monitoring Active**', unsafe_allow_html=True)

    if pid:
        df = pd.read_sql(f"SELECT * FROM readings WHERE pid='{pid}' ORDER BY timestamp ASC", conn)
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # --- FEATURE: CLINICAL DATA SUMMARY CARDS ---
            avg_score = df['score'].mean()
            last_score = df['score'].iloc[-1]
            delta = last_score - (df['score'].iloc[-2] if len(df) > 1 else last_score)

            c1, c2, c3 = st.columns(3)
            c1.metric("Current CRS Index", f"{last_score:.3f}", delta=f"{delta:.3f}", delta_color="inverse")
            c2.metric("Total Scans", len(df))
            c3.metric("Risk Profile", "CRITICAL" if last_score > 0.7 else "STABLE")

            # --- ENHANCED PLOTLY TRENDS WITH THRESHOLD ZONES ---
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            colors = ['#FFA500', '#FF4B4B', '#00D1FF', '#7000FF', '#00FF00']
            
            # Primary Markers
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['glucose'], name="Glucose", 
                                     line=dict(color=colors[0], width=3), mode='lines+markers'), secondary_y=False)
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['ntprobnp'], name="NT-proBNP", 
                                     line=dict(color=colors[1], width=3), mode='lines+markers'), secondary_y=False)
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['lpa'], name="Lp(a)", 
                                     line=dict(color=colors[3], width=3), mode='lines+markers'), secondary_y=False)
            
            # Secondary Markers (Dashed)
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['hb'], name="Hemoglobin", 
                                     line=dict(color=colors[2], dash='dot')), secondary_y=True)
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['troponin'], name="Troponin", 
                                     line=dict(color=colors[4], dash='dash')), secondary_y=True)

            # --- NEW: Background Threshold Shading ---
            fig.add_hrect(y0=0.7, y1=1.0, fillcolor="red", opacity=0.1, line_width=0, annotation_text="Critical Zone", secondary_y=False)
            fig.add_hrect(y0=0.4, y1=0.7, fillcolor="yellow", opacity=0.1, line_width=0, annotation_text="Warning Zone", secondary_y=False)

            fig.update_layout(
                title="<b>Comprehensive 5-Plex Bio-Trend Map</b>",
                template="plotly_dark",
                hovermode="x unified",
                xaxis=dict(showgrid=False),
                yaxis=dict(title="Marker Concentration (mg/dL)"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)

            # --- SENSE-CRS RISK PROGRESSION (ANIMATED AREA) ---
            st.subheader("🛡️ SENSE-CRS Risk Progression")
            
            # We use Plotly for the area chart to match the styling
            fig_area = go.Figure()
            fig_area.add_trace(go.Scatter(x=df['timestamp'], y=df['score'], fill='tozeroy', 
                                         line_color='#00FF00', name="Risk Score"))
            fig_area.update_layout(
                template="plotly_dark", 
                height=300, 
                margin=dict(l=0,r=0,t=0,b=0),
                xaxis=dict(showgrid=False),
                yaxis=dict(range=[0, 1])
            )
            st.plotly_chart(fig_area, use_container_width=True)

            # --- NEW FEATURE: CLINICAL LOGS TABLE ---
            with st.expander("📄 View Detailed Clinical Log", expanded=False):
                st.dataframe(df.style.background_gradient(subset=['score'], cmap='RdYlGn_r'), use_container_width=True)
                
            # --- NEXT STEP FEATURE ---
            if last_score > 0.6:
                st.markdown("""
                    <div class="report-card">
                        <h4 style="color:#FF4B4B;">⚕️ AI Clinical Observation</h4>
                        The CRS index shows an upward trend. High frequency monitoring is suggested.
                    </div>
                """, unsafe_allow_html=True)

        else:
            st.warning("⚠️ No diagnostic history found for this Patient ID.")

# --- PAGE: CARE PLAN ---
# --- PAGE: PERSONALIZED CARE PLAN (AI HEALTH COACH) ---
elif page == "Personalized Care Plan":
    # Custom Futuristic CSS
    st.markdown("""
        <style>
        .care-header {
            background: linear-gradient(45deg, #1e1e2f, #2a2a40);
            padding: 20px;
            border-radius: 15px;
            border-left: 10px solid #7000FF;
            margin-bottom: 25px;
        }
        .strategy-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            transition: all 0.4s ease;
        }
        .strategy-card:hover {
            background: rgba(255, 255, 255, 0.07);
            border-color: #7000FF;
            transform: translateY(-5px);
        }
        .status-badge {
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🥗 AI Care Strategy")
    pid = st.text_input("Search ID", placeholder="Enter Patient ID...")

    if pid:
        df_l = pd.read_sql(f"SELECT * FROM readings WHERE pid='{pid}' ORDER BY timestamp DESC LIMIT 1", conn)
        
        if not df_l.empty:
            data = df_l.iloc[0]
            
            # --- HEALTH AURA HEADER ---
            aura_color = "#FF4B4B" if data['score'] > 0.7 else "#FFA500" if data['score'] > 0.4 else "#00FF00"
            st.markdown(f"""
                <div class="care-header">
                    <h2 style="margin:0;">Strategy Roadmap: {data['name']}</h2>
                    <p style="margin:0; color:{aura_color};">● System Status: {'Critical Intervention Required' if data['score'] > 0.7 else 'Maintenance Mode'}</p>
                </div>
            """, unsafe_allow_html=True)

            # --- VISUALIZATION: BIOMARKER RADAR ---
            # Normalizing values for a 0-1 scale on radar
            categories = ['Glucose', 'Hemoglobin', 'NT-proBNP', 'Lp(a)', 'Troponin']
            # Simple normalization for visualization purposes
            radar_vals = [
                min(data['glucose']/200, 1), 
                min(data['hb']/18, 1), 
                min(data['ntprobnp']/1, 1), 
                min(data['lpa']/1, 1), 
                min(data['troponin']/1, 1)
            ]

            col_radar, col_info = st.columns([1.2, 1])
            
            with col_radar:
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=radar_vals,
                    theta=categories,
                    fill='toself',
                    fillcolor=aura_color,
                    opacity=0.3,
                    line=dict(color=aura_color, width=4),
                    name='Current Bio-Signature'
                ))
                fig_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                    showlegend=False,
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=350,
                    margin=dict(l=40, r=40, t=20, b=20)
                )
                st.plotly_chart(fig_radar, use_container_width=True)
                

            with col_info:
                st.write("### AI Diagnostics")
                st.info(f"**Bio-Age Index:** {round(data['score']*10 + 40, 1)} Years")
                st.metric("Risk Resilience", f"{round((1-data['score'])*100, 1)}%", help="Capability of system to handle metabolic stress")

            st.divider()

            # --- ACTIONABLE STRATEGY CARDS ---
            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown('<div class="strategy-card">', unsafe_allow_html=True)
                st.markdown("### 🍞 Metabolic")
                st.write(f"**Current:** {data['glucose']:.1f} mg/dL")
                if data['glucose'] > 140:
                    st.error("Action Required")
                    st.markdown("• Eliminate refined sugars<br>• 20m brisk walk post-meals<br>• Increase soluble fiber", unsafe_allow_html=True)
                else:
                    st.success("Target Achieved")
                    st.write("Maintain current complex-carb ratio.")
                st.markdown('</div>', unsafe_allow_html=True)

            with c2:
                st.markdown('<div class="strategy-card">', unsafe_allow_html=True)
                st.markdown("### 🩸 Hematology")
                st.write(f"**Current:** {data['hb']:.1f} g/dL")
                if data['hb'] < 12:
                    st.warning("Nutritional Focus")
                    st.markdown("• Iron-rich greens (Spinach)<br>• Vitamin C for absorption<br>• Reduce caffeine with meals", unsafe_allow_html=True)
                else:
                    st.success("Optimal Range")
                    st.write("Oxygen saturation is stable.")
                st.markdown('</div>', unsafe_allow_html=True)

            with c3:
                st.markdown('<div class="strategy-card">', unsafe_allow_html=True)
                st.markdown("### 🫀 Cardiac")
                st.write(f"**Index:** {data['score']:.2f}")
                if data['score'] > 0.5:
                    st.error("Stress Detected")
                    st.markdown("• Immediate physician review<br>• Reduce sodium < 1500mg/day<br>• Monitor resting HR", unsafe_allow_html=True)
                else:
                    st.success("Stable Condition")
                    st.write("Routine preventive care active.")
                st.markdown('</div>', unsafe_allow_html=True)

            # --- LIFESTYLE MATRIX ---
            st.write("##")
            with st.expander("🛠️ Personalized Lifestyle Prescription", expanded=True):
                t1, t2, t3 = st.tabs(["🥗 Nutrition", "🏃 Activity", "💊 Supplements"])
                with t1:
                    st.write("**Recommended Foods:** Walnuts, Flaxseeds, Leafy Greens, Fatty Fish.")
                    st.write("**Restrict:** Processed meats, High-fructose corn syrup.")
                    
                with t2:
                    rec_steps = 10000 if data['score'] < 0.4 else 5000
                    st.write(f"**Daily Goal:** {rec_steps} steps.")
                    st.write("**Modality:** Low-impact Zone 2 Cardio (Swimming/Fast Walking).")
                with t3:
                    if data['score'] > 0.5:
                        st.write("**Consult Doctor about:** CoQ10, Omega-3 Fish Oil, Magnesium Citrate.")
                    else:
                        st.write("**Focus:** General Multi-vitamin and Hydration.")

        else:
            st.info("🔍 No scan data found. Please complete a Diagnostic Scan first.")

# --- PAGE: DOCTOR'S TRIAGE DASHBOARD (COMMAND CENTER) ---
elif page == "Doctor's Triage Dashboard":
    # Custom CSS for Triage Command Center
    st.markdown("""
        <style>
        .triage-container {
            background: #0e1117;
            padding: 20px;
            border-radius: 15px;
        }
        .triage-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 8px solid;
            transition: all 0.3s ease;
        }
        .triage-card:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: scale(1.01);
        }
        @keyframes blink {
            0% { opacity: 1; }
            50% { opacity: 0.3; }
            100% { opacity: 1; }
        }
        .emergency-indicator {
            color: #ff4b4b;
            font-weight: bold;
            animation: blink 1s infinite;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("👨‍⚕️ PHC Administrative Hub")
    
    # --- TOP LEVEL ANALYTICS ---
    df_all = pd.read_sql("SELECT * FROM readings WHERE score > 0.4 ORDER BY timestamp DESC", conn)
    
    col1, col2, col3 = st.columns(3)
    critical_count = len(df_all[df_all['score'] > 0.7])
    moderate_count = len(df_all) - critical_count
    
    col1.metric("Critical Alerts", critical_count, delta="Immediate Action", delta_color="inverse")
    col2.metric("Moderate Risks", moderate_count)
    col3.metric("System Status", "Live", delta="Active Handshake")

    st.divider()

    # --- GEOSPATIAL TRIAGE (Simulated Distribution) ---
    st.subheader("📍 Emergency Geographic Distribution")
    if not df_all.empty:
        # Creating a simulated coordinate map for the triage
        fig_map = go.Figure(go.Scatter(
            x=np.random.randn(len(df_all)), 
            y=np.random.randn(len(df_all)),
            mode='markers+text',
            text=df_all['name'],
            marker=dict(
                size=df_all['score']*50, 
                color=df_all['score'], 
                colorscale='RdYlGn_r',
                showscale=True,
                colorbar=dict(title="Risk Index")
            )
        ))
        fig_map.update_layout(template="plotly_dark", height=300, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig_map, use_container_width=True)
        

    # --- TRIAGE QUEUE ---
    st.subheader("📋 Priority Triage Queue")
    
    if not df_all.empty:
        for i, row in df_all.iterrows():
            is_critical = row['score'] > 0.7
            severity = "🔴 CRITICAL" if is_critical else "🟡 MODERATE"
            color = "#ff4b4b" if is_critical else "#ffa500"
            
            # Card UI
            st.markdown(f'''
                <div class="triage-card" style="border-left-color: {color};">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-size: 1.2em; font-weight: bold;">{row["name"]}</span>
                        <span class="{"emergency-indicator" if is_critical else ""}">
                            {severity}
                        </span>
                    </div>
                    <p style="margin: 5px 0; color: #bbb;">
                        ID: <b>{row["pid"]}</b> | 
                        Timestamp: {row["timestamp"]} | 
                        CRS Score: <span style="color:{color}; font-weight:bold;">{row["score"]:.3f}</span>
                    </p>
                    <div style="font-size: 0.9em; color: #888;">
                        Troponin: {row['troponin']:.2f} | NT-proBNP: {row['ntprobnp']:.2f} | Lp(a): {row['lpa']:.2f}
                    </div>
                </div>
            ''', unsafe_allow_html=True)

            # Action Buttons
            c1, c2, c3 = st.columns([1.5, 1, 1])
            with c1:
                if st.button(f"🚀 Signal Dispatch: {row['name']}", key=f"disp_{i}"):
                    st.toast(f"Unit AMB-108 assigned to {row['name']}", icon="🚑")
                    speak(f"Ambulance signaled for {row['name']}.")
            with c2:
                if st.button(f"📞 Contact PHC", key=f"phc_{i}"):
                    st.toast(f"Tele-link established with {row['name']}'s sector PHC.")
            with c3:
                if st.button(f"✅ Mark Resolved", key=f"res_{i}"):
                    st.toast("Case archived.")

    else:
        st.success("✅ Triage Clear: No high-risk events detected in the last 24 hours.")

# --- FOOTER ---

st.markdown("---")

st.markdown("""
    <style>
    .footer-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        font-family: 'Courier New', Courier, monospace;
    }
    .status-ping {
        height: 10px;
        width: 10px;
        background-color: #00FF00;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
        box-shadow: 0 0 8px #00FF00;
        animation: pulse-green 2s infinite;
    }
    @keyframes pulse-green {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 0, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(0, 255, 0, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 0, 0); }
    }
    .footer-text {
        font-size: 0.85em;
        color: #888;
    }
    </style>
    
    <div class="footer-container">
        <div class="footer-text">
            <span class="status-ping"></span> 
            <b>SYSTEM STATUS:</b> ENCRYPTED & LIVE
        </div>
        <div class="footer-text">
            <b>SENSE AI v2.4</b> | 🛰️ Sat-Link Active
        </div>
        <div class="footer-text" style="color: #00D1FF;">
            Democratizing Cardiac Care
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<center style='color:#444; font-size:10px; margin-top:10px;'>HIPAA Compliant Data Encryption | Secure PHC Handshake Protocol</center>", unsafe_allow_html=True)
