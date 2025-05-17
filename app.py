import yfinance as yf
import pandas as pd
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

st.set_page_config(page_title="Scalping Signals", layout="wide")
st.title("🔍 إشارات السكالبينج")

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

    # تنسيق بسيط للإشارة مع رموز ملونة بالنص فقط
    def format_signal(x):
        if x == "شراء":
            return "🟢 شراء"
        elif x == "بيع":
            return "🔴 بيع"
        else:
            return "⚪ لا توجد إشارة"

    df_result['الإشارة'] = df_result['الإشارة'].apply(format_signal)

    placeholder.table(df_result)

auto_refresh = st.checkbox("تحديث تلقائي كل 10 ثواني", value=True)

while True:
    render_table()
    if not auto_refresh:
        break
    time.sleep(10)
