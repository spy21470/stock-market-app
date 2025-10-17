import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

st.set_page_config(page_title="ราคาหุ้น • Stock Prices", page_icon="📊", layout="wide")

st.markdown("## 📊 ราคาหุ้น — Stock Prices")
st.caption("Real-time (near) quotes & historical charts via Yahoo Finance")

# ตัวอย่างรายการหุ้น (รวมไทย/ต่างประเทศ)
preset = [
    "AAPL", "MSFT", "GOOGL", "TSLA", "NVDA",
    "PTT.BK", "CPALL.BK", "ADVANC.BK", "KBANK.BK", "SCC.BK",
    "^SET", "^GSPC", "^IXIC"
]

c1, c2, c3 = st.columns([3,2,2])
with c1:
    ticker = st.text_input("ใส่สัญลักษณ์หุ้น / Enter Ticker", value="AAPL", help="เช่น AAPL, TSLA, PTT.BK, ^SET")
with c2:
    pick = st.selectbox("หรือเลือกจากรายการ / Or choose preset", preset, index=0)
with c3:
    if st.button("ใช้ค่าที่เลือก / Use Preset"):
        ticker = pick

# วันที่เริ่มต้น-สิ้นสุด
d1, d2 = st.columns(2)
with d1:
    start = st.date_input("เริ่มต้น / Start", value=date.today() - timedelta(days=180))
with d2:
    end = st.date_input("สิ้นสุด / End", value=date.today())

if not ticker:
    st.warning("โปรดใส่สัญลักษณ์หุ้น (e.g., AAPL, PTT.BK)")
    st.stop()

t = yf.Ticker(ticker)

# -------- ป้ายข้อมูลปัจจุบัน (ใกล้เคียงเรียลไทม์) --------
with st.container():
    qcol1, qcol2, qcol3, qcol4 = st.columns(4)
    hist_today = t.history(period="1d")
    if hist_today.empty:
        st.error("ไม่พบข้อมูลสัญลักษณ์นี้ ลองตรวจสอบอีกครั้ง / No data returned for this ticker.")
    else:
        last_close = float(hist_today["Close"].iloc[-1])
        try:
            prev_close = t.fast_info.get("previous_close", None)
        except:
            prev_close = None
        change = (last_close - prev_close) if prev_close else None
        pct = (change/prev_close*100) if (prev_close and prev_close != 0) else None

        qcol1.metric("ราคา (Last Price)", f"{last_close:,.2f}")
        qcol2.metric("เปลี่ยนแปลง / Δ", f"{(change if change is not None else 0):+.2f}" if change is not None else "—")
        qcol3.metric("%เปลี่ยนแปลง", f"{(pct if pct is not None else 0):+.2f}%" if pct is not None else "—")
        try:
            info = t.fast_info
            vol = info.get("last_volume", None)
        except:
            vol = None
        qcol4.metric("ปริมาณ (Volume)", f"{vol:,}" if vol else "—")

st.markdown("---")

# -------- กราฟแท่งเทียน (Candlestick) --------
hist = t.history(start=pd.to_datetime(start), end=pd.to_datetime(end) + pd.Timedelta(days=1), interval="1d")
if hist.empty:
    st.warning("ไม่มีข้อมูลกราฟในช่วงวันที่เลือก")
else:
    fig = go.Figure(data=[go.Candlestick(
        x=hist.index,
        open=hist["Open"], high=hist["High"],
        low=hist["Low"], close=hist["Close"],
        name="Price"
    )])
    fig.update_layout(
        height=520,
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="#0B0E11",
        plot_bgcolor="#0B0E11",
        font=dict(color="#EAECEF"),
        xaxis=dict(gridcolor="#1F2A37"),
        yaxis=dict(gridcolor="#1F2A37"),
        title=f"Candlestick: {ticker}"
    )
    st.plotly_chart(fig, use_container_width=True)

    # ดาวน์โหลดข้อมูล
    csv = hist.reset_index().to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ ดาวน์โหลดข้อมูล (CSV) / Download CSV", data=csv, file_name=f"{ticker}_history.csv")

st.markdown("---")
# ลิงก์ไปหน้า Education / Home (ใช้ page_link ถ้ามี)
try:
    l, r = st.columns(2)
    with l:
        st.page_link("pages/2_📚_Education.py", label="📚 ไปอ่านความรู้หุ้น – Go to Education")
    with r:
        st.page_link("Home.py", label="🏠 กลับหน้าแรก – Back to Home")
except Exception:
    st.info("ใช้ Sidebar เพื่อสลับหน้า (หรืออัปเกรด Streamlit ≥ 1.31 เพื่อใช้ปุ่มลิงก์)")
