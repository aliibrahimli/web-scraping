import time
import requests
import selectorlib
import smtplib
import ssl


"INSERT INTO events VALUES ('Tigers', 'Tiger City', '2088.10.14')"
URL = "https://programmer100.pythonanywhere.com/tours/"


def scrape(url):
    """Scrape the page source from the URL"""

    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "alibrahimli041@gmail.com"
    password = "pckxbssmffhdbebb"

    receiver = "alibrahimli041@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)


def store(extracted):
    with open("data.txt", 'a') as file:
        file.write(extracted + "\n")


def read():
    with open("data.txt", 'r') as file:
        return file.read()


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        content = read()
        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                send_email(message="Hey, new even was found!")
        time.sleep(0.2)
