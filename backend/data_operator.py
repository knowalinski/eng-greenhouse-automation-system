import json
import csv
from datetime import datetime
# ! 22:31 16.01.2023 - DataOperator zaczął działać dobrze - szkoda, że nie wiem czemu xD
class DataOperator:
    def __init__(self, input_dictionary):
        
        self.input_dict = input_dictionary
        self.convert_data()
        self.output_dict = {}
        self.values = []
        self.timestamp = []
        self.sensor_id = 0
        self.now = ''
    def convert_data(self):
        d = json.loads(self.input_dict)
        self.input_dict = d
    def get_data(self):
        self.values = list(self.input_dict.values())[1:5]
        self.timestamp = list(self.input_dict.values())[5:7]
        self.sensor_id = list(self.input_dict.values())[0]
        # self.output_dict[self.input_dict["sensor_id"]] = [1,[]]
        
    def get_sensorid(self):
        self.get_data()
        return list(self.input_dict.values())[0]
    
    def get_values(self):
        self.get_data()
        return list(self.input_dict.values())[1:5]
    
    
    def csv_dump(self):
        self.get_data()
        d = self.input_dict
        with open(f'backend/dataSensor{d["sensor_id"]}.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(list(d.values()))

    

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

    def compare_time(self, timestamp):
        # TODO: get datetime string from timestamp
        datetime_object = datetime.strptime(timestamp, '%d-%m-%y %H:%M:%S')
        deltatime = datetime.now() - datetime_object
        return deltatime.total_seconds()/3600 # * zwraca czas w godzinach



class BoxGenerator(TimeOperator):
    def __init__(self, input_dict):
        super().__init__()
        self.input_file = input_dict
        self.sensor_data = []
        self.sensor_id = 0
        self.html = ''
        self.state = ''
    def check_state(self, sensor_state):
        if sensor_state == 1:
            self.state = "activeSensor"
        else:
            self.state = "inactiveSensor"
    
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
        self.check_state()
        a = self.state_class()
        b = self.sensorID_label()
        c = self.data_labels()
        return a+b+c

    def replicate(self):
        for key in self.input_file:
            self.sensor_id = key
            self.state = self.input_file[key][0]
            self.sensor_data = self.input_file[key][1]
            self.html+=self.merge()
    
    def generate(self):
        opener ='<!DOCTYPE html>\n<head>'\
                '\n<title>DASHBOARD</title>'\
                '\n<link rel="stylesheet" href="{{url_for(\'static\', filename=\'css/style.css\')}}">'\
                '\n</head>'\
                '\n<body>'\
                '\n<h2>DASHBOARD <span id="dash-board"></span></h2>'\
                '\n<button id = goto-plotting>plotting</button>\n'
        self.replicate()
        return opener+self.html+'</body>\n</html>'

    def html_dump(self):
            with open('backend/templates/index.html', 'w') as f:
                f.write(self.generate())
                f.close()

