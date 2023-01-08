from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
import json
import csv
from datetime import datetime


# TODO: dodać routing i threading

# from waitress import serve


def parser(some_json):
    d = json.loads(some_json)
    # d_keys = list(d.keys())
    # d_values = list(d.values())
    print(d["sensor_id"])
    with open(f'dataSensor{d["sensor_id"]}.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list(d.values()))

    #     # writer.writerows(some_json)
    # print(*r_data.keys(), *r_data.values())


# baza części serverowej, póki co tylko odbiera POSTa
# TODO: json parser
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    return "stary wstał"


@app.route("/data-collector", methods=['POST'])
def collector():
    if request.method == "POST":
        try:
            # print(request.data)
            # print(json.loads(request.data.decode("utf-8")))
            # print(type(json.loads(request.data)))
            parser(request.data)
        except ValueError:
            print("Decoding failed")
    print(request.data)
    return "test"


@app.route("/get-datetime", methods=['GET'])
def date_time():
    now = datetime.now()
    # date_list = [now.strftime("%d"),now.strftime("%m"),now.strftime("%Y")]
    # time_list = [now.strftime("%H"), now.strftime("%M"), now.strftime("%S") ]
    date_list = [now.day, now.month, now.year]
    time_list = [now.hour, now.minute, now.second]
    date_time_dict = {"date": date_list, "time": time_list}
    print(json.dumps(date_time_dict))
    return json.dumps(date_time_dict)



if __name__ == "__main__":
    # serve(app, host="0.0.0.0", threads=2)
    # host 0.0.0.0 po to, żeby odpaliło się w sieci lokalnej a nie tylko na localhoscie
    app.run(host="0.0.0.0")
