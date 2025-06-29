import csv

USER_DB = "data/users.csv"

def check_credentials(username, password):
    with open(USER_DB, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return row['role']
    return None
