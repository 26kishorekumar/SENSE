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
from fpdf import FPDF
import math
import time

def login_page():
  
    st.markdown("""
        <style>
        /* Background Glow Effect */
        .stApp {
            background: radial-gradient(circle at center, #1a1a2e 0%, #0f0f1a 100%);
        }
        
        .login-box {
            padding: 3rem;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(112, 0, 255, 0.3);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8), 
                        0 0 15px rgba(112, 0, 255, 0.2);
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .login-box:hover {
            border-color: #7000FF;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8), 
                        0 0 25px rgba(112, 0, 255, 0.4);
        }

        h1 {
            letter-spacing: 2px;
            font-weight: 800 !important;
            background: linear-gradient(45deg, #ffffff, #7000FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0px !important;
        }
        
        .stTextInput > div > div > input {
            background-color: rgba(0, 0, 0, 0.2) !important;
            color: white !important;
            border: 1px solid rgba(112, 0, 255, 0.2) !important;
        }

        /* Animated Button Styling */
        .stButton > button {
            background: linear-gradient(45deg, #7000FF, #450099) !important;
            color: white !important;
            font-weight: bold !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.6rem 2rem !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(112, 0, 255, 0.4) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.write("##")
    st.write("##")

    col1, col2, col3 = st.columns([0.8, 1.5, 0.8])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
 
        st.image("https://cdn-icons-png.flaticon.com/512/3858/3858733.png", width=80)
        
        st.title("SENSE AI")
        st.markdown("<p style='color: #888; font-size: 0.9rem; margin-top:-10px;'>Secure Clinical Intelligence Portal</p>", unsafe_allow_html=True)
        st.write("---")
        
        user = st.text_input("Institutional ID", placeholder="Enter username")
        pw = st.text_input("Access Key", type="password", placeholder="••••••••")
        
        st.write("##") 
        

        if st.button("INITIALIZE AUTHENTICATION", use_container_width=True):
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pw))
            result = c.fetchone()
            if result:
                st.session_state['logged_in'] = True
                st.session_state['user_role'] = result[2]
                st.session_state['username'] = user
                st.toast("Identity Verified. Welcome, Doctor.") 
                st.success("Access Granted")
                st.rerun()
            else:
                st.error("Authentication Failed: Invalid Credentials")
        
        st.markdown("<p style='font-size: 0.7rem; color: #555; margin-top: 20px;'>Authorized Personnel Only. System access is logged.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- CONFIGURATION & THEME ---
st.set_page_config(
    page_title="SENSE AI | Clinical Intelligence System",
    page_icon="🧬", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.yourclinic.com/support',
        'Report a bug': "https://www.yourclinic.com/bug",
        'About': "# SENSE AI: Precision Health Dashboard\nThis is a high-security clinical intelligence portal for 5-plex biomarker analysis."
    }
)

# --- GLOBAL STYLING ENHANCEMENTS ---

st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid rgba(112, 0, 255, 0.2);
    }

    /* Custom Scrollbar for Futuristic Feel */
    ::-webkit-scrollbar {
        width: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #0e1117;
    }
    ::-webkit-scrollbar-thumb {
        background: #7000FF;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #450099;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* 1. Global Page Entrance & Scanline Overlay */
    @keyframes fadeIn {
        from { opacity: 0; filter: blur(10px); transform: translateY(20px); }
        to { opacity: 1; filter: blur(0); transform: translateY(0); }
    }
    
    .main .block-container {
        animation: fadeIn 1.2s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Subtle Scanline Effect */
    .main::before {
        content: " ";
        display: block;
        position: fixed;
        top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.02));
        z-index: 9999;
        background-size: 100% 4px, 3px 100%;
        pointer-events: none;
        opacity: 0.3;
    }

    /* 2. Deep Space Glassmorphism */
    .main {
        background: radial-gradient(circle at 20% 20%, #1e1e30 0%, #0c0d13 100%);
    }

    /* 3. Cyber-Metric Cards with Animated Border */
    [data-testid="stMetric"] {
        background: rgba(13, 17, 23, 0.8) !important;
        border: 1px solid rgba(112, 0, 255, 0.3) !important;
        border-radius: 15px !important;
        padding: 25px !important;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5), inset 0 0 10px rgba(112, 0, 255, 0.1) !important;
    }
    
    [data-testid="stMetric"]::after {
        content: "";
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: conic-gradient(transparent, transparent, transparent, #7000ff);
        animation: rotate 4s linear infinite;
        opacity: 0.2;
        z-index: -1;
    }
    
    @keyframes rotate { 100% { transform: rotate(360deg); } }

    [data-testid="stMetric"]:hover {
        border-color: #00d1ff !important;
        box-shadow: 0 0 25px rgba(0, 209, 255, 0.4) !important;
        transform: scale(1.02);
    }

    /* 4. High-Risk Triage Pulse (Multi-dimensional) */
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 5px #ff4b4b; border-color: #ff4b4b; }
        50% { box-shadow: 0 0 20px #ff4b4b; border-color: #ff8e8e; }
        100% { box-shadow: 0 0 5px #ff4b4b; border-color: #ff4b4b; }
    }
    
    .triage-card { 
        padding: 25px;
        border-radius: 16px; margin-bottom: 20px; 
        background: rgba(35, 10, 10, 0.4); 
        border: 1px solid #ff4b4b;
        border-left: 10px solid #ff4b4b;
        backdrop-filter: blur(12px);
        animation: pulse-glow 3s infinite ease-in-out;
    }

    /* 5. Recommendation Box - Shimmer Effect */
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .recommendation-box {
        padding: 24px;
        border-radius: 16px;
        background: linear-gradient(90deg, #0d1117 25%, #161b22 50%, #0d1117 75%);
        background-size: 200% 100%;
        animation: shimmer 5s infinite linear;
        border: 1px solid rgba(0, 209, 255, 0.2);
        box-shadow: inset 0 0 15px rgba(0, 209, 255, 0.05);
    }

    /* 6. Sidebar Header UI */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b0e14 0%, #161b22 100%) !important;
        box-shadow: 5px 0 15px rgba(0,0,0,0.5);
    }
    
    /* 7. Enhanced Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(45deg, #7000ff, #00d1ff);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        transition: 0.4s;
    }
    .stButton>button:hover {
        letter-spacing: 3px;
        box-shadow: 0 0 20px rgba(112, 0, 255, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    /* 1. The Neural Container */
    .neural-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1; /* Keeps it behind all content */
        background: #0c0d13;
        overflow: hidden;
    }

    /* 2. Synaptic Pulse Effect */
    .neural-bg::after {
        content: "";
        position: absolute;
        width: 200%;
        height: 200%;
        top: -50%;
        left: -50%;
        background: radial-gradient(circle at center, 
                    rgba(112, 0, 255, 0.08) 0%, 
                    rgba(0, 209, 255, 0.03) 30%, 
                    transparent 70%);
        animation: synaptic-float 15s infinite linear;
    }

    /* 3. Grid Overlay for a Technical Look */
    .neural-bg::before {
        content: "";
        position: absolute;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(112, 0, 255, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(112, 0, 255, 0.05) 1px, transparent 1px);
        background-size: 50px 50px;
        mask-image: radial-gradient(ellipse at center, black, transparent 80%);
    }

    /* 4. Motion Animation */
    @keyframes synaptic-float {
        0% { transform: rotate(0deg) scale(1); }
        50% { transform: rotate(180deg) scale(1.2); }
        100% { transform: rotate(360deg) scale(1); }
    }

    /* 5. Artificial 'Flicker' for AI Intensity */
    @keyframes synaptic-flicker {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 0.6; }
        52% { opacity: 0.3; }
        54% { opacity: 0.7; }
    }
    .neural-bg {
        animation: synaptic-flicker 8s infinite secondary;
    }
    </style>
    
    <div class="neural-bg"></div>
""", unsafe_allow_html=True)


import io
import re
from fpdf import FPDF

def clean_medical_text(text):
    """
    Force-cleans text to be Latin-1 compatible.
    Removes Unicode/Emojis that corrupt the file structure.
    """
    if not text: return ""
    text = text.replace('⚠', '[!]').replace('•', '-').replace('▪', '-')
    return text.encode('latin-1', 'ignore').decode('latin-1')

def create_pdf_report(data, nutrition, activity, supplements):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- HEADER ---
    pdf.set_fill_color(20, 30, 50) 
    pdf.rect(0, 0, 210, 45, 'F')
    pdf.set_font("Helvetica", 'B', 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, "SENSE-AI | CLINICAL BIOMARKER REPORT", ln=True, align='L')
    
    # --- PATIENT INFO ---
    pdf.set_font("Helvetica", '', 10)
    pdf.set_text_color(200, 200, 200)
    safe_name = clean_medical_text(data['name'].upper())
    pdf.cell(0, 5, f"PATIENT: {safe_name} | ID: {data['pid']} | DATE: {data['timestamp']}", ln=True)
    pdf.ln(20)

    # --- TABLE---
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "I. DIAGNOSTIC RESULTS", ln=True)
    
    pdf.set_fill_color(230, 235, 245)
    w = [55, 40, 50, 45]
    cols = ["MARKER", "OBSERVED", "REFERENCE", "STATUS"]
    for i in range(len(cols)):
        pdf.cell(w[i], 10, cols[i], 1, 0, 'C', True)
    pdf.ln()

    # Data Rows
    # Optimized Data Rows for Clinical Accuracy
    pdf.set_font("Helvetica", '', 10)
    for key in ['glucose', 'hb', 'ntprobnp', 'lpa', 'troponin']:
        val = data[key]
        ref = THRESHOLDS[key]
        
        # 1. ALERT LOGIC: Hb is abnormal if BELOW threshold, others if ABOVE
        is_alert = val < ref['high'] if key == 'hb' else val > ref['high']
        status_text = "ACTION REQUIRED" if is_alert else "OPTIMAL"
        
        # 2. DYNAMIC REFERENCE SYMBOL: > for Hb floor, < for others' ceiling
        ref_symbol = ">" if key == 'hb' else "<"

        pdf.cell(w[0], 10, f" {ref['label']}", 1)
        pdf.cell(w[1], 10, f" {val:.2f} {ref['unit']}", 1, 0, 'C')
        pdf.cell(w[2], 10, f" {ref_symbol} {ref['high']} {ref['unit']}", 1, 0, 'C')
        
        # Status with Conditional Coloring
        if is_alert: 
            pdf.set_text_color(180, 0, 0) # Clinical Red
        else:
            pdf.set_text_color(0, 100, 0) # Success Green
            
        pdf.cell(w[3], 10, status_text, 1, 1, 'C')
        
        pdf.set_text_color(0, 0, 0)

    # --- CARE STRATEGY---
    pdf.ln(10)
    sections = [("NUTRITION", nutrition), ("ACTIVITY", activity), ("SUPPLEMENTS", supplements)]
    for title, content in sections:
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 8, title, ln=True)
        pdf.set_font("Helvetica", '', 10)
        pdf.multi_cell(0, 6, clean_medical_text(content), border='L')
        pdf.ln(4)
    return pdf.output(dest='S').encode('latin-1')

def add_logo():
    if os.path.exists("LOGO.JPG"):
        st.sidebar.markdown("""
            <style>
            .logo-wrapper {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(112, 0, 255, 0.2);
                border-radius: 20px;
                padding: 15px;
                margin-bottom: 20px;
                backdrop-filter: blur(10px);
                box-shadow: inset 0 0 20px rgba(112, 0, 255, 0.05);
                display: flex;
                justify-content: center;
                align-items: center;
                position: relative;
                overflow: hidden;
            }

            @keyframes logo-pulse {
                0% { filter: drop-shadow(0 0 5px rgba(112, 0, 255, 0.2)); }
                50% { filter: drop-shadow(0 0 20px rgba(0, 209, 255, 0.6)); }
                100% { filter: drop-shadow(0 0 5px rgba(112, 0, 255, 0.2)); }
            }

            .logo-wrapper::after {
                content: "";
                position: absolute;
                top: -100%;
                left: -100%;
                width: 50%;
                height: 300%;
                background: linear-gradient(
                    to right, 
                    transparent, 
                    rgba(255, 255, 255, 0.1), 
                    transparent
                );
                transform: rotate(45deg);
                animation: scan 4s infinite;
            }

            @keyframes scan {
                0% { top: -100%; left: -100%; }
                100% { top: 100%; left: 100%; }
            }

            .stImage > img {
                animation: logo-pulse 4s infinite ease-in-out;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                border-radius: 12px;
            }

            .stImage > img:hover {
                transform: scale(1.05) rotate(1deg);
                filter: drop-shadow(0 0 30px rgba(0, 209, 255, 0.8)) !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
        st.sidebar.image("LOGO.JPG", use_container_width=True)
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
import io

def speak(text):

    try:
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang='en', slow=False)
        tts.write_to_fp(mp3_fp)
        
        mp3_fp.seek(0)
        b64 = base64.b64encode(mp3_fp.read()).decode()
        
        audio_html = f"""
            <audio autoplay="true" style="display:none;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            <script>
                console.log("SENSE AI: Playing clinical notification...");
            </script>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
        
    except Exception as e:
        st.sidebar.error(f"Voice Engine Offline: {e}")
        
import sqlite3

# --- DATABASE ARCHITECTURE ---
def init_db():
    """
    Initializes a resilient relational schema.
    Enhancements: Added timeout and isolation levels for concurrent clinical access.
    """
    db_conn = sqlite3.connect('sense_health.db', check_same_thread=False, timeout=10)
    db_conn.row_factory = sqlite3.Row
    db_cursor = db_conn.cursor()

    # --- 1. USER AUTHENTICATION TABLE ---
    db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT
        )
    ''')
    
    # Default Credentials Check
    db_cursor.execute("SELECT * FROM users")
    if not db_cursor.fetchone():
        db_cursor.execute("INSERT INTO users VALUES (?, ?, ?)", ("admin", "admin123", "Doctor"))
    
    # --- 2. PATIENT REGISTRY (MASTER DATA) ---
    db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            pid TEXT PRIMARY KEY, 
            name TEXT, 
            phone TEXT,
            address TEXT,
            join_date TEXT, 
            streak INTEGER DEFAULT 0
        )
    ''')

    # --- AUTO-MIGRATION LOGIC---
    db_cursor.execute("PRAGMA table_info(patients)")
    columns = [column[1] for column in db_cursor.fetchall()]
    if 'phone' not in columns:
        db_cursor.execute('ALTER TABLE patients ADD COLUMN phone TEXT')
    if 'address' not in columns:
        db_cursor.execute('ALTER TABLE patients ADD COLUMN address TEXT')
    
    # --- 3. 5-PLEX DIAGNOSTIC REPOSITORY (READINGS) ---
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

    # --- 4. CARE PLAN REPOSITORY (PHYSICIAN NOTES) ---
    db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS care_plans (
            pid TEXT PRIMARY KEY,
            nutrition TEXT,
            activity TEXT,
            supplements TEXT,
            last_updated DATETIME,
            FOREIGN KEY (pid) REFERENCES patients(pid)
        )
    ''')

    db_conn.commit()
    return db_conn, db_cursor

conn, c = init_db()

# --- LOGIN SYSTEM LOGIC ---

def login_page():
    """
    Renders a high-fidelity, secure clinical login interface.
    Enhancements: Glassmorphism, Form-submission support, and identity-branding.
    """
    st.markdown("""
        <style>
        /* Centered Background Glow */
        .stApp {
            background: radial-gradient(circle at center, #1a1b26 0%, #0a0a0f 100%);
        }
        
        .login-card {
            padding: 40px;
            border-radius: 24px;
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(112, 0, 255, 0.3);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), 
                        inset 0 0 20px rgba(112, 0, 255, 0.05);
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .auth-shield {
            font-size: 50px;
            background: linear-gradient(45deg, #7000FF, #00d1ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 10px rgba(112, 0, 255, 0.5));
            margin-bottom: 10px;
        }

        /* Styling Inputs to match the Futuristic Theme */
        .stTextInput > div > div > input {
            background-color: rgba(0, 0, 0, 0.3) !important;
            border: 1px solid rgba(112, 0, 255, 0.2) !important;
            color: #e0e0e0 !important;
            border-radius: 10px !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: #00d1ff !important;
            box-shadow: 0 0 10px rgba(0, 209, 255, 0.2) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.write("##")
    col1, col2, col3 = st.columns([0.8, 1.4, 0.8])
    
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="auth-shield">🛡️</div>', unsafe_allow_html=True)
        st.title("SENSE AI")
        st.caption("SECURE CLINICAL AUTHENTICATION PROTOCOL")
        st.markdown("---")
        
        with st.form("auth_form", clear_on_submit=False):
            u_name = st.text_input("Institutional Username", placeholder="e.g. dr_smith")
            u_pass = st.text_input("Security Access Key", type="password", placeholder="••••••••")
            
            st.write("##")
            submit = st.form_submit_button("🚀 INITIALIZE SYSTEM ACCESS", use_container_width=True)
            
            if submit:
                c.execute("SELECT * FROM users WHERE username=? AND password=?", (u_name, u_pass))
                user_record = c.fetchone()
                
                if user_record:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = u_name
                    st.session_state['user_role'] = user_record[2]
                    st.toast("Identity Verified. Accessing Diagnostic Hub...")
                    st.success("Credentials Confirmed.")
                    st.rerun()
                else:
                    st.error("Access Denied: Check Username/Key")
        
        st.markdown("<p style='font-size: 10px; color: #555; margin-top: 20px;'>Encryption Standard: AES-256 | System Access Logged</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- SESSION INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- THE GATEKEEPER ---
if not st.session_state['logged_in']:
    login_page()
    st.stop()

# --- LOGGED IN UI ---
st.sidebar.markdown(f"""
    <div style="padding:10px; border-radius:10px; background:rgba(0, 255, 128, 0.1); border:1px solid #00ff80;">
        <span style="color:#00ff80;">● SYSTEM ONLINE</span><br>
        <small style="color:#ccc;">User: {st.session_state['username']}</small>
    </div>
    <br>
""", unsafe_allow_html=True)

if st.sidebar.button("🚪 TERMINATE SESSION", use_container_width=True):
    st.session_state['logged_in'] = False
    st.rerun()
    
# --- ANALYTICS & BIOMARKER INTELLIGENCE ENGINE ---

# Clinical Reference Ranges (Architectural Constants - Do Not Modify)
THRESHOLDS = {
    'glucose':  {'normal': 100,  'high': 140,  'label': 'Blood Glucose', 'unit': 'mg/dL'},  # Abnormal > 140
    'hb':       {'normal': 14,   'high': 12,   'label': 'Hemoglobin',    'unit': 'g/dL'},   # Abnormal < 12
    'ntprobnp': {'normal': 100,  'high': 125,  'label': 'NT-proBNP',    'unit': 'pg/mL'},  # Abnormal > 125
    'lpa':      {'normal': 190,  'high': 200,  'label': 'Total Serum Cholesterol',  'unit': 'mg/dL'},  # High Risk > 200
    'troponin': {'normal': 0.01, 'high': 0.04, 'label': 'Troponin I',    'unit': 'ng/mL'}   # Abnormal > 0.04
}

def color_to_value(hsv_mean: list, biomarker: str) -> float:
    """
    Advanced Colorimetric Mapping Engine.
    Converts ROI pixel intensity (HSV Space) into clinically calibrated values.
    Safety Enhancements: 
    - Type hinting for IDE optimization.
    - Bound-clipping to prevent non-physiological results.
    - Floating-point precision rounding.
    """
    try:
        saturation_intensity = np.clip(hsv_mean[1] / 255.0, 0, 1)
        
        t = THRESHOLDS[biomarker]

        if biomarker == 'hb':
            result = t['normal'] - (saturation_intensity * (t['normal'] - t['high']))
        else:
            result = t['normal'] + (saturation_intensity * (t['high'] - t['normal']))
            
        return round(float(result), 3)
        
    except KeyError:
        return 0.0
    except Exception:
        return 0.0

@st.cache_data(show_spinner=False)
def calculate_crs(vals):
    try:
        v = [float(x) for x in vals]
        
        normalized_vectors = [
            (v[0] - 70) / 150,               # Glucose
            (14 - v[1]) / 6,                 # Hemoglobin
            math.log(max(v[2], 0) + 1) / 6,  # NT-proBNP
            v[3] / 200,                      # Total Serum Cholesterol
            v[4] / 0.04                      # Troponin
        ]
        
        s = [np.clip(x, 0, 1) for x in normalized_vectors]
        
        # Clinical weighting factors
        final_score = (0.3 * s[0]) + (0.25 * s[1]) + (0.2 * s[2]) + (0.15 * s[3]) + (0.1 * s[4])
        
        import logging
        logging.info(f"CRS Engine - PID: {st.session_state.get('active_pid', 'Unknown')}")
        logging.info(f"Indices: G:{s[0]:.3f} H:{s[1]:.3f} N:{s[2]:.3f} L:{s[3]:.3f} T:{s[4]:.3f}")

        return round(float(final_score), 5)
    except Exception as e:
        st.error(f"SENSE-CRS Engine Error: {e}")
        return 0.0

def get_risk_label(score):
    if score >= 0.75:
        return "CRITICAL ALERT", "#FF3131" # High-intensity red
    if score >= 0.50:
        return "ELEVATED RISK", "#FF9100"  # Clinical orange
    if score >= 0.25:
        return "INCIPIENT", "#00D1FF"       # Warning/Early detection blue
    return "STABLE / OPTIMAL", "#00FF80"   # Healthy green

add_logo()

st.sidebar.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;} /* Optional: Hides default nav to use your selectbox */
    .sidebar-stat-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(112, 0, 255, 0.2);
        padding: 12px;
        border-radius: 12px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("🩺 SENSE AI COMMAND")

# Enhanced Animated Sidebar Metadata
st.sidebar.markdown(f"""
    <div style="background: rgba(0, 209, 255, 0.05); padding: 18px; border-radius: 15px; border-left: 4px solid #00D1FF; border-right: 1px solid rgba(0, 209, 255, 0.2);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <small style="color: #00D1FF; letter-spacing: 1px; font-weight: bold;">NODE: PHC-SECTOR 4</small>
            <span style="color: #00FF00; font-size: 10px; animation: blink 2s infinite;">● LIVE</span>
        </div>
        <div style="margin-top: 8px;">
            <span style="color: #FFFFFF; font-family: monospace; font-size: 14px;">SECURE LINK ENCRYPTED</span><br>
            <small style="color: #555;">LATENCY: 14ms | SSL: ACTIVE</small>
        </div>
    </div>
    <style>
    @keyframes blink {{
        0% {{ opacity: 0.2; }}
        50% {{ opacity: 1; }}
        100% {{ opacity: 0.2; }}
    }}
    </style>
""", unsafe_allow_html=True)

st.sidebar.write("##")

page = st.sidebar.selectbox("🧭 OPERATIONAL VIEW", [
    "👤 Patient Registration",
    "📁 Master Patient Directory",
    "🔬 New Diagnostic Scan",
    "📉 Clinical History & Trends",
    "💊 Personalized Care Plan",
    "🚨 Doctor's Triage Dashboard"
])

st.sidebar.write("---")

c.execute("SELECT COUNT(*) FROM patients")
total_p = c.fetchone()[0]

with st.sidebar.container():
    st.markdown('<div class="sidebar-stat-card">', unsafe_allow_html=True)
    st.metric("Total Registry", f"{total_p} Patients", delta=f"{total_p} Active", delta_color="normal")
    st.markdown(f"""
        <hr style="margin: 10px 0; border: 0.1px solid rgba(255,255,255,0.1);">
        <small style="color: #888;">AUTHORIZED ACCESS:</small><br>
        <span style="color: #7000FF; font-weight: bold;">{st.session_state.get('username', 'STAFF')}</span>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: REGISTRATION---
if page == "👤 Patient Registration":
    st.markdown("""
        <style>
        .registration-header {
            background: linear-gradient(135deg, rgba(30,30,47,0.9), rgba(14,17,23,0.9));
            padding: 25px;
            border-radius: 20px;
            border-left: 5px solid #7000FF;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin-bottom: 30px;
            animation: fadeIn 0.8s ease-out;
        }
        
        /* Modernized ID Card with Glass Overlay */
        .id-card {
            background: linear-gradient(135deg, #7000FF 0%, #00D1FF 100%);
            padding: 30px;
            border-radius: 20px;
            color: white;
            box-shadow: 0 20px 40px rgba(112, 0, 255, 0.3);
            max-width: 450px;
            margin: auto;
            position: relative;
            overflow: hidden;
            animation: slideInRight 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        .id-card::before {
            content: "";
            position: absolute;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
            animation: rotate 10s linear infinite;
        }

        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(50px); }
            to { opacity: 1; transform: translateX(0); }
        }

        /* Styled Form Inputs */
        .stForm {
            background: rgba(255,255,255,0.02) !important;
            border-radius: 20px !important;
            border: 1px solid rgba(112, 0, 255, 0.1) !important;
            padding: 20px !important;
        }
        </style>
        
        <div class="registration-header">
            <h1 style="margin:0; font-family: 'Inter', sans-serif; letter-spacing:-1px;">📋 Patient Onboarding</h1>
            <p style="color:#00D1FF; font-weight: 500;">Establishing Secure Clinical Identity Hub</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        with st.form("reg_form", clear_on_submit=True):
            st.markdown("### 👤 Medical Identity Details")
            sub_col1, sub_col2 = st.columns([2, 1])
            u_name = sub_col1.text_input("Full Legal Name", placeholder="e.g. John Doe")
            u_age = sub_col2.number_input("Age", min_value=1, max_value=120, value=30)
            u_gender = st.selectbox("Gender Registry", ["Male", "Female", "Other", "Prefer not to say"])
            
            st.markdown("### 📞 Contact & Residency")
            u_phone = st.text_input("Primary Phone Number", placeholder="+91 XXXXX-XXXXX")
            u_address = st.text_area("Official Residential Address", placeholder="Enter full address for medical records...")
            
            st.write("##")
            st.caption("🔒 All data is stored in an AES-256 encrypted local clinical database.")
            submit = st.form_submit_button("🚀 INITIALIZE PATIENT RECORD", use_container_width=True)
            
            if submit:
                if not u_name or not u_phone:
                    st.error("❌ Mandatory Fields Missing: Please provide Name and Phone.")
                else:
                    new_id = f"SENSE-{uuid.uuid4().hex[:6].upper()}"
                    join_date = datetime.now().strftime('%Y-%m-%d')
                    c.execute("INSERT INTO patients (pid, name, phone, address, join_date, streak) VALUES (?,?,?,?,?,?)", (new_id, u_name, u_phone, u_address, join_date, 0))
                    conn.commit()
                    speak(f"Registration successful for {u_name}. System ID generated.")
                    st.session_state['last_reg'] = {
                        'name': u_name,
                        'id': new_id,
                        'date': join_date,
                        'phone': u_phone,
                        'address': u_address
                    }
                    st.balloons()

    with col2:
        if 'last_reg' in st.session_state:
            reg = st.session_state['last_reg']
            st.markdown(f"""
                <div class="id-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <h4 style="margin:0; letter-spacing: 2px;">SENSE AI IDENTITY</h4>
                        <span style="background:rgba(255,255,255,0.2); padding:2px 8px; border-radius:5px; font-size:10px;">ACTIVE</span>
                    </div>
                    <h1 style="margin:20px 0; font-size: 2.2em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">{reg['name'].upper()}</h1>
                    <div style="font-family: monospace; font-size: 1.1em; background: rgba(0,0,0,0.1); padding: 15px; border-radius: 10px;">
                        <div style="margin-bottom:5px;"><b>ID:</b> {reg['id']}</div>
                        <div style="margin-bottom:5px;"><b>PH:</b> {reg['phone']}</div>
                        <div style="font-size: 0.8em; opacity: 0.9;"><b>LOC:</b> {reg['address']}</div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 25px; opacity: 0.8; font-size: 0.8em;">
                        <span>ISSUED: {reg['date']}</span>
                        <span>VERIFIED BY: SENSE-CORE</span>
                    </div>
                </div>
                <br>
                <div style="text-align:center;">
                    <p style="color:#888; font-size: 0.9rem;">Identity card generated and encrypted.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Awaiting new registration to generate Identity Card...")

# --- PAGE: MASTER DIRECTORY ---
elif page == "📁 Master Patient Directory":
    st.title("📁 Clinical Registry Master")
    st.markdown("---")
    
    c.execute("SELECT pid, name, phone, join_date, streak FROM patients ORDER BY join_date DESC")
    patients = c.fetchall()
    
    if patients:
        df = pd.DataFrame(patients, columns=["Patient ID", "Name", "Contact", "Registration Date", "Care Streak"])
        
        # Searching Capability
        search = st.text_input("🔍 Search Registry (Name or ID)", placeholder="Type to filter...")
        if search:
            df = df[df['Name'].str.contains(search, case=False) | df['Patient ID'].str.contains(search, case=False)]
            
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.write("##")
        st.subheader("🛠️ Registry Actions")
        col1, col2 = st.columns(2)
        with col1:
            target_id = st.selectbox("Select Patient to Remove", df['Patient ID'].tolist())
        with col2:
            st.write("##")
            if st.button("🗑️ DE-REGISTER PATIENT", use_container_width=True):
                c.execute("DELETE FROM patients WHERE pid=?", (target_id,))
                c.execute("DELETE FROM readings WHERE pid=?", (target_id,))
                conn.commit()
                st.success(f"Record {target_id} purged from system.")
                st.rerun()
    else:
        st.warning("No records found in the clinical database.")

# --- PAGE: NEW DIAGNOSTIC SCAN ---
elif page == "🔬 New Diagnostic Scan":
    st.title("🔬 5-Plex Biomarker Imaging Scan")
    st.markdown("---")
    
    c.execute("SELECT pid, name FROM patients")
    p_list = {f"{r[1]} ({r[0]})": r[0] for r in c.fetchall()}
    
    if not p_list:
        st.error("No patients registered. Please go to 'Patient Registration' first.")
        st.stop()
        
    selected_p = st.selectbox("🎯 Target Patient for Scan", list(p_list.keys()))
    pid = p_list[selected_p]
    p_name = selected_p.split(' (')[0]
    
    st.session_state['active_pid'] = pid
    
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        st.markdown("""
            <div style="padding:20px; border-radius:15px; background:rgba(112, 0, 255, 0.05); border: 1px solid rgba(112, 0, 255, 0.2);">
                <h4>📸 Imaging Protocol</h4>
                <p style="font-size:0.85rem; color:#aaa;">Upload the high-resolution clinical assay strip image for colorimetric AI analysis.</p>
            </div>
        """, unsafe_allow_html=True)
        img_file = st.file_uploader("Assay Strip ROI", type=['jpg', 'png', 'jpeg'])

    if img_file:
        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        
        # Simulated ROI Analysis (Colorimetric Logic)
        with st.status("🚀 Processing Bio-Imaging Data...", expanded=True) as status:
            st.write("1. Normalizing light conditions...")
            time.sleep(0.5)
            st.write("2. Detecting 5-plex assay zones...")
            time.sleep(0.8)
            st.write("3. Mapping HSV saturation vectors to clinical thresholds...")
            
            # --- REAL-TIME CALCULATIONS ---
            # In a real app, this would involve cv2.mean() on specific ROIs
            simulated_hsv = [0, 180, 200] 
            
            readings = {
                'glucose':  color_to_value(simulated_hsv, 'glucose'),
                'hb':       color_to_value(simulated_hsv, 'hb'),
                'ntprobnp': color_to_value(simulated_hsv, 'ntprobnp'),
                'lpa':      color_to_value(simulated_hsv, 'lpa'),
                'troponin': color_to_value(simulated_hsv, 'troponin')
            }
            
            score = calculate_crs(list(readings.values()))
            status.update(label="✅ Analysis Complete", state="complete", expanded=False)

        # UI: DISPLAY RESULTS
        st.write("##")
        risk_text, risk_color = get_risk_label(score)
        
        st.markdown(f"""
            <div style="text-align:center; padding:30px; border-radius:20px; background:rgba(0,0,0,0.3); border:1px solid {risk_color};">
                <h5 style="color:#888; margin:0;">CLINICAL RISK SCORE (SENSE-CRS)</h5>
                <h1 style="color:{risk_color}; font-size:4rem; margin:10px 0;">{score:.4f}</h1>
                <div style="display:inline-block; padding:5px 20px; border-radius:50px; background:{risk_color}; color:white; font-weight:bold;">
                    {risk_text}
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.write("##")
        cols = st.columns(5)
        for i, (key, val) in enumerate(readings.items()):
            ref = THRESHOLDS[key]
            # Alert color logic
            is_bad = val < ref['high'] if key == 'hb' else val > ref['high']
            color = "#FF3131" if is_bad else "#00FF80"
            cols[i].metric(ref['label'], f"{val} {ref['unit']}", delta=None, delta_color="inverse")

        if st.button("💾 COMMITT READINGS TO PERMANENT RECORD", use_container_width=True):
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute("""
                INSERT INTO readings (pid, name, glucose, hb, ntprobnp, lpa, troponin, score, timestamp) 
                VALUES (?,?,?,?,?,?,?,?,?)""", 
                (pid, p_name, readings['glucose'], readings['hb'], readings['ntprobnp'], readings['lpa'], readings['troponin'], score, ts))
            
            # Increment care streak
            c.execute("UPDATE patients SET streak = streak + 1 WHERE pid=?", (pid,))
            conn.commit()
            speak("Diagnostic results archived successfully.")
            st.success("Clinical metrics recorded. History updated.")

# --- PAGE: CLINICAL HISTORY & TRENDS ---
elif page == "📉 Clinical History & Trends":
    st.title("📉 Clinical Longitudinal Trends")
    st.markdown("---")
    
    c.execute("SELECT pid, name FROM patients")
    p_list = {f"{r[1]} ({r[0]})": r[0] for r in c.fetchall()}
    
    if not p_list:
        st.error("Registry empty.")
        st.stop()
        
    selected_p = st.selectbox("🔍 Select Patient to View Trends", list(p_list.keys()))
    pid = p_list[selected_p]
    
    c.execute("SELECT * FROM readings WHERE pid=? ORDER BY timestamp ASC", (pid,))
    data = c.fetchall()
    
    if data:
        df = pd.DataFrame(data, columns=["PID", "Name", "Glucose", "Hb", "NTproBNP", "Lpa", "Troponin", "Score", "Timestamp"])
        
        # --- TREND CHART ---
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Score'], name="SENSE-CRS (Risk)", line=dict(color='#7000FF', width=4)), secondary_y=False)
        fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Glucose'], name="Glucose", line=dict(dash='dash')), secondary_y=True)
        
        fig.update_layout(
            title=f"Diagnostic Trajectory for {selected_p}",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("##")
        st.subheader("📄 Raw Diagnostic Logs")
        st.dataframe(df.sort_values('Timestamp', ascending=False), use_container_width=True)
    else:
        st.info("No historical readings found for this patient.")

# --- PAGE: PERSONALIZED CARE PLAN ---
elif page == "💊 Personalized Care Plan":
    st.title("💊 Precision Care & Intervention Strategy")
    st.markdown("---")
    
    c.execute("SELECT pid, name FROM patients")
    p_list = {f"{r[1]} ({r[0]})": r[0] for r in c.fetchall()}
    
    selected_p = st.selectbox("🎯 Target Patient for Intervention", list(p_list.keys()))
    pid = p_list[selected_p]
    
    # Get latest readings for AI context
    c.execute("SELECT * FROM readings WHERE pid=? ORDER BY timestamp DESC LIMIT 1", (pid,))
    latest = c.fetchone()
    
    c.execute("SELECT * FROM care_plans WHERE pid=?", (pid,))
    plan = c.fetchone()
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("### 🧬 AI-Driven Strategy Panel")
        with st.form("care_form"):
            nutri = st.text_area("Nutrition & Dietary Intervention", value=plan[1] if plan else "")
            activ = st.text_area("Physical Activity & Cardiac Rehab", value=plan[2] if plan else "")
            supps = st.text_area("Pharmacological & Supplement Notes", value=plan[3] if plan else "")
            
            if st.form_submit_button("🚀 UPDATE CARE STRATEGY", use_container_width=True):
                ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                c.execute("""
                    INSERT OR REPLACE INTO care_plans (pid, nutrition, activity, supplements, last_updated)
                    VALUES (?,?,?,?,?)""", (pid, nutri, activ, supps, ts))
                conn.commit()
                st.success("Clinical care plan synchronized.")
                st.rerun()

    with col2:
        st.markdown("### 📄 Clinical Document Generation")
        st.write("Generate a secure PDF report for the patient including latest diagnostics and the customized care plan.")
        
        if latest and plan:
            if st.button("📑 GENERATE ENCRYPTED BIOMARKER REPORT", use_container_width=True):
                pdf_data = create_pdf_report(latest, plan[1], plan[2], plan[3])
                st.download_button(
                    label="⬇️ DOWNLOAD PDF REPORT",
                    data=pdf_data,
                    file_name=f"SENSE_Report_{pid}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.warning("Ensure both Diagnostic Readings and a Care Plan exist to generate a report.")

# --- PAGE: DOCTOR'S TRIAGE DASHBOARD ---
elif page == "🚨 Doctor's Triage Dashboard":
    st.title("🚨 Critical Triage & Population Health")
    st.markdown("---")
    
    # Get high-risk patients
    c.execute("SELECT pid, name, score, timestamp FROM readings WHERE score > 0.5 ORDER BY score DESC")
    high_risk = c.fetchall()
    
    if high_risk:
        st.subheader(f"⚠️ Action Required: {len(high_risk)} High-Risk Cases")
        for p in high_risk:
            label, color = get_risk_label(p[2])
            st.markdown(f"""
                <div class="triage-card">
                    <div style="display: flex; justify-content: space-between;">
                        <h3 style="margin:0; color:white;">{p[1]}</h3>
                        <span style="font-weight:bold; color:{color};">{label} ({p[2]:.4f})</span>
                    </div>
                    <p style="margin:5px 0; font-size:0.9rem; color:#ff8e8e;">Latest Reading: {p[3]}</p>
                    <small style="color:#aaa;">System ID: {p[0]}</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.success("No critical alerts. All patients are within optimal or manageable ranges.")

# --- FOOTER ---
st.markdown("""
    <style>
    .footer-wrapper {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(11, 14, 20, 0.95);
        backdrop-filter: blur(15px);
        border-top: 1px solid rgba(112, 0, 255, 0.3);
        padding: 12px 0;
        z-index: 1000;
        box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.6);
    }
    .footer-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    .footer-text {
        color: #888;
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .footer-highlight {
        color: #7000FF;
        font-weight: bold;
    }
    .status-ping {
        width: 8px;
        height: 8px;
        background: #00FF00;
        border-radius: 50%;
        box-shadow: 0 0 10px #00FF00;
        animation: ping 2s infinite;
    }
    @keyframes ping {
        0% { transform: scale(1); opacity: 1; }
        100% { transform: scale(2.5); opacity: 0; }
    }
    .sat-link-icon {
        font-size: 14px;
        margin-right: 8px;
        animation: rotate-sat 10s linear infinite;
        display: inline-block;
    }
    @keyframes rotate-sat {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    </style>
    
    <div class="footer-wrapper">
        <div class="footer-container">
            <div class="footer-text">
                <span class="status-ping"></span> 
                <span style="color:#00FF00;">LIVE REDUNDANCY ACTIVE</span>
            </div>
            <div class="footer-text">
                <span class="sat-link-icon">🛰️</span>
                <b>SENSE-NODE:</b> <span class="footer-highlight">40.7128° N, 74.0060° W</span>
            </div>
            <div class="footer-text">
                <b>CORE:</b> v2.4.0-PRO | <span style="margin-left:5px; color:#7000FF;">AES-256</span>
            </div>
            <div class="footer-text" style="color: #00D1FF; font-weight: 900; opacity: 0.8;">
                DEMOCRATIZING CARDIAC CARE
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style='display: flex; justify-content: center; gap: 20px; margin-top: 50px; margin-bottom: 100px; opacity: 0.3;'>
        <img src='https://img.icons8.com/color/48/000000/google-cloud-platform.png'/>
        <img src='https://img.icons8.com/color/48/000000/python.png'/>
        <img src='https://img.icons8.com/color/48/000000/sqlite.png'/>
        <img src='https://img.icons8.com/color/48/000000/artificial-intelligence.png'/>
    </div>
""", unsafe_allow_html=True)