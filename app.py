import streamlit as st
from streamlit_autorefresh import st_autorefresh

signals = [
    {"symbol": "EUR/USD", "price": "1.11669", "signal": "لا توجد إشارة", "tp": "-", "sl": "-"},
    {"symbol": "XAU/USD", "price": "3205.30005", "signal": "لا توجد إشارة", "tp": "-", "sl": "-"},
    {"symbol": "BTC/USD", "price": "102720.36719", "signal": "بيع", "tp": "102514.92645", "sl": "102925.80792"},
    {"symbol": "NAS100", "price": "21428.79102", "signal": "شراء", "tp": "21471.6486", "sl": "21385.93343"},
]

css_style = """
<style>
/* ضبط خلفية الصفحة والخط */
body, .main {
    background-color: #f9fbfc;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    direction: rtl;
    text-align: center;
}

/* عنوان */
h1 {
    color: #195782;
    margin-bottom: 5px;
}
h4 {
    color: #333;
    margin-bottom: 30px;
}

/* تصميم الجدول */
table {
    border-collapse: collapse;
    width: 100%;
    max-width: 900px;
    margin: 0 auto 40px auto;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    background: #ffffff;
}

th, td {
    padding: 12px 10px;
    border-bottom: 1px solid #ddd;
    font-size: 16px;
    color: #333;
}

th {
    background-color: #195782;
    color: white;
    font-weight: 600;
    text-align: center;
}

td {
    text-align: center;
}

/* تأثير صفوف الجدول */
tr:hover {
    background-color: #f1f9ff;
}

/* ألوان الإشارات */
.signal-none {
    color: #7a7a7a;
    font-weight: 600;
}
.signal-buy {
    color: #1a8a34;
    font-weight: 700;
    animation: blink-green 1.5s infinite;
}
.signal-sell {
    color: #d63031;
    font-weight: 700;
    animation: blink-red 1.5s infinite;
}
@keyframes blink-green {
    0%, 100% {opacity: 1;}
    50% {opacity: 0.4;}
}
@keyframes blink-red {
    0%, 100% {opacity: 1;}
    50% {opacity: 0.4;}
}

/* المعلومات أسفل الصفحة */
.footer {
    max-width: 900px;
    margin: 0 auto 30px auto;
    font-size: 14px;
    color: #555;
    border-top: 1px solid #ccc;
    padding-top: 15px;
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
}
.footer a {
    color: #195782;
    text-decoration: none;
    font-weight: 600;
}
.footer a:hover {
    text-decoration: underline;
}

/* للأجهزة الصغيرة */
@media (max-width: 600px) {
    table, th, td {
        font-size: 14px;
    }
    .footer {
        flex-direction: column;
        gap: 5px;
    }
}
</style>
"""

def main():
    st_autorefresh(interval=10 * 1000, key="datarefresh")

    st.markdown(css_style, unsafe_allow_html=True)

    st.title("تقرير إشارات السكالبينج")
    st.markdown("<h4>التحديث التلقائي كل 10 ثواني</h4>", unsafe_allow_html=True)

    # بناء جدول الإشارات
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
    for item in signals:
        signal_class = "signal-none"
        if item["signal"] == "شراء":
            signal_class = "signal-buy"
        elif item["signal"] == "بيع":
            signal_class = "signal-sell"

        table_html += f"""
            <tr>
                <td>{item['symbol']}</td>
                <td>{item['price']}</td>
                <td><span class="{signal_class}">{item['signal']}</span></td>
                <td>{item['tp']}</td>
                <td>{item['sl']}</td>
            </tr>
        """
    table_html += """
        </tbody>
    </table>
    """

    st.markdown(table_html, unsafe_allow_html=True)

    # معلومات الاتصال
    st.markdown(
        """
        <div class="footer">
            <span>الاسم: عبد الحق</span>
            <span>الهاتف / واتساب: <a href="tel:0664959709">0664959709</a></span>
            <span>البريد: <a href="mailto:abdelhak122@gmail.com">abdelhak122@gmail.com</a></span>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
