import streamlit as st

st.set_page_config(page_title="ความรู้หุ้น • Investing Basics", page_icon="📚", layout="wide")

st.markdown("## 📚 ความรู้หุ้น — Investing Basics")
st.caption("Short, bilingual notes for beginners • Thai + English")

st.markdown("""
### 1) คำศัพท์สำคัญ (Key Terms)
- **Price / ราคา**: ราคาซื้อขายล่าสุดของหุ้น
- **Volume / ปริมาณ**: จำนวนหุ้นที่ถูกซื้อขายในช่วงเวลา
- **Market Cap / มูลค่าตลาด**: ราคาหุ้น × จำนวนหุ้นทั้งหมด
- **P/E Ratio**: ราคาเทียบกำไรต่อหุ้น (ประเมินความแพง/ถูก)
- **Dividend / เงินปันผล**: ผลตอบแทนที่บริษัทจ่ายคืนผู้ถือหุ้น

### 2) วิธีอ่านกราฟแท่งเทียน (Candlestick)
- **Body**: ช่วงเปิด–ปิด (Open–Close)
- **Wick/Shadow**: หางเทียนแสดงราคาสูงสุด/ต่ำสุด (High/Low)
- **Bullish (เขียว)**: ปิดสูงกว่าเปิด → แรงซื้อเด่น
- **Bearish (แดง)**: ปิดต่ำกว่าเปิด → แรงขายเด่น

### 3) ความเสี่ยงและการจัดพอร์ต (Risk & Portfolio)
- **Diversification**: กระจายการลงทุน ลดความเสี่ยงเฉพาะตัว
- **Time Horizon**: ระยะเวลาการลงทุนสัมพันธ์กับความผันผวน
- **Risk Tolerance**: ยอมรับความเสี่ยงได้มากน้อยต่างกัน
- **Rebalancing**: ปรับสัดส่วนพอร์ตตามเป้าหมาย

> ⚠️ **คำเตือน (Disclaimer)**: ข้อมูลเพื่อการศึกษา ไม่ใช่คำแนะนำการลงทุน
""")

st.markdown("---")
try:
    l, r = st.columns(2)
    with l:
        st.page_link("Home.py", label="🏠 กลับหน้าแรก – Back to Home")
    with r:
        st.page_link("pages/1_📊_Stock_Data.py", label="📊 ไปหน้าราคาหุ้น – Stock Prices")
except Exception:
    st.info("ใช้ Sidebar เพื่อสลับหน้า (หรืออัปเกรด Streamlit ≥ 1.31 เพื่อใช้ปุ่มลิงก์)")
