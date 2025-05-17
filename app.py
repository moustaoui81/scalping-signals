import streamlit as st
import yfinance as yf
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh

# تحديث تلقائي كل 10 ثواني
st_autorefresh(interval=10 * 1000, key="refresh")

# إضافة CSS مخصص للصفحة والجدول
st.markdown("""
<style>
body, .css-18e3th9 {
    background-color: #1e1e2f;
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    direction: rtl;
}
h2 {
    color: #4a4a6a;
    text-align: center;
    margin-bottom: 15px;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 15px;
    box-shadow: 0 0 15px rgba(0,0,0,0.5);
    background-color: #2a2a45;
    color: white;
}
th, td {
    padding: 12px;
    text-align: center;
    border-bottom: 1px solid #444;
    font-size: 1rem;
}
th {
    background-color: #4a4a6a;
    color: white;
}
tr:hover {
    background-color: #3a3a5a;
}
.signal-buy {
    color: #4CAF50;
    font-weight: bold;
}
.signal-sell {
    color: #f44336;
    font-weight: bold;
}
.signal-none {
    color: #aaa;
}
.footer {
    text-align: center;
    font-size: 0.9em;
    color: #999;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

def style_signals(val):
    if val == "شراء":
        return 'color: #4CAF50; font-weight: bold; background-color: #d0f0c0'
    elif val == "بيع":
        return 'color: #f44336; font-weight: bold; background-color: #f9c0c0'
    else:
        return 'color: #aaa; background-color: #f0f0f0'

# بيانات تجريبية
data = {
    "الرمز": ["EUR/USD", "XAU/USD", "BTC/USD", "NAS100"],
    "السعر الحالي": [1.11669, 3205.30005, 103035.125, 21428.79102],
    "الإشارة": ["لا توجد إشارة", "لا توجد إشارة", "بيع", "شراء"],
    "هدف الربح (TP)": ["-", "-", 102829.05475, 21471.6486],
    "وقف الخسارة (SL)": ["-", "-", 103241.19525, 21385.93343]
}

df = pd.DataFrame(data)

# تطبيق تلوين الإشارات
styled_df = df.style.applymap(style_signals, subset=["الإشارة"])

st.markdown("## تقرير إشارات السكالبينج")

st.dataframe(styled_df, use_container_width=True)

st.markdown('<div class="footer">التحديث التلقائي كل 10 ثواني</div>', unsafe_allow_html=True)
