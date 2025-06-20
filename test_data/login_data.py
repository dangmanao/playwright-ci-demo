# เก็บ test data login
login_test_data = [
    # (username, password, expected_result)
    ("standard_user", "secret_sauce", "success"),
    ("standard_user", "invalidpassword", "Epic sadface: Username and password do not match any user in this service"),
    ("invalidusername", "secret_sauce", "Epic sadface: Username and password do not match any user in this service"),
    ("standard_user", "", "Epic sadface: Password is required"),
    ("", "secret_sauce", "Epic sadface: Username is required"),
    ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked outs.")
]
