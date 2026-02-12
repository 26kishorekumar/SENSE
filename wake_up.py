import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Auto-refresh the app every 60 seconds
st_autorefresh(interval=60_000, key="keep_alive")

# Initialize last ping
if "last_ping" not in st.session_state:
    st.session_state.last_ping = "Never"

st.title("Streamlit Keep Alive Test")
st.write(
    "This app stays awake by receiving pings from GitHub Actions and auto-refreshes every minute."
)

# Display the last ping time
st.subheader("Last ping received:")
st.write(st.session_state.last_ping)

# Ping simulation via query param
query_params = st.experimental_get_query_params()
if "ping" in query_params:
    st.session_state.last_ping = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.success("Ping received ✅")

# Optional: live counter showing seconds since last ping
if "ping_time_counter" not in st.session_state:
    st.session_state.ping_time_counter = datetime.now()

seconds_since_ping = (datetime.now() - datetime.strptime(st.session_state.last_ping, "%Y-%m-%d %H:%M:%S") 
                      if st.session_state.last_ping != "Never" else 0)
st.write(f"Time since last ping: {seconds_since_ping} seconds")
