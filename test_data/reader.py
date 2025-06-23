import csv

def read_login_data_from_csv(filepath):
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [(row['username'], row['password'], row['expected']) for row in reader]
    return data
