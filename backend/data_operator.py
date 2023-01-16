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

    
# dict = {"sensor_id":3,"soil_temperature":22.97,"soil_moisture":255,"air_temperature":22.97,"air_humidity":255,"date":"11:01:2023","time":"20:31:17"}
# dataOperator(dict).generate_output()
# DataOperator(dict).csv_dump()
class TimeOperator:
    def __init__(self):
        self.now = ''
        self.date_list = []
        self.time_list = []
    def get_datetime(self):
        self.now = datetime.now()
        date_list = [self.now.day, self.now.month, self.now.year]
        time_list = [self.now.hour, self.now.minute, self.now.second]
        return date_list, time_list
    
    def send_datetime(self):
        return {"date": "{:02d}:{:02d}:{}".format(*self.get_datetime()[0]), "time": "{:02d}:{:02d}:{:02d}".format(*self.get_datetime()[1])}

    
    def compare_time(self, timestamp):
        # TODO: get datetime string from timestamp
        
        datetime_object = datetime.strptime(timestamp, '%d:%m:%y %H:%M:%S')
        deltatime = datetime.now() - datetime_object
        return deltatime.total_seconds()/3600 # * zwraca czas w godzinach

