import streamlit as st

st.set_page_config(page_title="ความรู้หุ้น • Investing Basics", page_icon="📚", layout="wide")

def go(page_key):
    st.session_state.page = page_key
    try:
        if page_key == "home":
            st.switch_page("Home.py")
        elif page_key == "stock":
            st.switch_page("pages/1_Stock_Data.py")
    except Exception:
        st.info("สลับหน้าได้จาก Sidebar หากปุ่มไม่ทำงาน (update Streamlit ≥ 1.22 เพื่อใช้ st.switch_page)")
    st.experimental_rerun()

st.markdown("## 📚 ความรู้หุ้น — Investing Basics")
st.caption("Short bilingual notes • Thai + English")

st.markdown("""
### 1) คำศัพท์สำคัญ (Key Terms)
- **Price / ราคา** — ราคาซื้อขายล่าสุดของหุ้น  
- **Volume / ปริมาณ** — จำนวนหุ้นที่ถูกซื้อขายในช่วงเวลา  
- **Market Cap / มูลค่าตลาด** — ราคาหุ้น × จำนวนหุ้นทั้งหมด  
- **P/E Ratio** — ราคาเทียบกำไรต่อหุ้น (ประเมินความแพง/ถูก)  
- **Dividend / เงินปันผล** — ผลตอบแทนที่บริษัทจ่ายคืนผู้ถือหุ้น  

### 2) วิธีอ่านกราฟแท่งเทียน (How to read Candlesticks)
- **Body** — ช่วงเปิด–ปิด (Open–Close)  
- **Wick/Shadow** — หางเทียน (High/Low)  
- **Bullish (เขียว)** — ปิดสูงกว่าเปิด → แรงซื้อเด่น  
- **Bearish (แดง)** — ปิดต่ำกว่าเปิด → แรงขายเด่น  

### 3) ความเสี่ยงและพอร์ต (Risk & Portfolio)
- **Diversification** — กระจายการลงทุนเพื่อลดความเสี่ยงเฉพาะตัว  
- **Time Horizon** — ระยะเวลาการลงทุนสัมพันธ์กับความผันผวน  
- **Risk Tolerance** — ความสามารถในการรับความเสี่ยงต่างกัน  
- **Rebalancing** — ปรับสัดส่วนพอร์ตกลับสู่เป้าหมาย  
- **Cost & Tax** — ต้นทุนและภาษีมีผลต่อผลตอบแทนสุทธิ  

> ⚠️ **Disclaimer**: ข้อมูลเพื่อการศึกษา ไม่ใช่คำแนะนำการลงทุน (Educational use only)
""")

st.markdown("---")

c1, c2 = st.columns(2)
with c1:
    if st.button("🏠 กลับหน้าแรก (Home)"):
        go("home")
with c2:
    if st.button("📊 ไปหน้าราคาหุ้น (Stock Data)"):
        go("stock")
