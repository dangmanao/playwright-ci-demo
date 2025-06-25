import pytest
from keywords.login_keyword import LoginKeywords
from test_data.login_data_manager import LoginTestDataManager

# สร้าง instance ของ data manager และโหลดข้อมูล
data_manager = LoginTestDataManager("test_data/login_data.csv")

# สร้าง test function ธรรมดา (ไม่ใช้ parametrize)
def test_login_with_keyword_oop(page):
    kw = LoginKeywords(page)

    # วน test ทุกชุดจาก CSV
    for data in data_manager.get_all():
        username = data['username']
        password = data['password']
        expected = data['expected']

        print(f"🟢 RUN: {username=}, {password=}, {expected=}")

        # เริ่มทดสอบ
        kw.navigate_to_login()
        kw.input_username(username)
        kw.input_password(password)
        kw.click_login()

        if expected == "success":
            kw.should_see_inventory_page()
        else:
            kw.should_see_error_message(expected)

        # 👉 Reset browser ระหว่างแต่ละชุด test (optional)
        page.reload()
