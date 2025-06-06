import requests
import selectorlib
import smtplib, ssl
import os
import time
import sqlite3
URL = 'https://programmer100.pythonanywhere.com/tours/'

"INSERT INTO events VALUES ('Tigers', 'Tiger City', '2088.10.14')"
"SELECT * FROM events WHERE date='2088.10.15"

connection = sqlite3.connect("data1.db")


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "USERNAME_EMAIL"
    password = "PASWORD"

    receiver = "RECEIVER_EMAIL"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

def scrape(url):
    source = requests.get(url)
    text = source.text
    return text

def extract(source):
    jaml = selectorlib.Extractor.from_yaml_file('extract.yaml')
    co = jaml.extract(source)["tours"]
    return co

def store(extracted):
    row = extracted.split(',')
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute('INSERT INTO events VALUES(?,?,?)', row)
    connection.commit()

def read(extracted):
    row = extracted.split(',')
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows

if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        if extracted != 'No upcoming tours':
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(message='Hey, new event was found!')
        time.sleep(2)
