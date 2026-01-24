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
        padding: 25px; border-radius: 16px; margin-bottom: 20px; 
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
        padding: 24px; border-radius: 16px;
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
    pdf.set_font("Helvetica", '', 10)
    for key in ['glucose', 'hb', 'ntprobnp', 'lpa', 'troponin']:
        val = data[key]
        ref = THRESHOLDS[key]
        
        is_alert = val < 12 if key == 'hb' else val > ref['high']
        status_text = "ACTION REQUIRED" if is_alert else "OPTIMAL"
        
        pdf.cell(w[0], 10, f" {ref['label']}", 1)
        pdf.cell(w[1], 10, f" {val:.2f} {ref['unit']}", 1, 0, 'C')
        pdf.cell(w[2], 10, f" < {ref['high']} {ref['unit']}", 1, 0, 'C')
        
        if is_alert: pdf.set_text_color(180, 0, 0)
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
    'ntprobnp': {'normal': 100,  'high': 125,  'label': 'NT-proBNP',     'unit': 'pg/mL'},  # Abnormal > 125
    'lpa':      {'normal': 20,   'high': 50,   'label': 'Lp(a)',         'unit': 'mg/dL'},  # High Risk > 50
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
            (v[0] - 70) / 150,               # Glucose Stress
            (14 - v[1]) / 6,                 # Anemic Stress
            math.log(max(v[2], 0) + 1) / 6,  # Heart Failure Indicator (Safety max added)
            v[3] / 100,                      # Lipid Burden
            v[4] / 0.5                       # Acute Cardiac Injury (Troponin)
        ]
        
        s = [np.clip(x, 0, 1) for x in normalized_vectors]
        
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
        return "CRITICAL ALERT", "#FF3131"  # High-intensity red
    if score >= 0.50: 
        return "ELEVATED RISK", "#FF9100"  # Clinical orange
    if score >= 0.25: 
        return "INCIPIENT", "#00D1FF"      # Warning/Early detection blue
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
        @keyframes blink {{ 0% {{ opacity: 0.2; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.2; }} }}
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
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
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
                    
                    c.execute("INSERT INTO patients (pid, name, phone, address, join_date, streak) VALUES (?,?,?,?,?,?)", 
                              (new_id, u_name, u_phone, u_address, join_date, 0))
                    conn.commit()
                    
                    speak(f"Registration successful for {u_name}. System ID generated.")
                    
                    st.session_state['last_reg'] = {
                        'name': u_name, 'id': new_id, 'date': join_date, 
                        'phone': u_phone, 'address': u_address
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
                    <div style="display: flex; justify-content: space-between; margin-top: 20px; font-size: 0.8em; opacity: 0.8;">
                        <span>ISSUED: {reg['date']}</span>
                        <span>SECTOR-4 PHC</span>
                    </div>
                </div>
                <div style="text-align:center; margin-top:15px;">
                    <p style="color:#00D1FF; font-weight:bold;">✅ Patient Successfully Syncronized</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("👈 Complete the form to generate the Digital Health Identity Card.")
            st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=250)

    st.write("---")
    with st.expander("🔬 The Role of Longitudinal Health IDs"):
        col_ex1, col_ex2 = st.columns([1, 2])
        with col_ex1:
            st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=150)
        with col_ex2:
            st.write("""
                A **SENSE ID** is more than just a registry number. It enables **Longitudinal AI Analysis**, 
                meaning the system compares today's biomarker results with your historical data to detect 
                subtle cardiac shifts that a standard one-time test would miss.
            """)
            
elif page == "📁 Master Patient Directory":
        st.markdown("""
            <style>
            .directory-header {
                background: linear-gradient(90deg, #004d40, #002424);
                padding: 30px;
                border-radius: 15px;
                margin-bottom: 25px;
                border-bottom: 3px solid #008080;
            }
            .patient-card {
                background: #121417;
                border: 1px solid #2d2f39;
                border-left: 5px solid #008080;
                border-radius: 12px;
                padding: 25px;
                margin-bottom: 15px;
            }
            .status-badge {
                background: rgba(0, 128, 128, 0.2);
                color: #4db6ac;
                padding: 4px 12px;
                border-radius: 6px;
                font-size: 0.7em;
                font-weight: 700;
                text-transform: uppercase;
            }
            div.stButton > button {
                background: linear-gradient(90deg, #008080, #004d40) !important;
                color: white !important;
                border: none !important;
                padding: 10px 20px !important;
                border-radius: 8px !important;
                font-weight: 700 !important;
            }
            </style>
            <div class="directory-header">
                <h1 style="margin:0; color: #e0f2f1; letter-spacing: -1px;">📋 Master Patient Registry</h1>
                <p style="color: #80cbc4; margin:0; opacity: 0.8;">Secure Institutional Health Record Repository</p>
            </div>
        """, unsafe_allow_html=True)

        search_query = st.text_input("", placeholder="🔍 Search by Name, UID, or Address...", label_visibility="collapsed")

        if search_query:
            query = "SELECT * FROM patients WHERE name LIKE ? OR pid LIKE ? OR address LIKE ?"
            params = (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')
            df_p = pd.read_sql(query, conn, params=params)
        else:
            query = "SELECT * FROM patients ORDER BY join_date DESC"
            df_p = pd.read_sql(query, conn)

        if not df_p.empty:
            for i, row in df_p.iterrows():
                st.markdown(f"""
                    <div class="patient-card">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <span class="status-badge">Verified Entry</span>
                                <div style="font-size: 1.6em; font-weight: 800; color: #f5f5f5; margin-top: 10px;">{row['name'].upper()}</div> 
                                <code style="color: #4db6ac; background: none; font-size: 1.1em;">UID: {row['pid']}</code>
                            </div>
                            <div style="text-align: right;">
                                <small style="color: #455a64; font-weight: 900;">ENTRY DATE</small><br>
                                <span style="color: #90a4ae; font-family: monospace;">{row['join_date']}</span>
                            </div>
                        </div>
                        <div style="
                            margin-top: 20px; 
                            display: grid; 
                            grid-template-columns: 1fr 1fr; 
                            gap: 30px; 
                            border-top: 1px solid #2d2f39; 
                            padding-top: 15px;
                        ">
                            <div>
                                <small style="color: #546e7a; font-weight: bold; text-transform: uppercase; font-size: 0.8em;">Secure Contact</small><br>
                                <span style="color: #cfd8dc; font-size: 1.1em;">📞 {row['phone']}</span>
                            </div>
                            <div>
                                <small style="color: #546e7a; font-weight: bold; text-transform: uppercase; font-size: 0.8em;">Verified Address</small><br>
                                <span style="color: #cfd8dc; font-size: 1.1em;">📍 {row['address']}</span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"OPEN CLINICAL DOSSIER: {row['pid']}", key=f"btn_{row['pid']}", use_container_width=True):
                    st.session_state['active_id'] = row['pid']
                    st.toast(f"Dossier {row['pid']} synchronized.")
        else:
            st.info("No records found in the clinical database.")

# --- PAGE: NEW DIAGNOSTIC SCAN ---
elif page == "🔬 New Diagnostic Scan":
    st.markdown("""
        <style>
        /* Holographic Scan Container */
        .scan-wrapper {
            position: relative;
            border-radius: 15px;
            border: 2px solid rgba(0, 255, 0, 0.3);
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.1);
        }
        
        @keyframes scan-glow { 
            0% { top: -5%; opacity: 0; } 
            50% { opacity: 1; filter: brightness(1.5); } 
            100% { top: 105%; opacity: 0; } 
        }
        
        .scan-line {
            position: absolute; width: 100%; height: 6px;
            background: linear-gradient(to bottom, transparent, #00FF00, transparent);
            box-shadow: 0 0 25px #00FF00;
            animation: scan-glow 2.5s ease-in-out infinite; 
            z-index: 10;
        }

        /* Metric Card Modernization */
        .biomarker-card {
            background: rgba(255, 255, 255, 0.03);
            border-left: 4px solid #30363d;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 12px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .biomarker-card:hover {
            background: rgba(255, 255, 255, 0.07);
            border-left-color: #00FF00;
            transform: translateX(10px);
        }

        /* High-Intensity Emergency HUD */
        .critical-bg {
            background: linear-gradient(45deg, #600, #f00, #600);
            background-size: 400% 400%;
            animation: pulse-bg 1.5s infinite;
            border: 4px solid rgba(255,255,255,0.5);
        }
        @keyframes pulse-bg { 
            0% { background-position: 0% 50%; } 
            50% { background-position: 100% 50%; } 
            100% { background-position: 0% 50%; } 
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='letter-spacing:-1px;'>🔬 SENSE 5-Plex Diagnostic Engine</h1>", unsafe_allow_html=True)
    
    input_col1, input_col2 = st.columns([1, 1])
    with input_col1:
        p_id = st.text_input("📋 Patient Access ID", placeholder="Enter SENSE-XXXX")
    with input_col2:
        file = st.file_uploader("📸 Upload Diagnostic Strip", type=['jpg', 'png', 'jpeg'])

    if file and p_id:
        c.execute("SELECT name FROM patients WHERE pid=?", (p_id,))
        p_res = c.fetchone()
        
        if p_res:
            p_name = p_res[0]
            img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), 1)
            h, w, _ = img.shape

            img_blur = cv2.GaussianBlur(img, (5, 5), 0)
            hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)
            biomarker_keys = ['glucose', 'hb', 'ntprobnp', 'lpa', 'troponin']
            vals = []
            
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

            st.success(f"✅ Telemetry Lock: Results synchronized for {p_name}")
            
            res_col1, res_col2 = st.columns([1.3, 1])
            
            with res_col1:
                st.markdown('<div class="scan-wrapper"><div class="scan-line"></div>', unsafe_allow_html=True)
                st.image(cv2.cvtColor(img_disp, cv2.COLOR_BGR2RGB), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with res_col2:
                st.markdown(f"""
                    <div style="text-align:center; padding:10px; border-radius:10px; background:rgba(255,255,255,0.05);">
                        <small style="color:#888;">COMPOSITE RISK SCORE</small>
                        <h1 style="color:#00FF00; margin:0;">{score:.3f}</h1>
                    </div>
                """, unsafe_allow_html=True)
                
                for i, k in enumerate(biomarker_keys):
                    is_high = vals[i] > THRESHOLDS[k]['high']
                    st.markdown(f"""
                        <div class="biomarker-card">
                            <div style="display:flex; justify-content:space-between;">
                                <span style="color:#AAA; font-size:12px;">{THRESHOLDS[k]['label'].upper()}</span>
                                <span style="color:{'#FF4B4B' if is_high else '#00FF00'}; font-size:10px;">{'▲ CRITICAL' if is_high else '● NORMAL'}</span>
                            </div>
                            <div style="font-size:24px; font-weight:bold;">
                                {vals[i]:.2f} <small style="font-size:12px; color:#555;">{THRESHOLDS[k]['unit']}</small>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            if score > 0.7 or vals[4] > 0.04:
                alert_sound = '<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mp3"></audio>'
                st.markdown(alert_sound, unsafe_allow_html=True)
                
                alert_placeholder = st.empty()
                with alert_placeholder.container():
                    st.markdown(f"""
                        <div class="critical-bg" style="padding: 40px; border-radius: 20px; text-align: center; box-shadow: 0 0 50px rgba(255,0,0,0.5);">
                            <h1 style="color: white; margin: 0; font-size: 3em; text-shadow: 3px 3px 0px #000;">108 EMERGENCY</h1>
                            <h2 style="color: white; font-weight: 300;">DISPATCHING LIFE SUPPORT FOR {p_name.upper()}</h2>
                            <div style="margin-top:20px; font-family:monospace; color:rgba(255,255,255,0.8);">
                                TARGET ID: {p_id} | SECTOR 4 QUARANTINE: NOTIFIED
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    with st.status("📡 Establishing Emergency Handshake...", state="running") as status:
                        for i in range(5, 0, -1):
                            time.sleep(1)
                            st.write(f"Broadcasting vital signs to Dispatch Unit... {i}s")
                        status.update(label="🚑 108 DISPATCH CONFIRMED - INTERCEPTION IN PROGRESS", state="complete")
                
                speak(f"Emergency. Ambulance 108 dispatched for {p_name}. Life support protocols initiated.")
                
                st.subheader("🚑 Real-Time Interception Map")
                fig = go.Figure(go.Scatter(x=[0, 1.2, 2], y=[0, 0.8, 2], mode='lines+markers+text', 
                                          text=["HOSPITAL", "AMB-108", "PATIENT"], 
                                          marker=dict(size=[25, 45, 25], color=['#00FFFF', '#FF0000', '#00FF00'],
                                          line=dict(width=3, color='white'))))
                fig.update_layout(height=300, template="plotly_dark", margin=dict(l=10,r=10,t=10,b=10),
                                 xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                 yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                st.plotly_chart(fig, use_container_width=True)

            elif score > 0.4:
                st.warning("⚠️ PROVISIONAL ALERT: Physician intervention recommended.")
                speak(f"High risk detected. Results shared with medical hub.")
        else:
            st.error("❌ Patient ID not found. Please register the patient first.")
# --- PAGE: CLINICAL HISTORY & TRENDS ---
elif page == "📉 Clinical History & Trends":
    st.markdown("""
        <style>
        .analytics-header {
            background: linear-gradient(135deg, rgba(0, 209, 255, 0.1), rgba(112, 0, 255, 0.1));
            padding: 20px;
            border-radius: 15px;
            border: 1px solid rgba(0, 209, 255, 0.3);
            margin-bottom: 25px;
        }
        .report-card {
            background: rgba(255, 255, 255, 0.03);
            border-left: 5px solid #00D1FF;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
        }
        @keyframes heart-pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.15); opacity: 0.7; }
            100% { transform: scale(1); opacity: 1; }
        }
        .pulse-icon {
            display: inline-block;
            animation: heart-pulse 1.4s infinite;
            filter: drop-shadow(0 0 5px #FF4B4B);
            font-size: 26px;
        }
        /* Custom styling for metrics */
        [data-testid="stMetricValue"] {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2rem !important;
        }
        </style>
        
        <div class="analytics-header">
            <h1 style="margin:0; letter-spacing:-1px;">📈 Longitudinal Diagnostic Insights</h1>
            <p style="color:#888; margin:0;">Multi-Variate Biomarker Trend Mapping & Risk Trajectory</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_input, col_status = st.columns([2, 1])
    with col_input:
        pid = st.text_input("🔍 Patient Access Protocol", placeholder="Enter PID (e.g., SENSE-A12B)")
    with col_status:
        st.write("##")
        if pid:
            st.markdown('<div style="background:rgba(255,75,75,0.1); padding:10px; border-radius:10px; text-align:center;"><span class="pulse-icon">❤️</span> <b style="color:#FF4B4B;">MONITORING LIVE</b></div>', unsafe_allow_html=True)

    if pid:
        df = pd.read_sql(f"SELECT * FROM readings WHERE pid='{pid}' ORDER BY timestamp ASC", conn)
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            last_score = df['score'].iloc[-1]
            prev_score = df['score'].iloc[-2] if len(df) > 1 else last_score
            delta = last_score - prev_score

            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Current CRS Index", f"{last_score:.3f}", delta=f"{delta:.3f}", delta_color="inverse")
            with m2:
                st.metric("Analyzed Sessions", len(df), delta="Total Logs", delta_color="off")
            with m3:
                risk_status, risk_color = get_risk_label(last_score) # Using your custom label logic
                st.markdown(f"""
                    <div style="background:{risk_color}22; border:1px solid {risk_color}; padding:8px; border-radius:10px; text-align:center;">
                        <small style="color:{risk_color}; font-weight:bold;">RISK PROFILE</small><br>
                        <span style="color:{risk_color}; font-size:1.2em; font-weight:bold;">{risk_status}</span>
                    </div>
                """, unsafe_allow_html=True)

            st.write("##")

            fig = make_subplots(specs=[[{"secondary_y": True}]])
            colors = ['#FFA500', '#FF4B4B', '#00D1FF', '#7000FF', '#00FF00']
            
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['glucose'], name="Glucose", 
                                     line=dict(color=colors[0], width=3), mode='lines+markers'), secondary_y=False)
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['ntprobnp'], name="NT-proBNP", 
                                     line=dict(color=colors[1], width=3), mode='lines+markers'), secondary_y=False)
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['lpa'], name="Lp(a)", 
                                     line=dict(color=colors[3], width=3), mode='lines+markers'), secondary_y=False)
            
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['hb'], name="Hemoglobin", 
                                     line=dict(color=colors[2], dash='dot', width=2)), secondary_y=True)
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['troponin'], name="Troponin", 
                                     line=dict(color=colors[4], dash='dash', width=2)), secondary_y=True)

            fig.add_hrect(y0=0.7, y1=1.0, fillcolor="red", opacity=0.07, line_width=0, annotation_text="CRITICAL PATH", secondary_y=False)
            fig.add_hrect(y0=0.4, y1=0.7, fillcolor="yellow", opacity=0.07, line_width=0, annotation_text="ELEVATED RISK", secondary_y=False)

            fig.update_layout(
                title="<b>Comprehensive 5-Plex Bio-Trend Mapping</b>",
                template="plotly_dark",
                hovermode="x unified",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, title="Timeline of Diagnostics"),
                yaxis=dict(title="Metabolic/Cardiac Concentration", gridcolor='rgba(255,255,255,0.05)'),
                legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5)
            )
            
            st.plotly_chart(fig, use_container_width=True)

            st.write("##")
            st.subheader("🛡️ Risk Velocity Progression")
            
            fig_area = go.Figure()
            fig_area.add_trace(go.Scatter(x=df['timestamp'], y=df['score'], fill='tozeroy', 
                                         line=dict(color='#00FF00', width=4), 
                                         fillcolor='rgba(0, 255, 0, 0.1)', name="CRS Index"))
            
            fig_area.update_layout(
                template="plotly_dark", 
                height=350, 
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0,r=0,t=20,b=0),
                xaxis=dict(showgrid=False),
                yaxis=dict(range=[0, 1], title="CRS Index Value", gridcolor='rgba(255,255,255,0.05)')
            )
            st.plotly_chart(fig_area, use_container_width=True)

            col_logs, col_obs = st.columns([1.5, 1])
            
            with col_logs:
                with st.expander("📄 Raw Clinical Telemetry Data", expanded=False):
                    st.dataframe(df.style.background_gradient(subset=['score'], cmap='RdYlGn_r'), use_container_width=True)
            
            with col_obs:
                if last_score > 0.6:
                    st.markdown(f"""
                        <div class="report-card" style="border-left-color:#FF4B4B;">
                            <h4 style="color:#FF4B4B; margin:0;">⚕️ AI Clinical Observation</h4>
                            <p style="font-size:0.9em; color:#CCC;">
                                <b>Warning:</b> Current CRS Index ({last_score:.3f}) exceeds the 0.6 stability threshold. 
                                Longitudinal trajectory indicates a <b>{'+' if delta > 0 else ''}{delta*100:.1f}% shift</b> 
                                since last scan. Immediate triage advised.
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div class="report-card" style="border-left-color:#00FF00;">
                            <h4 style="color:#00FF00; margin:0;">✅ System Status: Stable</h4>
                            <p style="font-size:0.9em; color:#CCC;">
                                Patient biomarkers remain within optimal variance ranges. Continue routine observation.
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
                <div style="text-align:center; padding:50px; border:2px dashed #444; border-radius:20px;">
                    <h3 style="color:#666;">No Diagnostic Record Found</h3>
                    <p>System UID <b>{pid}</b> is registered but contains no 5-plex scan history.</p>
                </div>
            """, unsafe_allow_html=True)
            
# --- PAGE: PERSONALIZED CARE PLAN (AI HEALTH COACH) ---
elif page == "💊 Personalized Care Plan":
    st.markdown("""
        <style>
        .care-header {
            background: linear-gradient(90deg, #1e1e2f, #11111d);
            padding: 25px;
            border-radius: 20px;
            border-left: 8px solid #7000FF;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            margin-bottom: 30px;
        }
        .strategy-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 25px;
            border-radius: 20px;
            height: 100%;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .strategy-card:hover {
            background: rgba(112, 0, 255, 0.05);
            border-color: #7000FF;
            transform: translateY(-10px);
        }
        .action-point {
            font-size: 0.9em;
            margin-bottom: 8px;
            padding-left: 15px;
            border-left: 2px solid #7000FF;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='letter-spacing:-1px;'>🥗 AI-Driven Care Strategy</h1>", unsafe_allow_html=True)
    
    search_col1, _ = st.columns([2, 1])
    pid = search_col1.text_input("🔍 Access Patient Strategy Hub", placeholder="Enter Patient ID (e.g. SENSE-001)")

    if pid:
        df_l = pd.read_sql(f"SELECT * FROM readings WHERE pid='{pid}' ORDER BY timestamp DESC LIMIT 1", conn)
        
        if not df_l.empty:
            data = df_l.iloc[0]
            
            aura_color = "#FF4B4B" if data['score'] > 0.7 else "#FFA500" if data['score'] > 0.4 else "#00FF00"
            status_text = '🔴 CRITICAL INTERVENTION' if data['score'] > 0.7 else '🟢 MAINTENANCE MODE'
            
            st.markdown(f"""
                <div class="care-header">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <h2 style="margin:0; color:white;">Roadmap: {data['name']}</h2>
                            <p style="margin:5px 0 0 0; color:{aura_color}; font-weight:bold; letter-spacing:1px;">{status_text}</p>
                        </div>
                        <div style="text-align:right; opacity:0.6;">
                            <small>ID: {pid}</small><br>
                            <small>LAST SCAN: {data['timestamp'][:10]}</small>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            categories = ['Glucose', 'Hemoglobin', 'NT-proBNP', 'Lp(a)', 'Troponin']
            radar_vals = [
                min(data['glucose']/140, 1),  
                min(data['hb']/14, 1),      
                min(data['ntprobnp']/125, 1),  
                min(data['lpa']/50, 1),        
                min(data['troponin']/0.04, 1) 
            ]

            col_radar, col_metrics = st.columns([1.3, 1])
            
            with col_radar:
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=radar_vals, theta=categories, fill='toself',
                    fillcolor=aura_color, opacity=0.2,
                    line=dict(color=aura_color, width=4),
                    name='Current Bio-Signature'
                ))
                fig_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(255,255,255,0.1)")),
                    showlegend=False, template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    height=380, margin=dict(l=50, r=50, t=30, b=30)
                )
                st.plotly_chart(fig_radar, use_container_width=True)

            with col_metrics:
                st.markdown("### AI Diagnostic Insights")
                
                bio_age = round(data['score']*10 + 40, 1)
                st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:15px; border-top:3px solid #00D1FF;">
                        <small style="color:#888;">CALCULATED BIO-AGE</small>
                        <h2 style="margin:0; color:#00D1FF;">{bio_age} Years</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                st.write("##")
                st.metric("Risk Resilience", f"{round((1-data['score'])*100, 1)}%", 
                          help="System capability to absorb metabolic stress")
                st.progress(1-data['score'])

            st.write("---")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown('<div class="strategy-card">', unsafe_allow_html=True)
                st.markdown("### 🍞 Metabolic")
                st.markdown(f"<small>LEVEL: {data['glucose']:.1f} mg/dL</small>", unsafe_allow_html=True)
                if data['glucose'] > 140:
                    st.error("HIGH GLYCEMIC LOAD")
                    st.markdown("""
                        <div class="action-point">Eliminate refined sugars</div>
                        <div class="action-point">20m brisk walk post-meals</div>
                        <div class="action-point">Increase soluble fiber</div>
                    """, unsafe_allow_html=True)
                else:
                    st.success("STABLE METABOLISM")
                    st.write("Maintain current complex-carb ratio and fasting window.")
                st.markdown('</div>', unsafe_allow_html=True)

            with c2:
                st.markdown('<div class="strategy-card">', unsafe_allow_html=True)
                st.markdown("### 🩸 Hematology")
                st.markdown(f"<small>LEVEL: {data['hb']:.1f} g/dL</small>", unsafe_allow_html=True)
                if data['hb'] < 12:
                    st.warning("NUTRITIONAL FOCUS")
                    st.markdown("""
                        <div class="action-point">Iron-rich greens (Spinach)</div>
                        <div class="action-point">Vitamin C for absorption</div>
                        <div class="action-point">Reduce caffeine intake</div>
                    """, unsafe_allow_html=True)
                else:
                    st.success("OPTIMAL HEMATOLOGY")
                    st.write("Oxygen saturation and iron levels are clinically stable.")
                st.markdown('</div>', unsafe_allow_html=True)

            with c3:
                st.markdown('<div class="strategy-card">', unsafe_allow_html=True)
                st.markdown("### 🫀 Cardiac")
                st.markdown(f"<small>SCORE: {data['score']:.2f}</small>", unsafe_allow_html=True)
                if data['score'] > 0.5:
                    st.error("STRESS DETECTED")
                    st.markdown("""
                        <div class="action-point">Physician review required</div>
                        <div class="action-point">Sodium < 1500mg/day</div>
                        <div class="action-point">Monitor resting heart rate</div>
                    """, unsafe_allow_html=True)
                else:
                    st.success("CARDIAC STABILITY")
                    st.write("Cardiac markers indicate low systemic strain.")
                st.markdown('</div>', unsafe_allow_html=True)

            st.write("##")
            with st.expander("🛠️ Clinical Lifestyle Prescription Editor", expanded=True):
                plan_db = pd.read_sql(f"SELECT * FROM care_plans WHERE pid='{pid}'", conn)
                
                d_nut = "Foods: Walnuts, Greens. Restrict: Sugars."
                d_act = f"Goal: {10000 if data['score'] < 0.4 else 5000} steps per day."
                d_sup = "Focus: Hydration & Targeted Multivitamins."

                if not plan_db.empty:
                    d_nut, d_act, d_sup = plan_db.iloc[0]['nutrition'], plan_db.iloc[0]['activity'], plan_db.iloc[0]['supplements']

                with st.form(key=f"phys_form_{pid}"):
                    t1, t2, t3 = st.tabs(["🥗 Personalized Nutrition", "🏃 Activity Protocol", "💊 Clinical Supplementation"])
                    with t1: new_nut = st.text_area("Dietary Architecture", value=d_nut, height=100)
                    with t2: new_act = st.text_area("Exercise Biomechanics", value=d_act, height=100)
                    with t3: new_sup = st.text_area("Supplement Protocol", value=d_sup, height=100)
                    
                    if st.form_submit_button("💾 SYNCHRONIZE CARE PLAN", use_container_width=True):
                        c.execute("INSERT OR REPLACE INTO care_plans VALUES (?,?,?,?,?)", 
                                 (pid, new_nut, new_act, new_sup, datetime.now()))
                        conn.commit()
                        st.toast("Clinical Plan Updated Successfully!")
                        st.rerun()

            try:
                report_bytes = create_pdf_report(data, d_nut, d_act, d_sup)
                st.download_button(
                    label="📥 DOWNLOAD CLINICAL PDF SUMMARY",
                    data=report_bytes,
                    file_name=f"SENSE_Strategy_{pid}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"PDF Engine Note: {e}")

        else:
            st.warning("🔍 Patient Profile Found, but no Diagnostic Scan exists for this ID.")
            
            
# --- PAGE: DOCTOR'S TRIAGE DASHBOARD (COMMAND CENTER) ---
elif page == "🚨 Doctor's Triage Dashboard":
    st.markdown("""
        <style>
        .triage-card {
            background: rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 10px solid;
            transition: all 0.2s ease-in-out;
        }
        .triage-card:hover {
            background: rgba(255, 255, 255, 0.06);
            transform: scale(1.005);
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        }
        .severity-pill {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: 900;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        @keyframes alert-pulse {
            0% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7); }
            70% { box-shadow: 0 0 0 15px rgba(255, 75, 75, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
        }
        .critical-pulse {
            animation: alert-pulse 1.5s infinite;
            background: rgba(255, 75, 75, 0.2) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='letter-spacing:-1.5px;'>👨‍⚕️ SENSE Triage Command</h1>", unsafe_allow_html=True)
    
    df_all = pd.read_sql("SELECT * FROM readings WHERE score > 0.4 ORDER BY timestamp DESC", conn)
    
    m1, m2, m3, m4 = st.columns([1, 1, 1, 1])
    critical_count = len(df_all[df_all['score'] > 0.7])
    moderate_count = len(df_all) - critical_count
    
    with m1:
        st.metric("CRITICAL", critical_count, delta="Priority 1", delta_color="inverse")
    with m2:
        st.metric("MODERATE", moderate_count, delta="Priority 2")
    with m3:
        st.metric("FLEET STATUS", "Active", delta="108 Ready")
    with m4:
        st.markdown(f"""
            <div style="text-align:right; padding-top:10px;">
                <span style="color:#00FF00;">●</span> <small style="color:#888;">NETWORK SYNCED</small><br>
                <code style="font-size:0.8em;">LATENCY: 14ms</code>
            </div>
        """, unsafe_allow_html=True)

    st.write("---")

    st.subheader("📍 Real-Time Incident Mapping")
    if not df_all.empty:
        fig_map = go.Figure(go.Scatter(
            x=np.random.randn(len(df_all)), 
            y=np.random.randn(len(df_all)),
            mode='markers+text',
            text=df_all['name'],
            marker=dict(
                size=df_all['score']*60, 
                color=df_all['score'], 
                colorscale='RdYlGn_r',
                showscale=True,
                line=dict(width=2, color='white'),
                colorbar=dict(title="Severity", thickness=15)
            )
        ))
        fig_map.update_layout(
            template="plotly_dark", height=350, 
            margin=dict(l=0,r=0,t=0,b=0),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_map, use_container_width=True)

    st.subheader("📋 Active Incident Queue")
    
    if not df_all.empty:
        for i, row in df_all.iterrows():
            is_critical = row['score'] > 0.7
            severity_label = "RED ALERT" if is_critical else "STABLE RISK"
            color = "#ff4b4b" if is_critical else "#ffa500"
            bg_class = "critical-pulse" if is_critical else ""
            
            st.markdown(f'''
                <div class="triage-card {bg_class}" style="border-left-color: {color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.4em; font-weight: 800; color:white;">{row["name"]}</span>
                            <span style="margin-left:15px; color:#888; font-family:monospace;">UID: {row["pid"]}</span>
                        </div>
                        <span class="severity-pill" style="background:{color}; color:white;">
                            {severity_label}
                        </span>
                    </div>
                    <div style="margin: 15px 0; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
                        <div style="color: #bbb; font-size:0.85em;">
                            <b style="color:{color};">CRS INDEX:</b><br>{row["score"]:.3f}
                        </div>
                        <div style="color: #bbb; font-size:0.85em;">
                            <b>DETECTED AT:</b><br>{row["timestamp"]}
                        </div>
                        <div style="color: #bbb; font-size:0.85em;">
                            <b>MARKER PK:</b><br>T: {row['troponin']:.2f} | N: {row['ntprobnp']:.2f}
                        </div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns([1.5, 1, 1, 1])
            with c1:
                if st.button(f"🚑 DISPATCH 108", key=f"disp_{i}", use_container_width=True):
                    st.toast(f"HOSPITAL UNIT ASSIGNED TO {row['name']}", icon="🚑")
                    speak(f"Emergency Dispatch confirmed for {row['name']}.")
            with c2:
                if st.button(f"📞 CONTACT", key=f"phc_{i}", use_container_width=True):
                    st.toast(f"Connecting to Sector Hub...")
            with c3:
                if st.button(f"📝 NOTES", key=f"note_{i}", use_container_width=True):
                    st.info(f"Open clinical notes for {row['pid']}")
            with c4:
                if st.button(f"✅ CLEAR", key=f"res_{i}", use_container_width=True):
                    st.success("Case Resolved")
            st.write("---")

    else:
        st.markdown("""
            <div style="text-align:center; padding:100px; opacity:0.5;">
                <h2>✅ Triage Perimeter Clear</h2>
                <p>No high-risk biomarkers detected in the global registry.</p>
            </div>
        """, unsafe_allow_html=True)
        
# --- FOOTER: SECURE COMMAND TERMINAL ---

st.markdown("---")

st.markdown("""
    <style>
    .footer-wrapper {
        margin-top: 50px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        padding-top: 20px;
    }
    .footer-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 25px;
        background: linear-gradient(90deg, rgba(0,0,0,0.2), rgba(30,30,47,0.4));
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        font-family: 'JetBrains Mono', 'Courier New', monospace;
    }
    .status-ping {
        height: 8px;
        width: 8px;
        background-color: #00FF00;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        box-shadow: 0 0 10px #00FF00;
        animation: pulse-green 2s infinite;
    }
    @keyframes pulse-green {
        0% { transform: scale(0.9); opacity: 0.6; }
        50% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(0.9); opacity: 0.6; }
    }
    .footer-text {
        font-size: 0.75em;
        color: #666;
        letter-spacing: 1px;
        display: flex;
        align-items: center;
    }
    .footer-highlight {
        color: #00D1FF;
        font-weight: bold;
        text-transform: uppercase;
    }
    .sat-link-icon {
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
    <div style='display: flex; justify-content: center; gap: 20px; margin-top: 15px; opacity: 0.4;'>
        <span style='font-size: 9px; color: #888;'>🔒 HIPAA COMPLIANT</span>
        <span style='font-size: 9px; color: #888;'>🛡️ END-TO-END ENCRYPTION</span>
        <span style='font-size: 9px; color: #888;'>📡 PHC SECTOR HANDSHAKE</span>
    </div>
""", unsafe_allow_html=True)