import streamlit as st
import yfinance as yf

# ตั้งค่าเว็บ
st.set_page_config(page_title="Luxury Stock Dashboard", page_icon="💹", layout="wide")

# ใช้ session_state สำหรับการนำทาง
if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------- CSS หรูหรา Dark + Gold ----------
st.markdown("""
<style>
:root {
  --lux-gold: #D4AF37;
  --lux-green: #00C853;
  --bg-0: #0B0E11;
  --bg-1: #101418;
  --bg-2: #141922;
  --text-0: #EAECEF;
  --text-1: #B7BDC6;
}
html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--bg-0) !important;
  color: var(--text-0) !important;
}
.stButton > button {
  background: linear-gradient(135deg, var(--lux-gold), #8A6E2F);
  color: #000;
  border: 0;
  border-radius: 10px;
  padding: 0.6rem 1.2rem;
  font-weight: bold;
  cursor: pointer;
}
.stButton > button:hover {
  opacity: 0.85;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.title("💹 ตลาดหุ้น | Market Overview")
st.caption("Dark • Luxury • Thai + English • Real Data via Yahoo Finance")

st.subheader("ภาพรวมดัชนีหลัก (Major Indices)")

# ดัชนีหลัก
indices = {
    "S&P 500 (^GSPC)": "^GSPC",
    "NASDAQ (^IXIC)": "^IXIC",
    "Dow Jones (^DJI)": "^DJI",
    "SET Thailand (^SET)": "^SET"
}

cols = st.columns(len(indices))

def fetch_quote(ticker):
    t = yf.Ticker(ticker)
    hist = t.history(period="1d")
    if hist.empty:
        return None, None
    last_close = float(hist["Close"].iloc[-1])
    try:
        info = t.fast_info
        prev_close = info.get("previous_close", None)
    except:
        prev_close = None
    return last_close, prev_close

for (label, ticker), c in zip(indices.items(), cols):
    with c:
        price, prev = fetch_quote(ticker)
        if price is not None and prev:
            change = price - prev
            pct = (change / prev) * 100
            st.metric(label=label, value=f"{price:,.2f}", delta=f"{change:+.2f} ({pct:+.2f}%)")
        else:
            st.metric(label=label, value="—", delta="—")

st.markdown("---")

# ---------- Navigation Buttons ----------
st.subheader("ไปยังหน้าอื่น • Navigate")

col1, col2 = st.columns(2)
with col1:
    if st.button("📊 ดูราคาหุ้น (Stock Data)"):
        st.session_state.page = "stock"
        st.experimental_rerun()

with col2:
    if st.button("📚 ความรู้หุ้น (Education)"):
        st.session_state.page = "edu"
        st.experimental_rerun()

# ตรวจสอบ session_state เพื่อเปลี่ยนหน้า
if st.session_state.page == "stock":
    st.switch_page("pages/1_Stock_Data.py")
elif st.session_state.page == "edu":
    st.switch_page("pages/2_Education.py")
