import streamlit as st
import threading, time, json
from datetime import datetime, date, timedelta
import websocket

st.set_page_config(page_title="Goutam Nifty Live (Angel One)", layout="wide")

st.title("Goutam Nifty Live — Angel One SmartAPI (Tick-by-tick)")
st.markdown("This app connects to Angel One SmartAPI WebSocket and streams true tick-by-tick NIFTY 50 prices. "
            "You will be prompted for your daily Access Token. **Do NOT paste username/password here.**")

with st.expander("How to get Access Token (quick)"):
    st.markdown("""
1. Login to Angel One SmartAPI / SmartConnect using your client credentials and 2FA as usual.  
2. Generate Access Token from their portal or via the SmartAPI login flow.  
3. Paste the Access Token (only) into the field below when the app asks for it.
""")

api_key = st.text_input("API Key (optional) — leave blank if using access token only", type="password")
access_token = st.text_input("Paste today's Access Token here", type="password")

start_btn = st.button("Connect & Subscribe NIFTY 50 (tick)")

status = st.empty()
ticker_box = st.empty()
table_box = st.empty()

if start_btn:
    if not access_token:
        st.error("Please paste your Access Token (from Angel One SmartAPI).")
    else:
        status.info("Starting local websocket client...")
        import smartapi_client
        def run_client():
            client = smartapi_client.SmartWSClient(access_token=access_token, api_key=api_key)
            try:
                client.connect_and_subscribe_nifty(on_tick_callback=lambda tick: (
                    ticker_box.metric(label="NIFTY 50 LTP", value=f"{tick.get('ltp', '')}", delta=f"{tick.get('change', '')}%"),
                    table_box.table([tick])
                ))
            except Exception as e:
                status.error(f"WebSocket client error: {e}")

        t = threading.Thread(target=run_client, daemon=True)
        t.start()
        status.success("WebSocket client started. Subscribed to NIFTY 50. Waiting for ticks...")