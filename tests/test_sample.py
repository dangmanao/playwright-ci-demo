from playwright.sync_api import expect

def test_example(page, logger):
    logger.info("เริ่มเข้าเว็บไซต์ Playwright")
    page.goto("https://playwright.dev")

    logger.info("ตรวจสอบข้อความ Welcome")
    expect(page.get_by_text("Get started")).to_be_visible()
