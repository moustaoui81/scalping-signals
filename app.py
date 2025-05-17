import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh

# رموز العملات والأدوات المالية
symbols = {
    'EUR/USD': 'EURUSD=X',
    'XAU/USD': 'GC=F',
    'BTC/USD': 'BTC-USD',
    'NAS100': '^NDX'
}

def fetch_data(symbol, period='5d', interval='5m'):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)
    if df.empty:
        raise ValueError(f"No data for symbol {symbol}")
    return df

def sma(data, window):
    return data['Close'].rolling(window=window).mean()

def rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def analyze_price_action(df):
    df['SMA_10'] = sma(df, 10)
    df['SMA_30'] = sma(df, 30)
    df['RSI_14'] = rsi(df, 14)
    
    signal = "لا توجد إشارة"
    tp = None
    sl = None
    explanation = ""
    
    last_close = df['Close'].iloc[-1]
    sma_10 = df['SMA_10'].iloc[-1]
    sma_30 = df['SMA_30'].iloc[-1]
    rsi_val = df['RSI_14'].iloc[-1]
    
    if sma_10 > sma_30 and rsi_val < 70:
        signal = "شراء"
        tp = last_close * 1.002
        sl = last_close * 0.998
        explanation = (
            f"المتوسط المتحرك السريع (10) أعلى من المتوسط البطيء (30)، "
            f"وRSI أقل من 70، مما يدل على قوة في الاتجاه الصاعد وفرصة شراء جيدة."
        )
    elif sma_10 < sma_30 and rsi_val > 30:
        signal = "بيع"
        tp = last_close * 0.998
        sl = last_close * 1.002
        explanation = (
            f"المتوسط المتحرك السريع (10) أقل من المتوسط البطيء (30)، "
            f"وRSI أعلى من 30، مما يشير إلى ضعف في السعر وفرصة بيع."
        )
    else:
        explanation = (
            "لا توجد إشارة واضحة حالياً بناءً على المتوسطات المتحركة وRSI."
        )

    return signal, round(tp, 5) if tp else "-", round(sl, 5) if sl else "-", explanation

# تحديث الصفحة كل 10 ثواني تلقائيًا
st_autorefresh(interval=10*1000, limit=None, key="datarefresh")

st.set_page_config(page_title="تحليل إشارات السكالبينج", layout="centered")

# تصميم CSS للصفحة
st.markdown("""
<style>
body {
    background-color: #f9fafb;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    direction: rtl;
}
h1 {
    color: #195782;
    text-align: center;
    margin-bottom: 30px;
}
.table-container {
    max-width: 900px;
    margin: auto;
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}
table {
    width: 100%;
    border-collapse: collapse;
}
th {
    background-color: #195782;
    color: white;
    padding: 12px;
    font-size: 16px;
    text-align: center;
    border-radius: 8px 8px 0 0;
}
td {
    padding: 12px;
    border-bottom: 1px solid #ddd;
    text-align: center;
    font-size: 15px;
}
tr:hover {
    background-color: #f1f7ff;
}
.signal-buy {
    color: #008000;
    font-weight: bold;
}
.signal-sell {
    color: #d32f2f;
    font-weight: bold;
}
.signal-none {
    color: #666666;
}
.description {
    margin-top: 15px;
    font-size: 14px;
    color: #333333;
    background-color: #eef5fc;
    border-radius: 8px;
    padding: 12px;
    box-shadow: inset 0 0 5px #c4d7f7;
}
footer {
    margin-top: 40px;
    text-align: center;
    font-size: 13px;
    color: #999;
}
</style>
""", unsafe_allow_html=True)

st.title("تحليل إشارات السكالبينج الحيّة")

# بناء بيانات الجدول
data_rows = []
for name, symbol in symbols.items():
    try:
        df = fetch_data(symbol)
        current_price = round(df['Close'].iloc[-1], 5)
        signal, tp, sl, explanation = analyze_price_action(df)
        data_rows.append({
            "الأداة": name,
            "السعر الحالي": current_price,
            "الإشارة": signal,
            "هدف الربح (TP)": tp,
            "وقف الخسارة (SL)": sl,
            "شرح الإشارة": explanation
        })
    except Exception as e:
        data_rows.append({
            "الأداة": name,
            "السعر الحالي": "-",
            "الإشارة": "خطأ",
            "هدف الربح (TP)": "-",
            "وقف الخسارة (SL)": "-",
            "شرح الإشارة": f"حدث خطأ: {e}"
        })

df_display = pd.DataFrame(data_rows)

# تغيير لون نص الإشارة حسب نوعها
def color_signal(val):
    if val == "شراء":
        return 'color: green; font-weight: bold;'
    elif val == "بيع":
        return 'color: red; font-weight: bold;'
    elif val == "خطأ":
        return 'color: orange; font-weight: bold;'
    else:
        return 'color: gray;'

styled_df = df_display.style.applymap(color_signal, subset=["الإشارة"])

st.markdown('<div class="table-container">', unsafe_allow_html=True)
st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<footer> 
تم تحديث البيانات تلقائيًا كل 10 ثواني | خدمة إشارات السكالبينج الحيّة
</footer>
""", unsafe_allow_html=True)
