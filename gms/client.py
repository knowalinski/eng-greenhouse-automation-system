import requests
import time


url = "http://127.0.0.1:5000"
while True:
    time.sleep(5)
    requests.post(url, data="dupa")