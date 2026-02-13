# 🩺 SENSE AI: Precision Cardiac Health Dashboard

> **Democratizing Cardiac Care via Computer Vision & Predictive Analytics**

**SENSE AI** is a futuristic, clinical intelligence portal designed to bridge the gap between rapid diagnostic tests and digital health records. By using **Computer Vision** to analyze 5-plex biomarker strips, the system generates a real-time **Cardiac Risk Score (CRS)**, providing instantaneous triage and personalized care plans.

---

## ✨ Key Features

* **🔍 Computer Vision Engine:** Uses OpenCV to extract Region of Interest (ROI) from diagnostic strips and maps HSV color intensity to clinical values.
* **📈 SENSE-CRS Algorithm:** A proprietary weighted algorithm that fuses 5 biomarkers to calculate a unified Cardiac Risk Score.
* **🚨 High-Risk Triage HUD:** An emergency interface that triggers visual "pulses" and voice-based alerts (gTTS) when life-threatening levels are detected.
* **📊 Longitudinal Tracking:** Integrated SQLite3 database to monitor patient health trends over months or years.
* **📑 Clinical Reporting:** One-click PDF generation featuring medical-grade formatting and threshold-based color coding.
* **🎨 Neural UI:** A "Glassmorphism" interface built with custom CSS for a high-tech, clinical feel.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Python-based Web Framework)
* **Image Processing:** [OpenCV](https://opencv.org/) & NumPy
* **Database:** SQLite3
* **Visuals:** Plotly (Radar charts and time-series graphs)
* **Voice/Report:** gTTS (Google Text-to-Speech) & FPDF

---

## 🧪 Biomarkers Tracked

The system analyzes five critical indicators to provide a holistic cardiac profile:

1. **Glucose:** Metabolic stress indicator.
2. **Hemoglobin (Hb):** Oxygen-carrying capacity.
3. **NT-proBNP:** Heart failure marker (stretching of the heart muscle).
4. **Lp(a):** Genetic risk factor for atherosclerosis.
5. **Troponin I:** Critical protein released during acute cardiac injury.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8 or higher
* A webcam or sample diagnostic strip images

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/sense-ai.git
cd sense-ai

```


2. **Install dependencies:**
```bash
pip install streamlit opencv-python-headless numpy pandas plotly gtts fpdf

```


3. **Run the application:**
```bash
streamlit run app.py

```



---

## 📋 Usage Guide

1. **Login:** Use Institutional ID and Access Key .
2. **Register:** Create a new Patient ID in the **Patient Registration** tab.
3. **Scan:** Upload a strip image in the **New Diagnostic Scan** section.
4. **Analyze:** Review the **CRS Score** and automated **Personalized Care Plan**.
5. **Export:** Download the clinical report as a PDF for hospital records.

---

## 🔮 Future Roadmap

* [ ] **Hardware Integration:** Direct connection to Raspberry Pi camera modules.
* [ ] **LLM Integration:** Using GPT-4 to generate automated "Doctor's Notes."
* [ ] **Blockchain:** Securing patient data on a decentralized ledger for privacy.
* [ ] **FHIR Compliance:** Exporting data in standard hospital interoperability formats.

---

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Developed for AI Hackathon 2026** *Empowering clinicians, saving lives.*
