import requests

URL = "https://sense-ai.streamlit.app/"

def wake_streamlit():
    try:
        response = requests.get(URL, timeout=20)
        print(f"Pinged {URL} | Status: {response.status_code}")
    except Exception as e:
        print(f"Error pinging app: {e}")

if __name__ == "__main__":
    wake_streamlit()
