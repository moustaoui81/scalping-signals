import streamlit as st
import yfinance as yf
import pandas as pd
import time

# تعريف الرموز
symbols = {
    'EUR/USD': 'EURUSD=X',
    'XAU/USD': 'GC=F',
    'BTC/USD': 'BTC-USD',
    'NAS100': '^NDX'
}

# دالة لجلب البيانات من yfinance
def fetch_data(symbol, period='5d', interval='5m'):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)
    if df.empty:
        raise ValueError(f"No data for symbol {symbol}")
    return df

# دالة لحساب المتوسط المتحرك البسيط
def sma(data, window):
    return data['Close'].rolling(window=window).mean()

# دالة لحساب مؤشر القوة النسبية RSI
def rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# تحليل حركة السعر وتوليد إشارة
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

# دالة لتوليد التقرير وعرضه في ستريمليت
def generate_report():
    rows = []
    for name, symbol in symbols.items():
        try:
            df = fetch_data(symbol)
            current_price = round(df['Close'].iloc[-1], 5)
            signal, tp, sl = analyze_price_action(df)
            rows.append({
                "الرمز": name,
                "السعر الحالي": current_price,
                "الإشارة": signal,
                "هدف الربح (TP)": tp if tp else "-",
                "وقف الخسارة (SL)": sl if sl else "-"
            })
        except Exception as e:
            rows.append({
                "الرمز": name,
                "السعر الحالي": "-",
                "الإشارة": f"خطأ: {str(e)}",
                "هدف الربح (TP)": "-",
                "وقف الخسارة (SL)": "-"
            })
    return rows

# CSS لتنسيق الجدول والصفحة
css_style = """
<style>
body {
    direction: rtl;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #1e1e2f;
    color: #fff;
    padding: 10px;
}
h2 {
    color: #4a4a6a;
    text-align: center;
    margin-bottom: 15px;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 15px;
    box-shadow: 0 0 15px rgba(0,0,0,0.5);
    background-color: #2a2a45;
}
th, td {
    padding: 12px;
    text-align: center;
    border-bottom: 1px solid #444;
    font-size: 1rem;
}
th {
    background-color: #4a4a6a;
    color: white;
}
tr:hover {
    background-color: #3a3a5a;
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
.footer {
    text-align: center;
    font-size: 0.9em;
    color: #999;
}
</style>
"""

def main():
    st.markdown(css_style, unsafe_allow_html=True)
    st.markdown("<h2>تقرير إشارات السكالبينج</h2>", unsafe_allow_html=True)
    placeholder = st.empty()

    # تحديث البيانات كل 10 ثواني
    while True:
        data = generate_report()
        # بناء جدول HTML لعرض الإشارات بألوان مختلفة
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
        for row in data:
            signal_class = "signal-none"
            if "شراء" in row["الإشارة"]:
                signal_class = "signal-buy"
            elif "بيع" in row["الإشارة"]:
                signal_class = "signal-sell"

            table_html += f"""
            <tr>
                <td>{row['الرمز']}</td>
                <td>{row['السعر الحالي']}</td>
                <td class="{signal_class}">{row['الإشارة']}</td>
                <td>{row['هدف الربح (TP)']}</td>
                <td>{row['وقف الخسارة (SL)']}</td>
            </tr>
            """
        table_html += """
            </tbody>
        </table>
        <div class="footer">التحديث التلقائي كل 10 ثواني</div>
        """
        placeholder.markdown(table_html, unsafe_allow_html=True)
        time.sleep(10)


if __name__ == "__main__":
    main()
