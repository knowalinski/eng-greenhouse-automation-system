import requests
import json
import random
import time
from datetime import datetime

post_url = 'http://127.0.0.1:5000/data-collector'

def random_output(start:int, stop:int, accuracy:int) -> float:
    return round(random.uniform(start,stop),accuracy)

def get_datetime() -> tuple:
    now = datetime.now()
    date_list = [now.day, now.month, now.year]
    time_list = [now.hour, now.minute, now.second]
    return date_list, time_list

def mock_sensor(body):
    def wrapper(*arg, **kw):
        requests.post(post_url, body(*arg, **kw))
    return wrapper

@mock_sensor
def generate_dataframe(sensor_id = None):
    print("dataframe generated")
    sensor_id = random.randint(3,9) if sensor_id == None else sensor_id
    return json.dumps({"sensor_id": sensor_id,
        "air_temperature": random_output(40,50,2),
        "air_humidity": random_output(20,25,2), 
        "soil_moisture": random_output(0,50,1),
        "date": "{:02d}-{:02d}-{}".format(*get_datetime()[0]),
        "time": "{:02d}:{:02d}:{:02d}".format(*get_datetime()[1])})


if __name__ == "__main__":
    while True:
        generate_dataframe(sensor_id="1")
        generate_dataframe(sensor_id="2")
        # generate_dataframe(sensor_id="North")
        # generate_dataframe(sensor_id="South")
        # generate_dataframe(sensor_id="Center")
        # generate_dataframe(sensor_id="Outside")
        time.sleep(10)
