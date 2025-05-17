import streamlit as st
from streamlit_autorefresh import st_autorefresh
import yfinance as yf
import pandas as pd

# ✅ Must be FIRST command
st.set_page_config(page_title="Scalping Signals", layout="wide")

# Auto-refresh every 10 seconds
st_autorefresh(interval=10 * 1000, key="datarefresh")

# --- Custom CSS styling ---
st.markdown("""
    <style>
        body {
            background-color: #f2f6fc;
            color: #333333;
            font-family: 'Segoe UI', sans-serif;
        }
        .main {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.05);
        }
        table {
            background-color: #ffffff;
            border-radius: 10px;
            border-collapse: collapse;
            width: 100%;
        }
        thead th {
            background-color: #195782;
            color: #ffffff;
            padding: 10px;
        }
        tbody td {
            padding: 10px;
            border-bottom: 1px solid #eeeeee;
        }
    </style>
""", unsafe_allow_html=True)

# --- App title and description ---
st.markdown("<h1 style='color:#195782;'>🔍 Scalping Signals Live</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:16px;'>This dashboard shows fast-moving signals based on live data. Auto-refresh updates every 10 seconds.</p>", unsafe_allow_html=True)

# --- Your logic to load symbols ---
symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']
buy_signals = []

for symbol in symbols:
    data = yf.download(symbol, period="1d", interval="1m")
    if data.empty or len(data) < 2:
        continue

    current_price = data['Close'].iloc[-1]
    previous_price = data['Close'].iloc[-2]
    percent_change = ((current_price - previous_price) / previous_price) * 100

    if percent_change > 0.2:
        buy_signals.append({
            'Symbol': symbol,
            'Current Price': f"${current_price:.2f}",
            'Change (%)': f"{percent_change:.2f}%"
        })

# --- Display table with styling ---
if buy_signals:
    df = pd.DataFrame(buy_signals)
    st.markdown("### 🟢 Buy Signals")
    st.dataframe(df.style.set_properties(**{
        'background-color': '#ffffff',
        'color': '#000000',
        'border-color': 'gray',
        'text-align': 'center'
    }))
else:
    st.info("No buy signals at the moment. Please wait for the next refresh.")
