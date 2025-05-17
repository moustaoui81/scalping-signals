import yfinance as yf
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import numpy as np
import time
from IPython.display import clear_output, display, HTML

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

def generate_report():
    html = """
<style>
    body {font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#1e1e2f; color:#fff; padding:20px;}
    table {width:100%; border-collapse: collapse; margin: 20px 0; box-shadow: 0 0 15px rgba(0,0,0,0.5);}
    th, td {padding: 12px; text-align: center; border-bottom: 1px solid #444;}
    th {background: #4a4a6a; font-size: 1.1em;}
    tr:hover {background: #3a3a5a;}
    .signal-buy {color: #4CAF50; font-weight: bold;}
    .signal-sell {color: #f44336; font-weight: bold;}
    .signal-none {color: #aaa;}
    .tp-sl {font-weight: bold;}
    .footer {text-align: center; margin-top: 20px; font-size: 0.9em; color: #999;}
</style>
<h2>تقرير إشارات السكالبينج</h2>
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

    for name, symbol in symbols.items():
        try:
            df = fetch_data(symbol)
            current_price = round(df['Close'].iloc[-1], 5)
            signal, tp, sl = analyze_price_action(df)
            if signal == "شراء":
                signal_html = f'<span class="signal-buy">{signal}</span>'
            elif signal == "بيع":
                signal_html = f'<span class="signal-sell">{signal}</span>'
            else:
                signal_html = f'<span class="signal-none">{signal}</span>'
            tp_text = f"{tp}" if tp else "-"
            sl_text = f"{sl}" if sl else "-"
            html += f"""
    <tr>
        <td>{name}</td>
        <td>{current_price}</td>
        <td>{signal_html}</td>
        <td class="tp-sl">{tp_text}</td>
        <td class="tp-sl">{sl_text}</td>
    </tr>
            """
        except Exception as e:
            html += f"""
    <tr>
        <td>{name}</td>
        <td colspan="4" style="color:#f44336;">حدث خطأ: {str(e)}</td>
    </tr>
            """

    html += """
  </tbody>
</table>
<div class="footer">التحديث التلقائي كل 10 ثواني</div>
"""
    clear_output(wait=True)
    display(HTML(html))

def auto_update(interval=10):
    while True:
        generate_report()
        time.sleep(interval)

if __name__ == "__main__":
    auto_update()
