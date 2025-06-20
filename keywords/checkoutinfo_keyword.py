# keywords/login_keywords.py

from pages.checkoutinfo_page import CheckoutInfoPage

class CheckoutInfoKeywords:
    def __init__(self, page):
        self.page = page
        self.checkoutinfo_page = CheckoutInfoPage(page)

    def input_firstname(self, firstname):
        self.checkoutinfo_page.firstname_input.fill(firstname)

    def input_lastname(self, lastname):
        self.checkoutinfo_page.lastname_input.fill(lastname)

    def input_zipcode(self, zipcode):
        self.checkoutinfo_page.zipcode_input.fill(zipcode)

    def click_continue_button(self):
        self.checkoutinfo_page.continue_button.click()

    def should_see_error_message(self, expected):
        actual = self.checkoutinfo_page.error_message.text_content()
        assert actual == expected, f"Expected '{expected}' but got '{actual}'"
