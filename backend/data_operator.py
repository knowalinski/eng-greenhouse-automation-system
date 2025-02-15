import json
import csv
from datetime import datetime
import pandas as pd
import json
import plotly
import plotly.express as px
import random

class TimeOperator:
    def __init__(self) -> None:
        pass
        
    def get_datetime(self):
        '''return timestamp based on actual time'''
        now = datetime.now()
        date_list = [now.day, now.month, now.year]
        time_list = [now.hour, now.minute, now.second]
        return date_list, time_list

    def send_datetime(self):
        '''return dictionary containing timestamp'''
        return {"date": "{:02d}-{:02d}-{}".format(*self.get_datetime()[0]),
                "time": "{:02d}:{:02d}:{:02d}".format(*self.get_datetime()[1])}
    
    def delta_time(self, timestamp: str) -> float:
        '''calculate and return delta of actual time and given timestamp'''
        datetime_object = datetime.strptime(timestamp, '%d-%m-%Y %H:%M:%S')
        deltatime = datetime.now() - datetime_object
        return deltatime.total_seconds()/3600
        return deltatime.total_seconds()/10
        
    
class DataOperator:
    def __init__(self, input_dictionary) -> None:
        
        self.input_dict = input_dictionary
        self._load_json()
        self.values = []
        self.timestamp = []
        self.sensor_id = 0
        
    def _load_json(self) -> None:
        '''decode json input into dictionary'''
        d = json.loads(self.input_dict)
        self.input_dict = d
     
    def _parse_data(self) -> None:
        '''split json sections'''
        self.values = list(self.input_dict.values())[1:4]
        self.timestamp = list(self.input_dict.values())[4:6]
        self.sensor_id = list(self.input_dict.values())[0]

    def csv_dump(self) -> None:
        '''store incoming json data in separated csv files for every sensor'''
        self._parse_data()
        d = self.input_dict
        with open(f'backend/dataSensor{d["sensor_id"]}.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(list(d.values()))

class OutputGenerator(TimeOperator):   
    def __init__(self) -> None:
        super().__init__()
        self.latest_records = {}
        self.latest_timestamps = {}
        self.timestamp = ''
        
    def decode_timestamp(self,timestamp_input: str) -> None:
        '''dump data from timestamp into string'''
        self.timestamp = "{} {}".format(*timestamp_input)

           
    def update_records(self, id: str|int, values: list, timestamp: list) -> None:
        '''create and update lists of latest incoming values'''
        self.latest_records[id] = [1,[*values]]
        self.latest_timestamps[id] = [*timestamp]
        # print(self.latest_timestamps)
        
    def update_states(self) -> None:
        '''calculate states of sensors (active/inactive) based on delta time'''
        for key in self.latest_timestamps:
            self.decode_timestamp(self.latest_timestamps[key])
            if self.delta_time(self.timestamp) > 1:
                self.latest_records[key][0] = 0
                
    def return_output(self) -> dict:
        '''return list of latest records'''
        # print(self.latest_records)
        return self.latest_records
        
    def return_timestamps(self) -> str|dict:
        ''''return list of latest records timestamps'''
        return self.latest_timestamps
    
    
class BoxGenerator:
    def __init__(self, latest_records: dict, latest_timestamps: dict | str) -> None:
        self.input_file = latest_records
        self.timestamps = latest_timestamps
        self.sensor_data = []
        self.sensor_id = 0
        self.html = ''
        self.state = ''
        self.timestamp = ''
        
    def state_class(self) -> str:
        '''change box class based on calculated sensor state'''
        return f'<div class = "{self.state}"><br>\n'

    def sensorID_label(self) -> str:
        '''generate button with value and label based on sensor ID'''
        return f'<form action = "/redirecting" method="POST">\n'\
            f'<button type="submit" name="button" value="{self.sensor_id}">'\
            f'SENSOR {self.sensor_id}</button>\n'\
            f'</form>\n'
                
    def timestamp_labels(self) -> str:
        '''generate label with timestamp of latest record'''
        return '<br><h2>Time of last record {} {}</h2>'.format(*self.timestamp)
        
    def data_labels(self) -> str:
        '''generate labels with reading from lastest record'''
        return '<h2>Air temperature: {:.2f}*C</h2>\n' \
            '<h2>Air humidity: {:.2f}%</h2>\n' \
            '<h2>Soil humidity: {:.2f}%</h2>\n</div>\n'.format(*self.sensor_data)

    def merge(self) -> str:
        '''merge generated lines into one string'''
        a: str = self.state_class()
        b: str = self.sensorID_label()
        c: str = self.data_labels()
        d: str = self.timestamp_labels()
        return a+b+d+c

    def replicate(self) -> None:
        '''create boxes for every sensor contained in list of latest records'''
        for key in self.input_file:
            self.sensor_id = key
            self.state = "activeSensor" if self.input_file[key][0] else "inactiveSensor"
            self.sensor_data = self.input_file[key][1]
            self.timestamp = self.timestamps[key]
            self.html+=self.merge()
    
    def generate_html(self) -> str:
        '''merge generated bits and add immutable parts of html into one string'''
        opener ='<!DOCTYPE html>\n<head>'\
                '\n<title>DASHBOARD</title>'\
                '\n<link rel="stylesheet" href="{{url_for(\'static\', filename=\'css/style.css\')}}">'\
                '\n<meta http-equiv="refresh" content="60"> '\
                '\n</head>'\
                '\n<body>'\
                '\n<h2>DASHBOARD <span id="dash-board"></span></h2>\n'
        self.replicate()
        return opener+self.html+'</body>\n</html>'

    def html_dump(self) -> None:
        '''dump generated string into html file'''
        with open('backend/templates/index.html', 'w') as f:
            f.write(self.generate_html())
            f.close()


class DataPlotter:
    def __init__(self, sensor_id) -> None:
        self.sensor_id = sensor_id

    def return_all_data(self) -> tuple:
        '''create jsons with data from csv files for plotting'''
        with open(f'backend/dataSensor{self.sensor_id}.csv', 'r') as file:
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
        temperature_fig = px.line(temperature_df, x="time",
                                  y="temperature",
                                  title=f"Temperature from sensor {self.sensor_id}")
        humidity_fig = px.line(humidity_df, x="time",
                               y="humidity",
                               title=f"Humidity from sensor {self.sensor_id}")
        moisture_fig = px.line(moisture_df,
                               x="time",
                               y="moisture",
                               title=f"Soil moisture from sensor {self.sensor_id}")

        temperatureJSON = json.dumps(temperature_fig,
                                     cls=plotly.utils.PlotlyJSONEncoder)
        humidityJSON = json.dumps(humidity_fig,
                                  cls=plotly.utils.PlotlyJSONEncoder)
        moistureJSON = json.dumps(moisture_fig,
                                  cls=plotly.utils.PlotlyJSONEncoder)
        
        return temperatureJSON, humidityJSON, moistureJSON