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
st.set_page_config(page_title="SENSE AI | Precision Health Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    .triage-card { 
        padding: 20px; border-radius: 10px; margin-bottom: 15px; 
        background-color: #1c2128; border-left: 8px solid #ff4b4b;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    .recommendation-box {
        padding: 15px; border-radius: 8px; border: 1px solid #30363d;
        background-color: #0d1117; height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ASSETS & DATABASE ---
def add_logo():
    if os.path.exists("LOGO.JPG"):
        st.sidebar.image("LOGO.JPG", use_container_width=True)

def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        filename = f"temp_voice_{uuid.uuid4().hex}.mp3"
        tts.save(filename)
        with open(filename, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(md, unsafe_allow_html=True)
        os.remove(filename) 
    except Exception as e:
        st.error(f"Voice Error: {e}")

conn = sqlite3.connect('sense_health.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS patients (pid TEXT PRIMARY KEY, name TEXT, join_date TEXT, streak INTEGER)')
c.execute('CREATE TABLE IF NOT EXISTS readings (pid TEXT, name TEXT, glucose REAL, hb REAL, ntprobnp REAL, lpa REAL, troponin REAL, score REAL, timestamp TEXT)')
conn.commit()

# --- 3. ANALYTICS ENGINE ---
THRESHOLDS = {
    'glucose':  {'normal': 100, 'high': 200, 'label': 'Blood Glucose'},
    'hb':       {'normal': 14,  'high': 8,   'label': 'Hemoglobin'},
    'ntprobnp': {'normal': 100, 'high': 500, 'label': 'NT-proBNP'},
    'lpa':      {'normal': 20,  'high': 100, 'label': 'Lp(a)'},
    'troponin': {'normal': 0.01, 'high': 0.5, 'label': 'Troponin I'}
}

def color_to_value(hsv_mean, biomarker):
    norm_score = np.clip(hsv_mean[1] / 255.0, 0, 1)
    t = THRESHOLDS[biomarker]
    if biomarker == 'hb':
        return t['normal'] - (norm_score * (t['normal'] - t['high']))
    return t['normal'] + (norm_score * (t['high'] - t['normal']))

def calculate_crs(vals):
    s = [(vals[0]-70)/150, (14-vals[1])/6, log(vals[2]+1)/6, vals[3]/100, vals[4]/0.5]
    s = [np.clip(x, 0, 1) for x in s]
    return (0.3*s[0]) + (0.25*s[1]) + (0.2*s[2]) + (0.15*s[3]) + (0.1*s[4])

# --- 4. NAVIGATION ---
add_logo()
st.sidebar.title("SENSE AI Portal")
page = st.sidebar.selectbox("Select View", 
    ["Patient Registration", "New Diagnostic Scan", "Clinical History & Trends", "Personalized Care Plan", "Doctor's Triage Dashboard"])

# --- PAGE: REGISTRATION ---
if page == "Patient Registration":
    st.title("📋 Patient Onboarding")
    with st.form("reg_form"):
        u_name = st.text_input("Full Legal Name")
        if st.form_submit_button("Register & Generate ID"):
            new_id = f"SENSE-{uuid.uuid4().hex[:6].upper()}"
            c.execute("INSERT INTO patients VALUES (?,?,?,?)", (new_id, u_name, datetime.now().strftime('%Y-%m-%d'), 0))
            conn.commit()
            st.success(f"Registered: {u_name} | ID: {new_id}")

# --- PAGE: LIVE SCAN (PAD DETECTION USING V2 ROI LOGIC) ---
elif page == "New Diagnostic Scan":
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

            # Optional denoise for crayon/marker textures
            img_blur = cv2.GaussianBlur(img, (5, 5), 0)
            hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)

            biomarker_keys = ['glucose', 'hb', 'ntprobnp', 'lpa', 'troponin']
            vals = []

            # --- Spacing-based ROI detection (horizontal pads) ---
            start_x  = int(w * 0.05)
            spacing  = int(w * 0.18)
            pad_w    = int(w * 0.12)
            pad_h    = int(h * 0.40)
            y_pos    = int(h * 0.30)

            img_disp = img.copy()
            for i, k in enumerate(biomarker_keys):
                x = start_x + (i * spacing)
                x2 = min(x + pad_w, w)
                y2 = min(y_pos + pad_h, h)
                roi = hsv[y_pos:y2, x:x2]
                if roi.size > 0:
                    val = color_to_value(np.mean(roi, axis=(0,1)), k)
                    vals.append(val)
                    cv2.rectangle(img_disp, (x, y_pos), (x2, y2), (0, 255, 0), 3)
                    cv2.putText(img_disp, k.upper(), (x, y_pos-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
                else:
                    vals.append(THRESHOLDS[k]['normal'])

            # Guarantee exactly 5 values
            if len(vals) < 5:
                vals += [THRESHOLDS[k]['normal'] for k in biomarker_keys[len(vals):]]
            vals = vals[:5]

            score = calculate_crs(vals)
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute("INSERT INTO readings VALUES (?,?,?,?,?,?,?,?,?)", 
                      (p_id, p_name, vals[0], vals[1], vals[2], vals[3], vals[4], score, ts))
            conn.commit()

            st.success(f"Analysis Recorded for {p_name}")
            col_a, col_b = st.columns([1.5, 1])
            with col_a: 
                st.image(cv2.cvtColor(img_disp, cv2.COLOR_BGR2RGB), caption="Pad Detection (ROI method)")
            with col_b:
                st.metric("SENSE-CRS Index", f"{score:.3f}")
                st.dataframe(pd.DataFrame({"Marker": biomarker_keys, "Value": [round(v,2) for v in vals]}))

            if vals[4] > 0.4:
                speak(f"Emergency. High Troponin detected for {p_name}. Alerting medical team.")
            else:
                speak(f"Analysis complete for {p_name}. Your score is {round(score,2)}.")
        else:
            st.error("Patient ID not found. Register first.")
    elif file and not p_id:
        st.warning("Enter Patient ID first!")

# --- PAGE: CLINICAL HISTORY ---
elif page == "Clinical History & Trends":
    st.title("📈 Longitudinal Diagnostic Insights")
    pid = st.text_input("Patient ID Lookup")
    if pid:
        df = pd.read_sql(f"SELECT * FROM readings WHERE pid='{pid}' ORDER BY timestamp ASC", conn)
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            colors = ['#FFA500', '#FF4B4B', '#00D1FF', '#7000FF', '#00FF00']
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['glucose'], name="Glucose", line=dict(color=colors[0], width=4)), secondary_y=False)
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['ntprobnp'], name="NT-proBNP", line=dict(color=colors[1], width=4)), secondary_y=False)
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['lpa'], name="Lp(a)", line=dict(color=colors[3], width=4)), secondary_y=False)
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['hb'], name="Hemoglobin", line=dict(color=colors[2], dash='dot')), secondary_y=True)
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['troponin'], name="Troponin", line=dict(color=colors[4], dash='dash')), secondary_y=True)
            fig.update_layout(title="Complete 5-Plex Trend Analysis", template="plotly_dark", hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
            st.subheader("SENSE-CRS Risk Progression")
            st.area_chart(df.set_index('timestamp')['score'])
        else:
            st.info("No records found.")

# --- PAGE: CARE PLAN ---
elif page == "Personalized Care Plan":
    st.title("🥗 AI Care Strategy")
    pid = st.text_input("Search ID")
    if pid:
        df_l = pd.read_sql(f"SELECT * FROM readings WHERE pid='{pid}' ORDER BY timestamp DESC LIMIT 1", conn)
        if not df_l.empty:
            data = df_l.iloc[0]
            st.subheader(f"Strategy Roadmap: {data['name']}")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown('<div class="recommendation-box">### 🍞 Metabolic</div>', unsafe_allow_html=True)
                st.write(f"Glucose: {data['glucose']:.1f}")
                if data['glucose'] > 140: 
                    st.warning("High risk. Switch to low-GI diet.")
                else: 
                    st.success("Target achieved.")
            with c2:
                st.markdown('<div class="recommendation-box">### 🩸 Hematology</div>', unsafe_allow_html=True)
                st.write(f"Hemoglobin: {data['hb']:.1f}")
                if data['hb'] < 12: 
                    st.info("Anemia detected. Iron-rich foods + Vitamin C.")
                else: 
                    st.success("Optimal range.")
            with c3:
                st.markdown('<div class="recommendation-box">### 🫀 Cardiac</div>', unsafe_allow_html=True)
                st.write(f"Risk Score: {data['score']:.2f}")
                if data['score'] > 0.5: 
                    st.error("Cardiac stress detected. Immediate GP consultation.")
                else: 
                    st.success("Stable.")
        else:
            st.info("No recent data.")

# --- PAGE: DOCTOR DASHBOARD ---
elif page == "Doctor's Triage Dashboard":
    st.title("👨‍⚕️ PHC Administrative Hub")
    df_all = pd.read_sql("SELECT pid, name, score, timestamp FROM readings WHERE score > 0.4 ORDER BY timestamp DESC", conn)
    if not df_all.empty:
        for i, row in df_all.iterrows():
            severity = "CRITICAL" if row['score'] > 0.7 else "MODERATE"
            color = "#ff4b4b" if severity == "CRITICAL" else "#ffa500"
            st.markdown(f'''
                <div class="triage-card" style="border-left-color: {color};">
                    <h3>{severity}: {row["name"]}</h3>
                    <p>ID: <b>{row["pid"]}</b> | Risk: <b>{row["score"]:.3f}</b> | {row["timestamp"]}</p>
                </div>
            ''', unsafe_allow_html=True)
            btn_key = f"notify_{row['pid']}_{i}"
            if st.button(f"Notify Dispatch for {row['name']}", key=btn_key):
                st.toast(f"Ambulance signaled for {row['name']}")
    else:
        st.success("Triage Clear.")

# --- FOOTER ---
st.markdown("---")
st.markdown("*SENSE AI - Democratizing Cardiac Care | Powered by AI*")
