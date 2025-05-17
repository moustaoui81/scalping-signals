import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# ✅ التحديث التلقائي كل 10 ثواني
st_autorefresh(interval=10 * 1000, key="data_refresh")

# 🎨 تنسيق CSS
st.markdown("""
    <style>
    body {
        background-color: #f2f4f8;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
    }
    h1 {
        color: #195782;
    }
    .stDataFrame thead tr th {
        background-color: #195782;
        color: white;
    }
    .stDataFrame tbody tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    </style>
""", unsafe_allow_html=True)

# 🧠 ترويسة
st.title("📈 إشارات السكالبينج - Scalping Signals")

# ✅ قائمة الأسهم
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
            signal = '-'

        data.append({'السهم': symbol, 'الإشارة': signal, 'السعر الحالي': f"${current:.2f}"})

# 🧾 جدول الإشارات
if data:
    df_result = pd.DataFrame(data)
    st.dataframe(df_result, use_container_width=True)
else:
    st.warning("لا توجد إشارات حالياً. ⏳")

# ✅ توقيع بسيط
st.markdown("<hr><center>تم التحديث تلقائياً كل 10 ثواني | تصميم بسيط بلغة ❤️ البايثون و Streamlit</center>", unsafe_allow_html=True)
