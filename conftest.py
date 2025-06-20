# นำเข้า pytest เพื่อใช้งาน fixture
import pytest
# นำเข้า sync_playwright สำหรับเปิด browser แบบ synchronous
from playwright.sync_api import sync_playwright
# นำเข้า logger ที่สร้างไว้ใช้งานร่วมกัน
from utils.logger import get_logger
# นำเข้า os และ datetime สำหรับสร้างชื่อไฟล์ screenshot
import os
import datetime

# ✅ Fixture: สร้าง logger หนึ่งตัว ใช้ร่วมกันทั้ง session (รันครั้งเดียว)
@pytest.fixture(scope="session")
def logger():
    return get_logger("TestLogger")

# ✅ Dynamic Parametrize เพื่อรันซ้ำหลาย browser
def pytest_generate_tests(metafunc):
    if "browser_name" in metafunc.fixturenames:
       metafunc.parametrize("browser_name", ["chromium"])  # หรือเพิ่ม firefox ได้ด้วย ถ้าต้องการให้ run กี่ browser ให้มาปรับตรงนี้โดยที่ ลบ หรือ เพิ่ม ชื่อ browser ใน [] "msedge" อันนี้คือ edge

# ✅ Fixture: สำหรับรัน test แบบ desktop browser
# ทำงานทุกครั้งที่มี test (function scope)
# ✅ Fixture ที่เปิด browser ตาม browser_name ที่ส่งมา
@pytest.fixture(scope="function")
def page(browser_name, logger):
    with sync_playwright() as p:
        if browser_name == "chromium":
            browser = p.chromium.launch(channel="chrome", headless=False, slow_mo=100, args=["--start-maximized"])
        elif browser_name == "msedge":
            browser = p.chromium.launch(channel="msedge", headless=False, slow_mo=500, args=["--start-maximized"])
        else:
            raise ValueError(f"ไม่รู้จัก browser: {browser_name}")

        # สร้าง browser context ใหม่ (เหมือนเปิดหน้าต่างใหม่)
        context = browser.new_context(no_viewport=True)
        # สร้างหน้าเว็บใหม่ใน context นี้ โดยใช้แบบ Full screen
        page = context.new_page()
        yield page  # ส่ง page object ไปให้ test ใช้งาน

        # ตรวจสอบว่า test นี้ fail หรือไม่ แล้วเก็บ screenshot ถ้า fail
        if hasattr(page, '_did_fail') and page._did_fail:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/fail_{timestamp}.png"
            page.screenshot(path=f"reports/{browser_name}_fail_{timestamp}.png")
            logger.info(f"[SCREENSHOT SAVED] {filename}")

        # ปิด browser context และตัว browser
        context.close()
        browser.close()

# ✅ Fixture: สำหรับรัน test แบบ mobile browser โดยใช้ preset iPhone 13
@pytest.fixture(scope="function")
def mobile_page(logger):
    with sync_playwright() as p:
        # ใช้ preset device profile ของ iPhone 13 ที่ Playwright เตรียมไว้ให้
        iphone = p.devices["iPhone 13"]
        # เปิด browser แบบ headful และ slowMo 1000ms
        browser = p.chromium.launch(headless=False, slow_mo=100)
        # สร้าง browser context ใหม่ตาม config ของ iPhone 13
        context = browser.new_context(**iphone)
        # สร้างหน้าใหม่ใน context นั้น
        page = context.new_page()
        yield page  # ส่ง page object ให้ test ใช้งาน

        # ถ้า test fail ให้เก็บ screenshot
        if hasattr(page, '_did_fail') and page._did_fail:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/fail_mobile_{timestamp}.png"
            page.screenshot(path=filename)
            logger.info(f"[MOBILE SCREENSHOT SAVED] {filename}")

        # ปิด context และ browser หลัง test เสร็จ
        context.close()
        browser.close()

# ✅ Hook ของ pytest: ทำงานหลังจากแต่ละ test case จบลง
# ใช้สำหรับเช็คว่า test fail หรือไม่ แล้วตั้ง flag `_did_fail`
def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        # ตรวจสอบว่ามีการใช้ page หรือ mobile_page ใน test หรือไม่
        for key in ["page", "mobile_page"]:
            page = item.funcargs.get(key, None)
            if page:
                # ตั้ง flag เพื่อให้ fixture ด้านบนรู้ว่า test นี้ fail
                page._did_fail = True