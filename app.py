import yfinance as yf
import streamlit as st

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

def analyze_price_action(df):
    # تحليلات بسيطة - يمكنك تعديلها
    last_close = df['Close'].iloc[-1]
    signal = "لا توجد إشارة"
    if df['Close'].iloc[-1] > df['Close'].iloc[-2]:
        signal = "شراء"
    else:
        signal = "بيع"
    return signal, round(last_close, 5)

st.title("تقرير إشارات السكالبينج")

for name, symbol in symbols.items():
    try:
        df = fetch_data(symbol)
        signal, price = analyze_price_action(df)
        st.write(f"**{name}**")
        st.write(f"السعر الحالي: {price}")
        st.write(f"الإشارة: {signal}")
        st.markdown("---")
    except Exception as e:
        st.error(f"حدث خطأ في جلب البيانات لـ {name}: {e}")
