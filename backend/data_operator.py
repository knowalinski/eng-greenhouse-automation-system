import json
import csv

class Data_operator:
    def __init__(self, input_dict):
        self.input_dict = input_dict
        self.output_dict = {}
        self.values = []
        self.timestamp = []
        self.sensor_id = 0
    def convert_data(self):
        d = json.loads(self.input_dict)
        self.input_dict = d
        # print(d["sensor_id"])
    def get_data(self):
        self.values = list(self.input_dict.values())[1:5]
        self.timestamp = list(self.input_dict.values())[5:7]
        self.sensor_id = list(self.input_dict.values())[0]
        # self.output_dict[self.input_dict["sensor_id"]] = [1,[]]
    
    def generate_output(self):
        self.get_data()
        self.output_dict[self.sensor_id] = [1,[*self.values]]

    def csv_dump(self):
        # d = json.loads(self.input_dict)
        # print(d["sensor_id"])
        self.convert_data()
        d = self.input_dict
        with open(f'backend/dataSensor{d["sensor_id"]}.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(list(d.values()))

# dict = {"sensor_id":3,"soil_temperature":22.97,"soil_moisture":255,"air_temperature":22.97,"air_humidity":255,"date":"11:01:2023","time":"20:31:17"}
# Data_operator(dict).generate_output()
# Data_operator(dict).csv_dump()