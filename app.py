import streamlit as st
from streamlit_autorefresh import st_autorefresh
import yfinance as yf
import pandas as pd
import time

# ✅ Set page config FIRST
st.set_page_config(page_title="Scalping Signals", layout="wide")

# ✅ Auto-refresh every 10 seconds
st_autorefresh(interval=10000, key="datarefresh")

# ✅ Custom CSS styling
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    }
    h1, h3 {
        color: #195782;
    }
    .stDataFrame th {
        background-color: #195782;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ Title
st.markdown("## 🔍 Scalping Signals Live")
st.write("This dashboard shows fast-moving signals based on live data. Auto-refresh updates every 10 seconds.")

# ✅ Symbols to track
symbols = ["AAPL", "MSFT", "GOOG", "AMZN", "META", "TSLA", "NVDA", "AMD", "NFLX", "BABA"]

buy_signals = []

# ✅ Fetch and calculate
for symbol in symbols:
    data = yf.download(symbol, period="1d", interval="1m", progress=False)

    if data.empty or len(data) < 2:
        continue

    current_price = data['Close'].iloc[-1]
    previous_price = data['Close'].iloc[-2]

    if pd.isna(current_price) or pd.isna(previous_price):
        continue

    percent_change = ((current_price - previous_price) / previous_price) * 100

    if percent_change > 0.2:
        buy_signals.append({
            'Symbol': symbol,
            'Current Price': f"${current_price:.2f}",
            'Change (%)': f"{percent_change:.2f}%"
        })

# ✅ Show result
if buy_signals:
    df = pd.DataFrame(buy_signals)
    st.success(f"📈 {len(buy_signals)} Buy Signal(s) Detected")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No buy signals detected at this moment.")
