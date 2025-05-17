import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import time

# تعريف الرموز
symbols = {
    'EUR/USD': 'EURUSD=X',
    'XAU/USD': 'GC=F',
    'BTC/USD': 'BTC-USD',
    'NAS100': '^NDX'
}

# جلب البيانات من yfinance
def fetch_data(symbol, period='5d', interval='5m'):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)
    if df.empty:
        raise ValueError(f"No data for symbol {symbol}")
    return df

# المتوسط المتحرك البسيط
def sma(data, window):
    return data['Close'].rolling(window=window).mean()

# مؤشر القوة النسبية RSI
def rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# تحليل السعر واعطاء إشارة مع TP و SL
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

# تصميم CSS للصفحة
page_css = """
<style>
body {
    background: #0d1117;
    color: #c9d1d9;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h1, h2 {
    text-align: center;
    color: #58a6ff;
}
table {
    border-collapse: collapse;
    width: 90%;
    margin: 20px auto;
    box-shadow: 0 0 15px rgba(88, 166, 255, 0.4);
}
th, td {
    border: 1px solid #30363d;
    padding: 12px 18px;
    text-align: center;
}
th {
    background-color: #161b22;
    color: #58a6ff;
    font-size: 1.1rem;
}
tr:nth-child(even) {
    background-color: #161b22;
}
tr:hover {
    background-color: #238636;
    color: white;
    cursor: pointer;
}
.signal-buy {
    color: #2ea44f;
    font-weight: bold;
    animation: pulseGreen 2s infinite;
}
.signal-sell {
    color: #da3633;
    font-weight: bold;
    animation: pulseRed 2s infinite;
}
.signal-none {
    color: #8b949e;
}
.tp-sl {
    font-weight: bold;
    color: #79c0ff;
}
@keyframes pulseGreen {
    0% { text-shadow: 0 0 5px #2ea44f; }
    50% { text-shadow: 0 0 20px #2ea44f; }
    100% { text-shadow: 0 0 5px #2ea44f; }
}
@keyframes pulseRed {
    0% { text-shadow: 0 0 5px #da3633; }
    50% { text-shadow: 0 0 20px #da3633; }
    100% { text-shadow: 0 0 5px #da3633; }
}
.footer {
    font-size: 0.8rem;
    text-align: center;
    margin-top: 40px;
    color: #8b949e;
}
.contact-info {
    margin-top: 60px;
    font-size: 0.9rem;
    text-align: center;
    color: #58a6ff;
}
.contact-info span {
    display: inline-block;
    margin: 0 15px;
    font-weight: bold;
}
</style>
"""

# الدالة الرئيسية لعرض التقرير
def main():
    st.set_page_config(page_title="تقرير إشارات السكالبينج - عبد الحق", layout="centered")
    st.markdown(page_css, unsafe_allow_html=True)
    st.title("تقرير إشارات السكالبينج")

    # بناء جدول HTML
    html = """
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
    """

    st.markdown(html, unsafe_allow_html=True)
    st.markdown('<div class="footer">التحديث التلقائي كل 10 ثواني</div>', unsafe_allow_html=True)

    # معلومات الاتصال بالصفحة - صغيرة في الأسفل
    contact_html = """
    <div class="contact-info">
        <span>الاسم: عبد الحق</span> |
        <span>الهاتف: 0664959709</span> |
        <span>البريد: <a href="mailto:abdelhak122@gmail.com" style="color:#58a6ff;">abdelhak122@gmail.com</a></span> |
        <span>واتساب: <a href="https://wa.me/212664959709" target="_blank" style="color:#58a6ff;">0664959709</a></span>
    </div>
    """
    st.markdown(contact_html, unsafe_allow_html=True)

    # تحديث كل 10 ثواني تلقائيًا
    time.sleep(10)
    st.experimental_rerun()

if __name__ == "__main__":
    main()
