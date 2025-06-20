# นำเข้า Page class จาก Playwright ซึ่งใช้สำหรับควบคุมหน้าเว็บ
from playwright.sync_api import Page

class CheckoutInfoPage:
    def __init__(self, page):
        self.page = page
        self.firstname_input = page.locator("#first-name")
        self.lastname_input = page.locator("#last-name")
        self.zipcode_input = page.locator("#postal-code")
        self.continue_button = page.get_by_role("button", name="CONTINUE")
        self.error_message = page.locator("[data-test='error']")
