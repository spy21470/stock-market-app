import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="ตลาดหุ้น • Market Overview", page_icon="💹", layout="wide")

# ---------- CSS ----------
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
  --card: #0E131A;
}
html, body, [data-testid="stAppViewContainer"] { background: var(--bg-0) !important; color: var(--text-0) !important; }
[data-testid="stHeader"] { background: transparent !important; }
section.main > div { padding-top: 1.2rem; }
.stButton > button, .stDownloadButton > button {
  background: linear-gradient(135deg, var(--lux-gold), #8A6E2F);
  color: #0A0A0A; border: 0; border-radius: 10px; font-weight: 700;
}
.block-container { padding-top: 1rem; }
div[data-testid="stMetricValue"] { color: var(--text-0); }
div[data-testid="stMetricDelta"] { font-weight: 700; }
.lux-card {
  background: linear-gradient(180deg, var(--bg-1), var(--bg-2));
  border: 1px solid #212734; border-radius: 16px; padding: 18px;
}
.lux-subtle { color: var(--text-1); font-size: 0.95rem; }
</style>
""", unsafe_allow_html=True)
# ---------- End CSS ----------

st.title("💹 ตลาดหุ้น | Market Overview")
st.caption("Dark • Luxury • Thai + English • Real data via Yahoo Finance")

st.write("**ภาพรวมดัชนีหลัก (Major Indices)**")
indices = {
    "S&P 500 (^GSPC)": "^GSPC",
    "NASDAQ (^IXIC)": "^IXIC",
    "Dow Jones (^DJI)": "^DJI",
    "SET Thailand (^SET)": "^SET",
}
cols = st.columns(len(indices))

def fetch_quote(ticker):
    t = yf.Ticker(ticker)
    info = t.fast_info if hasattr(t, "fast_info") else{}
    last = getattr(t, "history")(period="1d").tail(1)
    print = None
    if not last.empty:
        price = float(lasst["Close"].iloc[-1])
    prev_close = getattr(info, "previous_close",None) if isinstance(info, dict) else getattr(info, "previous_close", None)
    return price, prev_close

for (label, ticker), c in zip(indices.items(), cols):
    with c:
        price, prev = fetch_quote(ticker)
        if price is not None and prev:
            change = price - prev
            pct = (change/prev)*100 if prev else 0
            delta_str = f"{change:+.2f} ({pct:+.2f}%)"
            st.metric(label=label, value=f"{price:,.2f}", delta=delta_str)
        else:
            st.metric(label=label, value="—", delta="—")

st.markdown("---")

left, right = st.columns([2,1])
with left:
    st.subheader("เกี่ยวกับเว็บ • About")
    st.markdown("""
- เว็บไซต์สรุปภาพรวมตลาดหุ้น, ดูราคาหุ้นรายตัว, และความรู้พื้นฐานการลงทุน  
- **Bilingual**: ไทย + English • **Theme**: Dark & Luxury • **Data**: Yahoo Finance (yfinance)
""")
with right:
    st.subheader("ไปยังหน้าอื่น • Navigate")
    # ใช้ page_link (Streamlit 1.31+) ถ้าไม่มี ให้ใช้ Sidebar
    try:
        st.page_link("pages/1_📊_Stock_Data.py", label="📊 ราคาหุ้น – Stock Prices")
        st.page_link("pages/2_📚_Education.py", label="📚 ความรู้หุ้น – Investing Basics")
    except Exception:
        st.info("ใช้เมนู Sidebar เพื่อสลับหน้า (หรืออัปเกรด Streamlit ≥ 1.31 เพื่อใช้ปุ่มลิงก์)")