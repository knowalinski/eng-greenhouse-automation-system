import csv
import os
import matplotlib.pyplot as plt

data_labels = {0: "sensor_id", 1: "temp1", 2: "hum1", 3: "temp2", 4: "hum2", 5: "date", 6: "time"}


def sensor_lister():
    sensors = []
    for i in range(20):
        if os.path.exists(f"dataSensor{i}.csv"):
            sensors.append(f"{i}")
    print(sensors)


def data_reader(sensor_id):
    # with open(f"dataSensor{sensor_id}.csv") as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=',')
    csv_file = open(f"dataSensor{sensor_id}.csv")
    csv_reader = csv.reader(csv_file, delimiter=',')
    return csv_reader
    # for row in csv_reader:
    #     print(
    #         f"sensor id: {row[0]}, temperature1: {row[1]}, hum1: {row[2]}, temp2: {row[3]}, hum2: {row[4]}, date: {row[5]}, time: {row[6]}")


def data_printer(sensor_id):
    data = data_reader(sensor_id)
    for row in data:
        print(
            f"sensor id: {row[0]}, temperature1: {row[1]}, hum1: {row[2]}, temp2: {row[3]}, hum2: {row[4]}, date: {row[5]}, time: {row[6]}")


def get_data(data_code, sensor_id):
    data = data_reader(sensor_id)
    for row in data:
        print(f"{data_labels[data_code]}:{row[data_code]}")


def plot_data(data_code, sensor_id):
    data = data_reader(sensor_id)
    x_axis = []
    y_axis = []
    for row in data:
        y_axis.append(row[data_code])
    plt.plot(y_axis)
    plt.ylabel(f"{data_labels[data_code]}")
    plt.show()

def get_one_day_data(data_code, sensor_id, date):
    data = data_reader(sensor_id)
    print(date)
    print(type(date))
    print(list(date))
    for row in data:
        if date in row[5]:
            print(f"{data_labels[data_code]}:{row[data_code]}")


# data_reader(3)
# sensor_lister()
# data_printer(3)
lab = [3, 3]
# get_data(*lab)
# plot_data(*lab)
date = "08:01:2023"
get_one_day_data(*lab, date)
# data_parser(3)
