from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
import json
import csv
from datetime import datetime
from data_operator import DataOperator, TimeOperator
# from waitress import serve
html = '    <div class = "sensor">\n<label for = "sensor_id">box from html</label>\n<br><label for = "">Air temperature:</label><br>\n<label for = "">Air humidity:</label><br>\n<label for = "">Soil temperature:</label><br>\n<label for = "">Soil humidity:</label><br>\n</div>'

# def parser(some_json):
#     d = json.loads(some_json)
#     print(d["sensor_id"])
#     with open(f'backend/dataSensor{d["sensor_id"]}.csv', 'a', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(list(d.values()))

# def html_generator():
#     with open('backend/templates/assets/ending.html', 'w') as f:
#         f.write(html)
#         f.close()
        


app = Flask(__name__)


# TODO: dodać routy dla dashboardu i plottera


# ! route testowy - później zostanie usunięty
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')
    

# * route dodbierający ramki danych z esp32
@app.route("/data-collector", methods=['POST'])
def collector():
    if request.method == "POST":
        try:
            # TODO: dodać zapisywanie ostatniej wartości dla każdego czujnika do słownika.
            # parser(request.data)
            DataOperator(request.data).csv_dump()
        except ValueError:
            print("Decoding failed")
    print(request.data)
    print("data collected")
    return "test"


# * route publikujący czas - pozwala na zrezygnowanie z fizycznego RTC w ESP32
# * (czas jest potrzebny jako identyfikator próbek w ramkach danych z czujników)
@app.route("/get-datetime", methods=['GET'])
def date_time():
    # now = datetime.now()
    # date_list = [now.day, now.month, now.year]
    # time_list = [now.hour, now.minute, now.second]
    # date_time_dict = {"date": "{:02d}:{:02d}:{}".format(*date_list), "time": "{:02d}:{:02d}:{:02d}".format(*time_list)}

    # print(json.dumps(date_time_dict))
    # return json.dumps(date_time_dict)
    return(TimeOperator().send_datetime())


# * route publikujący set requestowanych danych
# TODO: określić sposób requestowania i forme przesyłania informacji do gui
@app.route("/data-publisher", methods=['POST, GET'])
def data_publisher():
    return "data"

# * route publikujący listę dostępnych w systemie czujników wraz z ich stanami
# TODO: określić kryterium stanu czujnika (aktywny/nieaktywny)
@app.route("/sensor-publisher", methods=['POST','GET'])
def sensor_publisher():
    return "sensor id list"




if __name__ == "__main__":
    # serve(app, host="0.0.0.0", threads=2)
    # host 0.0.0.0 po to, żeby odpaliło się w sieci lokalnej a nie tylko na localhoscie
    app.run(host="0.0.0.0")
