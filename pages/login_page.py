# นำเข้า Page class จาก Playwright ซึ่งใช้สำหรับควบคุมหน้าเว็บ
from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")
