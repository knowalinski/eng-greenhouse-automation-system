import time
import csv
import pandas as pd
import plotly
import json
import plotly.express as px


            
def check_time(body):
    def wrapper(*arg, **kw):
        start_time = time.time()
        print(f"Time of parsing .csv file with {body(*arg, **kw)} records is: {time.time()-start_time}\n")
    return wrapper

@check_time
def parse_csv(no_records:int) -> int:
    with open(f"backend/{no_records}records.csv", 'r') as file:
        reader = csv.reader(file)
        temperature = []
        humidity = []
        moisture = []
        time = []
        for row in reader:
            temperature.append(round(float(row[1]),2))
            humidity.append(round(float(row[2]),2))
            moisture.append(round(float(row[3]),2))
            time.append(f"{row[4]} {row[5]}")
    temperature_df = pd.DataFrame(dict(time = time, temperature = temperature))
    humidity_df = pd.DataFrame(dict(time = time, humidity = humidity))
    moisture_df = pd.DataFrame(dict(time = time, moisture = moisture))
    temperature_fig = px.line(temperature_df, x="time", y="temperature", title=f"Temperature from sensor {1}")
    humidity_fig = px.line(humidity_df, x="time", y="humidity", title=f"Humidity from sensor {1}")
    moisture_fig = px.line(moisture_df, x="time", y="moisture", title=f"Soil moisture from sensor {1}")

    temperatureJSON = json.dumps(temperature_fig, cls=plotly.utils.PlotlyJSONEncoder)
    humidityJSON = json.dumps(humidity_fig, cls=plotly.utils.PlotlyJSONEncoder)
    moistureJSON = json.dumps(moisture_fig, cls=plotly.utils.PlotlyJSONEncoder)
    table = [temperatureJSON,humidityJSON,moistureJSON]
    table.remove(temperatureJSON)
    return no_records

parse_csv(10)
parse_csv(100)
parse_csv(1000)
parse_csv(10000)
parse_csv(100000)
parse_csv(1000000)