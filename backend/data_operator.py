import json
import csv
from datetime import datetime


class TimeOperator:
    def __init__(self):
        pass

    def get_datetime(self):
        now = datetime.now()
        date_list = [now.day, now.month, now.year]
        time_list = [now.hour, now.minute, now.second]
        return date_list, time_list

    def send_datetime(self):
        return {"date": "{:02d}-{:02d}-{}".format(*self.get_datetime()[0]), "time": "{:02d}:{:02d}:{:02d}".format(*self.get_datetime()[1])}
    
    def delta_time(self, timestamp):
        datetime_object = datetime.strptime(timestamp, '%d-%m-%Y %H:%M:%S')
        deltatime = datetime.now() - datetime_object
        # print (deltatime)
        # return deltatime.total_seconds()/3600 # * zwraca czas w godzinach
        return deltatime.total_seconds()/10 # * zwraca czas w godzinach
        
    
class DataOperator:
    # ładowanie inputu w json-ie
    # parsowanie json-a
    # zrzucanie wartości do csv
    def __init__(self, input_dictionary):
        
        self.input_dict = input_dictionary
        self._load_json()
        self.values = []
        self.timestamp = []
        self.sensor_id = 0
        
    def _load_json(self):
        d = json.loads(self.input_dict)
        self.input_dict = d
        
    def parse_data(self):
        self.values = list(self.input_dict.values())[1:5]
        self.timestamp = list(self.input_dict.values())[5:7]
        self.sensor_id = list(self.input_dict.values())[0]
    
    def csv_dump(self):
        self.parse_data()
        d = self.input_dict
        with open(f'backend/dataSensor{d["sensor_id"]}.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(list(d.values()))

class OutputGenerator(TimeOperator):
    # generowanie słownika z ostatnimi rekordami
    # generowanie słownika stanów
    def __init__(self):
        # latest records = {id:[timestamp, state]}
        super().__init__()
        self.latest_records = {}
        self.latest_timestamps = {}
        self.timestamp = ''
    def decode_timestamp(self,timestamp_input):
        self.timestamp = "{} {}".format(*timestamp_input)
        print(self.timestamp)
        
        
    def update_records(self,id, values,timestamp):
        self.latest_records[id] = [1,[*values]]
        self.latest_timestamps[id] = [*timestamp]
        
    def update_states(self):
        for key in self.latest_timestamps:
            self.decode_timestamp(self.latest_timestamps[key])
            # self.delta_time(self.timestamp)
            if self.delta_time(self.timestamp) > 1:
                self.latest_records[key][0] = 0
                
    def return_output(self):
        print(self.latest_records)
        return self.latest_records
        
    

class BoxGenerator:
    def __init__(self, input_dict):
        self.input_file = input_dict
        self.sensor_data = []
        self.sensor_id = 0
        self.html = ''
        self.state = ''
    # def check_state(self, sensor_state):
    #     if sensor_state == 1:
    #         self.state = "activeSensor"
    #     else:
    #         self.state = "inactiveSensor"
    
    def state_class(self):
        return f'<div class = "{self.state}"><br>\n'

    def sensorID_label(self):
        return f'<label>sensor_{self.sensor_id}</label>\n'

    def data_labels(self):
        return '<br><label>Air temperature: {}</label><br>\n' \
            '<label>Air humidity: {}</label><br>\n' \
                '<label>Soil temperature: {}</label><br>\n' \
                    '<label>Soil humidity: {}</label><br>\n</div>\n'.format(*self.sensor_data)

    def merge(self):
        a = self.state_class()
        b = self.sensorID_label()
        c = self.data_labels()
        return a+b+c

    def replicate(self):
        for key in self.input_file:
            self.sensor_id = key
            self.state = "activeSensor" if self.input_file[key][0] else "inactiveSensor"
            self.sensor_data = self.input_file[key][1]
            self.html+=self.merge()
    
    def generate_html(self):
        opener ='<!DOCTYPE html>\n<head>'\
                '\n<title>DASHBOARD</title>'\
                '\n<link rel="stylesheet" href="{{url_for(\'static\', filename=\'css/style.css\')}}">'\
                '\n<meta http-equiv="refresh" content="60"> '\
                '\n</head>'\
                '\n<body>'\
                '\n<h2>DASHBOARD <span id="dash-board"></span></h2>'\
                '\n<button id = goto-plotting>plotting</button>\n'
        self.replicate()
        return opener+self.html+'</body>\n</html>'

    def html_dump(self):
            with open('backend/templates/index.html', 'w') as f:
                f.write(self.generate_html())
                f.close()

