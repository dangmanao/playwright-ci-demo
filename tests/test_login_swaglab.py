import requests
from playwright.sync_api import expect
from urllib.parse import urljoin
from pages.login_page import LoginPage


def test_login_success(page, logger):
    # 1. เข้าหน้าเว็บด้วย
    page.goto("https://www.saucedemo.com/v1/")
    # 2. กรอก Username
    page.fill("#user-name", "standard_user")
    # 3. กรอก Password
    page.fill("#password", "secret_sauce")
    # 4. กดปุ่ม Login
    page.click("#login-button")
    # 5. ตรวจสอบว่า URL ถูกต้องหลัง login
    logger.info("ตรวจสอบว่าเจอ URL ที่ถูกต้องหลังจาก Login สำเร็จ")
    expect(page).to_have_url("https://www.saucedemo.com/v1/inventory.html")

def test_login_fail_with_invalid_password(page, logger):
    # 1. เข้าหน้าเว็บด้วย
    page.goto("https://www.saucedemo.com/v1/")
    # 2. กรอก Username
    page.fill("#user-name", "standard_user")
    # 3. กรอก Password
    page.fill("#password", "invalidpassword")
    # 4. กดปุ่ม Login
    page.click("#login-button")
    # 5. ตรวจสอบว่าในกล่อง login มี error message ที่บอกว่า password ไม่ถูกต้องแสดงขึ้นมาไหม
    logger.info("ตรวจสอบว่าเจอ Error message แสดงขึ้นมาถูกต้องไหม")
    expect(page.locator(".login-box", has_text="Epic sadface: Username and password do not match any user in this service")).to_be_visible()

def test_login_fail_with_invalid_username(page, logger):
    # 1. เข้าหน้าเว็บด้วย
    page.goto("https://www.saucedemo.com/v1/")
    # 2. กรอก Username
    page.fill("#user-name", "invalidusername")
    # 3. กรอก Password
    page.fill("#password", "secret_sauce")
    # 4. กดปุ่ม Login
    page.click("#login-button")
    # 5. ตรวจสอบว่าในกล่อง login มี error message ที่บอกว่า username ไม่ถูกต้องแสดงขึ้นมาไหม
    logger.info("ตรวจสอบว่าเจอ Error message แสดงขึ้นมาถูกต้องไหม")
    expect(page.locator(".login-box", has_text="Epic sadface: Username and password do not match any user in this service")).to_be_visible()

def test_login_fail_with_problem_user(page, logger):
    # 1. เข้าหน้าเว็บด้วย
    page.goto("https://www.saucedemo.com/v1/")
    # 2. กรอก Username
    page.fill("#user-name", "problem_user")
    # 3. กรอก Password
    page.fill("#password", "secret_sauce")
    # 4. กดปุ่ม Login
    page.click("#login-button")

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
    # 1. เข้าหน้าเว็บด้วย
    page.goto("https://www.saucedemo.com/v1/")
    # 2. กรอก Username
    page.fill("#user-name", "locked_out_user")
    # 3. กรอก Password
    page.fill("#password", "secret_sauce")
    # 4. กดปุ่ม Login
    page.click("#login-button")
    # 5. ตรวจสอบว่าในกล่อง login มี error message ที่บอกว่า username ไม่ถูกต้องแสดงขึ้นมาไหม
    logger.info("ตรวจสอบว่าเจอ Error message แสดงขึ้นมาถูกต้องไหม")
    expect(page.locator(".login-box", has_text="Epic sadface: Sorry, this user has been locked out.")).to_be_visible()

def test_empty_username(page, logger):
    # 1. เข้าหน้าเว็บด้วย
    page.goto("https://www.saucedemo.com/v1/")
    # 2. กรอก Username
    page.fill("#user-name", "")
    # 3. กรอก Password
    page.fill("#password", "secret_sauce")
    # 4. กดปุ่ม Login
    page.click("#login-button")
    # 5. ตรวจสอบว่าในกล่อง login มี error message ที่บอกว่า username ไม่ถูกต้องแสดงขึ้นมาไหม
    logger.info("ตรวจสอบว่าเจอ Error message แสดงขึ้นมาถูกต้องไหม")
    expect(page.locator(".login-box", has_text="Epic sadface: Username is required")).to_be_visible()

def test_empty_password(page, logger):
    # 1. เข้าหน้าเว็บด้วย
    page.goto("https://www.saucedemo.com/v1/")
    # 2. กรอก Username
    page.fill("#user-name", "standard_user")
    # 3. กรอก Password
    page.fill("#password", "")
    # 4. กดปุ่ม Login
    page.click("#login-button")
    # 5. ตรวจสอบว่าในกล่อง login มี error message ที่บอกว่า username ไม่ถูกต้องแสดงขึ้นมาไหม
    logger.info("ตรวจสอบว่าเจอ Error message แสดงขึ้นมาถูกต้องไหม")
    expect(page.locator(".login-box", has_text="Epic sadface: Password is required")).to_be_visible()