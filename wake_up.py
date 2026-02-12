import requests
import time

URL = "https://sense-ai.streamlit.app/"

for i in range(2):
    try:
        r = requests.get(URL, timeout=10)
        print(f"Ping {i+1} status:", r.status_code)
    except Exception as e:
        print(f"Ping {i+1} failed:", e)
    time.sleep(5)
