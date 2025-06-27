import pytest
from playwright.sync_api import sync_playwright
from utils.logger import get_logger
import datetime

# ✅ Logger fixture ใช้ร่วมกันทั้ง session
@pytest.fixture(scope="session")
def logger():
    return get_logger("TestLogger")


# ──────────────────────────────────────────────
# ✅ Fixture 1: เปิด browser ใหม่ "ทุกเทส" (Fresh Desktop)
# ──────────────────────────────────────────────
@pytest.fixture(scope="function")
def fresh_page(logger):
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False, slow_mo=300)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        yield page

        # 🔴 ถ้าเทส fail → เก็บ screenshot
        if hasattr(page, '_did_fail') and page._did_fail:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/fail_{timestamp}.png"
            page.screenshot(path=filename)
            logger.info(f"[SCREENSHOT SAVED] {filename}")

        context.close()
        browser.close()


# ──────────────────────────────────────────────
# ✅ Fixture 2: เปิด browser ค้างไว้ (Persistent Desktop)
# ──────────────────────────────────────────────
@pytest.fixture(scope="module")
def persistent_page(logger):
    p = sync_playwright().start()
    browser = p.chromium.launch(channel="chrome", headless=False, slow_mo=300)
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    yield page

    # 🔴 NOTE: ไม่เช็ค fail screenshot ใน persistent (แต่เพิ่มได้)
    context.close()
    browser.close()
    p.stop()


# ──────────────────────────────────────────────
# ✅ Fixture 3: เปิด browser ใหม่ "ทุกเทส" (Fresh Mobile)
# ──────────────────────────────────────────────
@pytest.fixture(scope="function")
def fresh_mobile_page(logger):
    with sync_playwright() as p:
        iphone = p.devices["iPhone 13"]
        browser = p.chromium.launch(headless=False, slow_mo=300)
        context = browser.new_context(**iphone)
        page = context.new_page()
        yield page

        if hasattr(page, '_did_fail') and page._did_fail:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/fail_mobile_{timestamp}.png"
            page.screenshot(path=filename)
            logger.info(f"[MOBILE SCREENSHOT SAVED] {filename}")

        context.close()
        browser.close()


# ──────────────────────────────────────────────
# ✅ Fixture 4: เปิด browser ค้างไว้ (Persistent Mobile)
# ──────────────────────────────────────────────
@pytest.fixture(scope="module")
def persistent_mobile_page(logger):
    p = sync_playwright().start()
    iphone = p.devices["iPhone 13"]
    browser = p.chromium.launch(headless=False, slow_mo=300)
    context = browser.new_context(**iphone)
    page = context.new_page()
    yield page

    context.close()
    browser.close()
    p.stop()


# ──────────────────────────────────────────────
# ✅ Hook: ตรวจจับว่า test case ไหน fail แล้ว set flag
# ──────────────────────────────────────────────
def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        for key in ["fresh_page", "fresh_mobile_page"]:
            page = item.funcargs.get(key, None)
            if page:
                # ตั้ง flag ว่า test นี้ล้มเหลว → เพื่อให้ fixture ไปถ่าย screenshot
                page._did_fail = True
