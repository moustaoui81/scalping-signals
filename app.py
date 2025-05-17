import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import time

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
    
    last_close = df['Close'].iloc[-1]
    sma_10 = df['SMA_10'].iloc[-1]
    sma_30 = df['SMA_30'].iloc[-1]
    rsi_val = df['RSI_14'].iloc[-1]
    
    if sma_10 > sma_30 and rsi_val < 70:
        signal = "شراء"
        tp = last_close * 1.002
        sl = last_close * 0.998
    elif sma_10 < sma_30 and rsi_val > 30:
        signal = "بيع"
        tp = last_close * 0.998
        sl = last_close * 1.002

    return signal, round(tp,5) if tp else None, round(sl,5) if sl else None

# تصميم الصفحة
st.set_page_config(page_title="إشارات السكالبينج الحيّة", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 0 20px rgba(0,0,0,0.1);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .signal-box {
        background: white;
        padding: 15px 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgb(0 0 0 / 0.1);
    }
    .signal-title {
        color: #195782;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .signal-text {
        font-size: 18px;
        margin-bottom: 6px;
    }
    .signal-buy {
        color: green;
        font-weight: 700;
    }
    .signal-sell {
        color: red;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main'>", unsafe_allow_html=True)

st.title("تقرير إشارات السكالبينج الحيّة")

# زر تحديث يدوي
if st.button("تحديث البيانات الآن 🔄"):
    st.experimental_rerun()

# تشغيل تحديث تلقائي كل 10 ثواني
# باستخدام streamlit_autorefresh
from streamlit_autorefresh import st_autorefresh
count = st_autorefresh(interval=10*1000, limit=None, key="refresh")

for name, symbol in symbols.items():
    try:
        df = fetch_data(symbol)
        current_price = round(df['Close'].iloc[-1], 5)
        signal, tp, sl = analyze_price_action(df)

        st.markdown(f"""
        <div class='signal-box'>
            <div class='signal-title'>{name}</div>
            <div class='signal-text'><b>السعر الحالي:</b> {current_price}</div>
            <div class='signal-text'><b>الإشارة:</b> 
                <span class='{"signal-buy" if signal=="شراء" else "signal-sell" if signal=="بيع" else ""}'>{signal}</span>
            </div>
            <div class='signal-text'><b>هدف الربح (TP):</b> {tp if tp else "-"}</div>
            <div class='signal-text'><b>وقف الخسارة (SL):</b> {sl if sl else "-"}</div>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"حدث خطأ في جلب البيانات لـ {name}: {e}")

st.markdown("</div>", unsafe_allow_html=True)
