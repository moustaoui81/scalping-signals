import streamlit as st
import pandas as pd
import time

# دالة لتلوين خلايا "الإشارة"
def style_signals(val):
    if val == "شراء":
        color = 'green'
        weight = 'bold'
    elif val == "بيع":
        color = 'red'
        weight = 'bold'
    else:
        color = 'gray'
        weight = 'normal'
    return f'color: {color}; font-weight: {weight}'

# بيانات الإشارات
data = {
    "الرمز": ["EUR/USD", "XAU/USD", "BTC/USD", "NAS100"],
    "السعر الحالي": [1.11669, 3205.30005, 103035.125, 21428.79102],
    "الإشارة": ["لا توجد إشارة", "لا توجد إشارة", "بيع", "شراء"],
    "هدف الربح (TP)": ["-", "-", 102829.05475, 21471.6486],
    "وقف الخسارة (SL)": ["-", "-", 103241.19525, 21385.93343]
}

df = pd.DataFrame(data)

st.title("تقرير إشارات السكالبينج")

# عرض الجدول مع تلوين الإشارات
st.dataframe(df.style.applymap(style_signals, subset=["الإشارة"]))

st.write("التحديث التلقائي كل 10 ثواني")

# تحديث تلقائي للصفحة كل 10 ثواني
time.sleep(10)
st.experimental_rerun()
