import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# ⏱ Auto-refresh every 10 seconds
st_autorefresh(interval=10 * 1000, key="refresh")

# 🎨 Page Styling (CSS)
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.05);
    }
    h1 {
        color: #195782;
        font-size: 2.5em;
        text-align: center;
    }
    .stDataFrame thead tr th {
        background-color: #195782;
        color: white;
    }
    .stDataFrame tbody tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    .stDataFrame td {
        text-align: center;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 🧠 Page title
st.title("📊 إشارات السكالبينج المباشرة")

# 📌 Define symbols to track
symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA']

data = []

for symbol in symbols:
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="1d", interval="1m")
    if len(df) >= 3:
        current = df['Close'].iloc[-1]
        previous = df['Close'].iloc[-2]
        before_previous = df['Close'].iloc[-3]

        if current > previous and previous < before_previous:
            signal = '📈 شراء'
        elif current < previous and previous > before_previous:
            signal = '📉 بيع'
        else:
            signal = '⏳ لا توجد إشارة'

        data.append({
            'السهم': symbol,
            'الإشارة': signal,
            'السعر الحالي': f"${current:.2f}"
        })

# 📋 Show DataFrame
if data:
    df_signals = pd.DataFrame(data)
    st.dataframe(df_signals, use_container_width=True)
else:
    st.warning("لا توجد إشارات حالياً، انتظر التحديث التالي...")

# 🔚 Footer
st.markdown("<hr><center>🔄 يتم التحديث تلقائياً كل 10 ثواني</center>", unsafe_allow_html=True)
