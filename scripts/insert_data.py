import random
import uuid
from datetime import datetime, timedelta

import lorem
import requests


def generate_random_date(start_year=2000, end_year=2050):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    time_between_dates = end_date - start_date
    random_number_of_days = random.randrange(time_between_dates.days)
    return start_date + timedelta(days=random_number_of_days)


def create_message(url, author, date, body):
    payload = {"author": author, "date": date.isoformat(), "body": body}
    response = requests.post(url, json=payload)
    return response


API_URL = "http://localhost:8090/messages/"

for i in range(500):
    author = str(uuid.uuid4())
    date = generate_random_date()
    body = lorem.text()[: random.randint(50, 500)]
    response = create_message(API_URL, author, date, body)
    if response.status_code == 200:
        print(f"Message {i} created")
    else:
        print(f"Error {response.status_code}")
