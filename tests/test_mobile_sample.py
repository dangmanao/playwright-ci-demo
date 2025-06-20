from playwright.sync_api import expect

def test_mobile_view(mobile_page, logger):
    logger.info("เข้าเว็บไซต์ playwright แบบ mobile")
    mobile_page.goto("https://playwright.dev")

    logger.info("ตรวจสอบปุ่ม Get started")
    expect(mobile_page.get_by_text("Get started")).to_be_visible()