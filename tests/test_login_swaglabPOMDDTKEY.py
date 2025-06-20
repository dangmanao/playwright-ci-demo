# นำเข้า pytest ซึ่งเป็น testing framework ที่เราใช้รัน test
import pytest

# นำเข้า LoginPage class จากไฟล์ page object
# (จริง ๆ ไม่ได้ใช้ในไฟล์นี้โดยตรง อาจจะลบได้ถ้าไม่มีใช้งานเนื่องจาก keyword ที่ใช้มีการ import page ในส่วนนั้นแล้ว)
# from pages.login_page import LoginPage

# นำเข้า test data (list ของชุดข้อมูล login) จากไฟล์ login_data.py
from test_data.login_data import login_test_data

# นำเข้า class ที่เก็บ action (keyword) สำหรับ login
from keywords.login_keyword import LoginKeywords

# ใช้ decorator ของ pytest เพื่อกำหนดว่า test function นี้จะถูกรันซ้ำหลายครั้ง โดยใช้ค่าจาก login_test_data
# แต่ละครั้งจะ map ค่าใน tuple → (username, password, expected) ไปให้กับ parameter ของ test function
@pytest.mark.parametrize("username, password, expected", login_test_data)
def test_login_with_keyword_ddt(page, username, password, expected):
    # สร้าง instance ของ LoginKeywords เพื่อเรียกใช้คำสั่ง keyword ต่าง ๆ
    kw = LoginKeywords(page)
    # Step 1: เปิดหน้า login ของระบบ
    kw.navigate_to_login()
    # Step 2: กรอก username ที่รับมาจาก test data
    kw.input_username(username)
    # Step 3: กรอก password จาก test data
    kw.input_password(password)
    # Step 4: คลิกปุ่ม login
    kw.click_login()
    # Step 5: ตรวจสอบผลลัพธ์ที่คาดหวังจาก test data
    if expected == "success":
        # ถ้า login สำเร็จ ให้ตรวจสอบว่าอยู่ในหน้า inventory แล้ว
        kw.should_see_inventory_page()
    else:
        # ถ้า login ไม่สำเร็จ ให้ตรวจสอบว่าข้อความ error ที่แสดงตรงกับที่คาดไว้
        kw.should_see_error_message(expected)
