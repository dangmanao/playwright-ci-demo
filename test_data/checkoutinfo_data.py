# เก็บ test data login
checkoutinfo_test_data = [
    # (firstname, lastname, ,zipcode, expected_result)
    ("", "", "", "Error: First Name is required"),
    ("testfirstname", "", "", "Error: Lastname Name is required"),
    ("", "testlastname","", "Error: First Name is required"),
    ("testfirstname", "testlastname", "", "Error: Postal Code is required"),
    ("testfirstname", "testlastname", "50300", "success")
]
