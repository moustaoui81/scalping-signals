import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_autorefresh import st_autorefresh

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

def main():
    st.set_page_config(page_title="تحليل إشارات السكالبينج", layout="centered")

    st.markdown("""
        <style>
            .big-font {
                font-size:24px !important;
                color:#f0a500;
                text-align:center;
                margin-bottom: 20px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                max-width: 800px;
                margin: auto;
                box-shadow: 0 0 15px rgba(0,0,0,0.7);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: white;
                background:#1e1e2f;
            }
            th, td {
                padding: 12px;
                border-bottom: 1px solid #444;
                text-align: center;
            }
            th {
                background: #4a4a6a;
                font-size: 1.1em;
            }
            tr:hover {
                background: #3a3a5a;
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
            .tp-sl {
                font-weight: bold;
            }
            .footer {
                text-align: center;
                margin-top: 30px;
                font-size: 0.9em;
                color: #999;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="big-font">تقرير إشارات السكالبينج</div>', unsafe_allow_html=True)

    # تحديث تلقائي كل 10 ثواني
    count = st_autorefresh(interval=10_000, limit=None, key="refresh")

    rows = []
    for name, symbol in symbols.items():
        try:
            df = fetch_data(symbol)
            current_price = round(df['Close'].iloc[-1], 5)
            signal, tp, sl = analyze_price_action(df)
            rows.append((name, current_price, signal, tp, sl))
        except Exception as e:
            rows.append((name, "خطأ", f"حدث خطأ: {str(e)}", "-", "-"))

    # بناء جدول HTML
    table_html = """
    <table>
      <thead>
        <tr>
          <th>الرمز</th>
          <th>السعر الحالي</th>
          <th>الإشارة</th>
          <th>هدف الربح (TP)</th>
          <th>وقف الخسارة (SL)</th>
        </tr>
      </thead>
      <tbody>
    """

    for r in rows:
        name, price, signal, tp, sl = r
        if signal == "شراء":
            signal_html = f'<span class="signal-buy">{signal}</span>'
        elif signal == "بيع":
            signal_html = f'<span class="signal-sell">{signal}</span>'
        elif "حدث خطأ" in str(signal):
            signal_html = f'<span style="color:#f44336;">{signal}</span>'
        else:
            signal_html = f'<span class="signal-none">{signal}</span>'

        tp_text = f"{tp}" if tp else "-"
        sl_text = f"{sl}" if sl else "-"
        table_html += f"""
        <tr>
            <td>{name}</td>
            <td>{price}</td>
            <td>{signal_html}</td>
            <td class="tp-sl">{tp_text}</td>
            <td class="tp-sl">{sl_text}</td>
        </tr>
        """
    table_html += """
      </tbody>
    </table>
    <div class="footer">التحديث التلقائي كل 10 ثواني</div>
    """

    st.markdown(table_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
