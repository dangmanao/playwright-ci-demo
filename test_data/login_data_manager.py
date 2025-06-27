from test_data.login_data import LoginTestCase
import csv

def read_login_data_from_csv(filepath):
    test_cases = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            test_cases.append(LoginTestCase(
                username=row['username'],
                password=row['password'],
                expected=row['expected']
            ))
    return test_cases