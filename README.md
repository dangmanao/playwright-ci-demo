# Playwright Python Automation Test Structure

## 🧪 วิธีใช้งาน
1. ติดตั้ง dependency
```bash
pip install -r requirements.txt
```

2. รัน test พร้อม generate HTML report
```bash
python run_tests.py
```

## 💡 Feature หลัก
- เปิด browser แบบ headful ทุกครั้งที่รัน
- ใช้ slowMo ทุก test ที่ 500ms
- มีการสร้าง report HTML พร้อม random name และเปิดอัตโนมัติ
- สามารถใส่ logger.info ใน test แล้วแสดงผลใน report เฉพาะ log ที่ต้องการ
- ถ้ามี test fail จะมี screenshot แนบใน report
- รองรับการทดสอบแบบ Responsive (Mobile Size) ผ่าน fixture `mobile_page`

## 📘 คำอธิบายแต่ละไฟล์หลัก

### 📁 utils/logger.py
- ใช้สร้าง `logger` ที่สามารถเรียกใช้ในทุก test ด้วยคำสั่ง `logger.info(...)`
- logger นี้จะ log ลง stdout และเก็บเข้า report ได้
- ช่วยให้เราควบคุม log ที่เราสนใจได้เอง

### 📄 conftest.py
- เป็นไฟล์ fixture หลักของ pytest
- ใช้สร้าง fixture สำหรับ:
  - `logger`: ใช้งาน logger กลางร่วมกัน
  - `page`: สำหรับ desktop browser context
  - `mobile_page`: สำหรับ mobile responsive browser context (ใช้ iPhone 13)
- มี logic สำหรับตรวจจับ test ที่ fail เพื่อเก็บ screenshot ลง reports/
- มี hook `pytest_runtest_makereport` เพื่อ track การ fail ของ test

### 📄 pytest.ini
- เป็นไฟล์ config สำหรับ pytest
- ตั้งค่า:
  - `--capture=tee-sys`: ทำให้ log แสดงและเข้า report ด้วย
  - `log_file_level = INFO`: ระบุระดับ log ที่จะโชว์ (INFO ขึ้นไป)

### 📄 run_tests.py
- เป็น Python script สำหรับรัน test
- ทำหน้าที่:
  - สร้างชื่อ report ตาม timestamp
  - เรียก `pytest.main(...)` พร้อม generate HTML report
  - เปิด browser เพื่อแสดงผล report หลังจบ test (เฉพาะบน local/dev)
```

pytest                              # ถ้าใช้ร่วมกับ pytest
pytest test_login.py               # รันเฉพาะไฟล์
pytest -k "ชื่อ test"              # รันเฉพาะ test function ที่ชื่อมีคำนี้
---