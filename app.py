import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# دالة لتلوين خلايا "الإشارة"
def style_signals(val):
    if val == "شراء":
        color = '#4CAF50'  # أخضر
        weight = 'bold'
    elif val == "بيع":
        color = '#f44336'  # أحمر
        weight = 'bold'
    else:
        color = '#aaa'     # رمادي
        weight = 'normal'
    return f'color: {color}; font-weight: {weight}'

# هنا يتم تحديث الصفحة تلقائياً كل 10 ثواني
count = st_autorefresh(interval=10 * 1000, limit=None, key="auto_refresh")

data = {
    "الرمز": ["EUR/USD", "XAU/USD", "BTC/USD", "NAS100"],
    "السعر الحالي": [1.11669, 3205.30005, 103035.125, 21428.79102],
    "الإشارة": ["لا توجد إشارة", "لا توجد إشارة", "بيع", "شراء"],
    "هدف الربح (TP)": ["-", "-", 102829.05475, 21471.6486],
    "وقف الخسارة (SL)": ["-", "-", 103241.19525, 21385.93343]
}

df = pd.DataFrame(data)

st.set_page_config(page_title="2تقرير إشارات السكالبينج", layout="wide")

st.markdown("""
<style>
body {
    direction: rtl;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #1e1e2f;
    color: #fff;
    padding: 10px;
}
h1, h2 {
    color: #4a4a6a;
    text-align: center;
    margin-bottom: 15px;
}
.stDataFrame table {
    background-color: #2a2a45 !important;
    border-collapse: collapse !important;
    width: 100% !important;
    box-shadow: 0 0 15px rgba(0,0,0,0.5);
}
.stDataFrame th, .stDataFrame td {
    padding: 12px !important;
    text-align: center !important;
    border-bottom: 1px solid #444 !important;
    font-size: 1rem !important;
}
.stDataFrame th {
    background-color: #4a4a6a !important;
    color: white !important;
}
.stDataFrame tr:hover {
    background-color: #3a3a5a !important;
}
.footer {
    text-align: center;
    font-size: 0.9em;
    color: #999;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)

st.title("تقرير إشارات السكالبينج")

st.dataframe(df.style.applymap(style_signals, subset=["الإشارة"]))

st.markdown('<div class="footer">التحديث التلقائي كل 10 ثواني</div>', unsafe_allow_html=True)
