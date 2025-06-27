import pytest
from test_data.login_data_manager import read_login_data_from_csv
from test_data.login_data import LoginTestCase
from keywords.login_keyword import LoginKeywords

test_data = read_login_data_from_csv("test_data/login_data.csv")

@pytest.mark.parametrize("case", test_data)
def test_login_with_keyword_ddt(persistent_page, case: LoginTestCase):
    print(f"🔍 Running with: username={case.username}, password={case.password}, expected={case.expected}")

    kw = LoginKeywords(persistent_page)

    kw.navigate_to_login()
    kw.input_username(case.username)
    kw.input_password(case.password)
    kw.click_login()

    if case.expected == "success":
        kw.should_see_inventory_page()
    else:
        kw.should_see_error_message(case.expected)

        # 👉 Reset browser ระหว่างแต่ละชุด test (optional)
        persistent_page.reload()
