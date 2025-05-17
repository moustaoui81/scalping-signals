# file: scalping_signals_app.py

import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import time

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
        raise ValueError(f"لا توجد بيانات للرمز: {symbol}")
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

# واجهة Streamlit
st.set_page_config(page_title="تقرير إشارات السكالبينج", layout="wide")
st.title("📈 تقرير إشارات السكالبينج")
st.markdown("### يتم التحديث كل 10 ثواني تلقائيًا")

placeholder = st.empty()

def render_table():
    data = []

    for name, symbol in symbols.items():
        try:
            df = fetch_data(symbol)
            current_price = round(df['Close'].iloc[-1], 5)
            signal, tp, sl = analyze_price_action(df)
            data.append({
                'الرمز': name,
                'السعر الحالي': current_price,
                'الإشارة': signal,
                'هدف الربح (TP)': tp if tp else '-',
                'وقف الخسارة (SL)': sl if sl else '-'
            })
        except Exception as e:
            data.append({
                'الرمز': name,
                'السعر الحالي': 'خطأ',
                'الإشارة': f"⚠️ {str(e)}",
                'هدف الربح (TP)': '-',
                'وقف الخسارة (SL)': '-'
            })

    df_result = pd.DataFrame(data)
    df_result['الإشارة'] = df_result['الإشارة'].apply(lambda x: 
        f"🟢 شراء" if x == "شراء" else
        f"🔴 بيع" if x == "بيع" else
        f"⚪ {x}"
    )
    placeholder.table(df_result)

# التحديث كل 10 ثواني
refresh_interval = 10
while True:
    render_table()
    time.sleep(refresh_interval)
