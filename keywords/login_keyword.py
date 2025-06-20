# keywords/login_keywords.py

from pages.login_page import LoginPage

class LoginKeywords:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)

    def navigate_to_login(self):
        self.page.goto("https://www.saucedemo.com/v1/index.html")

    def input_username(self, username):
        self.login_page.username_input.fill(username)

    def input_password(self, password):
        self.login_page.password_input.fill(password)

    def click_login(self):
        self.login_page.login_button.click()

    def should_see_error_message(self, expected):
        actual = self.login_page.error_message.text_content()
        assert actual == expected, f"Expected '{expected}' but got '{actual}'"
    
    def should_see_inventory_page(self):
        assert self.page.url == "https://www.saucedemo.com/v1/inventory.html"
