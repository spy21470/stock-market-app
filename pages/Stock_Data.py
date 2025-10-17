import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

st.set_page_config(page_title="ราคาหุ้น • Stock Prices", page_icon="📊", layout="wide")

# ---------- Navigation helper ----------
def go(page_key):
    st.session_state.page = page_key
    try:
        # ใช้ได้ตั้งแต่ Streamlit 1.22+
        if page_key == "home":
            st.switch_page("Home.py")
        elif page_key == "edu":
            st.switch_page("pages/2_Education.py")
    except Exception:
        # ถ้า switch_page ใช้ไม่ได้ ให้บอกผู้ใช้ใช้ Sidebar แทน
        st.info("สลับหน้าได้จาก Sidebar หากปุ่มไม่ทำงาน (update Streamlit ≥ 1.22 เพื่อใช้ st.switch_page)")
    st.experimental_rerun()

# ---------- Header ----------
st.markdown("## 📊 ราคาหุ้น — Stock Prices")
st.caption("Real data via Yahoo Finance (TH/EN) • Candlestick + Metrics")

# ---------- Inputs ----------
preset = [
    "AAPL", "MSFT", "GOOGL", "TSLA", "NVDA",
    "PTT.BK", "CPALL.BK", "ADVANC.BK", "KBANK.BK", "SCC.BK",
    "^SET", "^GSPC", "^IXIC"
]

c1, c2, c3 = st.columns([3, 2, 2])
with c1:
    ticker = st.text_input("ใส่สัญลักษณ์หุ้น / Enter Ticker", value="AAPL", help="เช่น AAPL, TSLA, PTT.BK, ^SET")
with c2:
    pick = st.selectbox("หรือเลือกจากรายการ / Or choose preset", preset, index=0)
with c3:
    if st.button("ใช้ค่าที่เลือก / Use preset"):
        ticker = pick

d1, d2 = st.columns(2)
with d1:
    start = st.date_input("เริ่มต้น / Start", value=date.today() - timedelta(days=180))
with d2:
    end = st.date_input("สิ้นสุด / End", value=date.today())

if not ticker:
    st.warning("โปรดใส่สัญลักษณ์หุ้น (e.g., AAPL, PTT.BK)")
    st.stop()

# ---------- Fetch ----------
t = yf.Ticker(ticker)
today_hist = t.history(period="1d")

if today_hist.empty:
    st.error("ไม่พบข้อมูลของสัญลักษณ์นี้ / No data for this ticker.")
    st.stop()

last_close = float(today_hist["Close"].iloc[-1])
try:
    info = t.fast_info
    prev_close = info.get("previous_close", None)
    vol = info.get("last_volume", None)
except Exception:
    prev_close, vol = None, None

change = (last_close - prev_close) if prev_close is not None else None
pct = ((change / prev_close) * 100) if prev_close not in (None, 0) else None

m1, m2, m3, m4 = st.columns(4)
m1.metric("ราคา (Last Price)", f"{last_close:,.2f}")
m2.metric("เปลี่ยนแปลง / Δ", f"{change:+.2f}" if change is not None else "—")
m3.metric("%เปลี่ยนแปลง", f"{pct:+.2f}%" if pct is not None else "—")
m4.metric("ปริมาณ (Volume)", f"{vol:,}" if vol else "—")

st.markdown("---")

# ---------- History + Chart ----------
hist = t.history(
    start=pd.to_datetime(start),
    end=pd.to_datetime(end) + pd.Timedelta(days=1),
    interval="1d"
)

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

    csv = hist.reset_index().to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ ดาวน์โหลดข้อมูล (CSV) / Download CSV", data=csv, file_name=f"{ticker}_history.csv")

st.markdown("---")

# ---------- Navigation Buttons ----------
c_left, c_right = st.columns(2)
with c_left:
    if st.button("🏠 กลับหน้าแรก (Home)"):
        go("home")
with c_right:
    if st.button("📚 ไปหน้าความรู้ (Education)"):
        go("edu")
