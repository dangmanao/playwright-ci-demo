import requests
from playwright.sync_api import expect
from urllib.parse import urljoin
from pages.login_page import LoginPage


def test_login_success(page, logger):
    # สร้างอ็อบเจกต์ login_page โดยส่ง page เข้าไปให้ class LoginPage ใช้งาน
    login_page = LoginPage(page)
    # เรียกใช้เมธอด navigate() เพื่อเข้าไปยังหน้า login
    login_page.navigate()
    # เรียกใช้เมธอด login() เพื่อกรอก username, password และคลิกปุ่ม login
    login_page.login("standard_user", "secret_sauce")
    logger.info("ตรวจสอบว่าเจอ URL ที่ถูกต้องหลังจาก Login สำเร็จ")
    expect(page).to_have_url("https://www.saucedemo.com/v1/inventory.html")

def test_login_fail_with_invalid_password(page, logger):
    # สร้างอ็อบเจกต์ login_page โดยส่ง page เข้าไปให้ class LoginPage ใช้งาน
    login_page = LoginPage(page)
    # เรียกใช้เมธอด navigate() เพื่อเข้าไปยังหน้า login
    login_page.navigate()
    # เรียกใช้เมธอด login() เพื่อกรอก username, password และคลิกปุ่ม login
    login_page.login("standard_user", "invalidpassword")
    # 5. ตรวจสอบว่าในกล่อง login มี error message ที่บอกว่า password ไม่ถูกต้องแสดงขึ้นมาไหม
    logger.info("ตรวจสอบว่าเจอ Error message แสดงขึ้นมาถูกต้องไหม")
    expect(page.locator(".login-box", has_text="Epic sadface: Username and password do not match any user in this service")).to_be_visible()

def test_login_fail_with_invalid_username(page, logger):
    # สร้างอ็อบเจกต์ login_page โดยส่ง page เข้าไปให้ class LoginPage ใช้งาน
    login_page = LoginPage(page)
    # เรียกใช้เมธอด navigate() เพื่อเข้าไปยังหน้า login
    login_page.navigate()
    # เรียกใช้เมธอด login() เพื่อกรอก username, password และคลิกปุ่ม login
    login_page.login("invalidusername", "secret_sauce")
    # 5. ตรวจสอบว่าในกล่อง login มี error message ที่บอกว่า username ไม่ถูกต้องแสดงขึ้นมาไหม
    logger.info("ตรวจสอบว่าเจอ Error message แสดงขึ้นมาถูกต้องไหม")
    expect(page.locator(".login-box", has_text="Epic sadface: Username and password do not match any user in this service")).to_be_visible()

def test_login_fail_with_problem_user(page, logger):
    # สร้างอ็อบเจกต์ login_page โดยส่ง page เข้าไปให้ class LoginPage ใช้งาน
    login_page = LoginPage(page)
    # เรียกใช้เมธอด navigate() เพื่อเข้าไปยังหน้า login
    login_page.navigate()
    # เรียกใช้เมธอด login() เพื่อกรอก username, password และคลิกปุ่ม login
    login_page.login("problem_user", "secret_sauce")

    images = page.locator("img.inventory_item_img")
    # 🔹 หา element ของรูปภาพสินค้า (selector class ของรูป)
    total = images.count()
    # 🔹 นับว่ามีทั้งหมดกี่รูป (กี่สินค้า)
    for i in range(total):
            src = images.nth(i).get_attribute("src")  # ดึงค่า src (อาจเป็น relative)
            full_url = urljoin("https://www.saucedemo.com/v1/", src)         # ✅ รวม base URL กับ src

            print(f"🔍 Checking image {i+1}: {full_url}")

            #try:
            response = requests.get(full_url)
            logger.info("ตรวจสอบว่ารูปต้องโหลดไม่ขึ้น")
            assert response.status_code == 404, f"Image {i+1} โหลดไม่สำเร็จ (status: {response.status_code})"

def test_login_fail_with_lock_user(page, logger):
    # สร้างอ็อบเจกต์ login_page โดยส่ง page เข้าไปให้ class LoginPage ใช้งาน
    login_page = LoginPage(page)
    # เรียกใช้เมธอด navigate() เพื่อเข้าไปยังหน้า login
    login_page.navigate()
    # เรียกใช้เมธอด login() เพื่อกรอก username, password และคลิกปุ่ม login
    login_page.login("locked_out_user", "secret_sauce")
    # 5. ตรวจสอบว่าในกล่อง login มี error message ที่บอกว่า username ไม่ถูกต้องแสดงขึ้นมาไหม
    logger.info("ตรวจสอบว่าเจอ Error message แสดงขึ้นมาถูกต้องไหม")
    expect(page.locator(".login-box", has_text="Epic sadface: Sorry, this user has been locked out.")).to_be_visible()

def test_empty_username(page, logger):
    # สร้างอ็อบเจกต์ login_page โดยส่ง page เข้าไปให้ class LoginPage ใช้งาน
    login_page = LoginPage(page)
    # เรียกใช้เมธอด navigate() เพื่อเข้าไปยังหน้า login
    login_page.navigate()
    # เรียกใช้เมธอด login() เพื่อกรอก username, password และคลิกปุ่ม login
    login_page.login("", "secret_sauce")
    # 5. ตรวจสอบว่าในกล่อง login มี error message ที่บอกว่า username ไม่ถูกต้องแสดงขึ้นมาไหม
    logger.info("ตรวจสอบว่าเจอ Error message แสดงขึ้นมาถูกต้องไหม")
    expect(page.locator(".login-box", has_text="Epic sadface: Username is required")).to_be_visible()

def test_empty_password(page, logger):
    # สร้างอ็อบเจกต์ login_page โดยส่ง page เข้าไปให้ class LoginPage ใช้งาน
    login_page = LoginPage(page)
    # เรียกใช้เมธอด navigate() เพื่อเข้าไปยังหน้า login
    login_page.navigate()
    # เรียกใช้เมธอด login() เพื่อกรอก username, password และคลิกปุ่ม login
    login_page.login("standard_user", "")
    # 5. ตรวจสอบว่าในกล่อง login มี error message ที่บอกว่า username ไม่ถูกต้องแสดงขึ้นมาไหม
    logger.info("ตรวจสอบว่าเจอ Error message แสดงขึ้นมาถูกต้องไหม")
    expect(page.locator(".login-box", has_text="Epic sadface: Password is required")).to_be_visible()