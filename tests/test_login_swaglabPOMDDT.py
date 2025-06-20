# นำเข้า pytest ซึ่งเป็น testing framework ที่เราใช้รัน test
import pytest
# นำเข้า LoginPage class จากไฟล์ page object
from pages.login_page import LoginPage
# นำเข้า test data (list ของชุดข้อมูล login) จากไฟล์ login_data.py
from test_data.login_data import login_test_data
# ใช้ decorator ของ pytest เพื่อกำหนดว่า test function นี้จะถูกรันซ้ำหลายครั้ง โดยใช้ค่าจาก login_test_data
# แต่ละครั้งจะ map ค่าใน tuple → (username, password, expected) ไปให้กับ parameter ของ test function
@pytest.mark.parametrize("username, password, expected", login_test_data)
def test_login_ddt(page, username, password, expected):
    # สร้าง object ของ LoginPage โดยส่ง page (browser tab ที่เปิดอยู่) เข้าไปให้ class
    login_page = LoginPage(page)
    # สั่งให้เปิดหน้า login (navigate ไปยัง URL)
    login_page.navigate()
    # ทำการ login โดยใช้ username และ password จาก test data ชุดนั้น
    login_page.login(username, password)
    # ตรวจสอบผลลัพธ์ของแต่ละกรณี (แยกเงื่อนไข)
    if expected == "success":
        # ถ้า expected เป็น "success" แสดงว่า login ต้องสำเร็จ
        # → ตรวจสอบว่าเราเข้าไปยังหน้า inventory ได้หรือไม่
        assert page.url == "https://www.saucedemo.com/v1/inventory.html"
    else:
        # ถ้าไม่สำเร็จ ให้ตรวจสอบว่า error message บนหน้าจอตรงกับ expected หรือไม่
        assert login_page.get_error_message() == expected
