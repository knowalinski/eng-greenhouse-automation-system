from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
import json
import csv
import random
from datetime import datetime
from box_generator import BoxGenerator
from data_operator import DataOperator, TimeOperator
# from waitress import serve
# html = '    <div class = "sensor">\n<label for = "sensor_id">box from html</label>\n<br><label for = "">Air temperature:</label><br>\n<label for = "">Air humidity:</label><br>\n<label for = "">Soil temperature:</label><br>\n<label for = "">Soil humidity:</label><br>\n</div>'

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
input_dict = {}

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
            # TODO: dodać konwersje typu danych w generatorze wyjściowego słownika
            # TODO: dodać zapisywanie ostatniej wartości dla każdego czujnika do słownika.
            data = DataOperator(request.data)
            # data.csv_dump()
            input_dict[data.get_sensorid()] = [1, [*data.get_values()]]
            BoxGenerator(input_dict).html_dump()
            print (input_dict)
            print("data collected")
        except ValueError:
            print("Decoding failed")
    print(type(request.data))
    
    return "test"


# * route publikujący czas - pozwala na zrezygnowanie z fizycznego RTC w ESP32
# * (czas jest potrzebny jako identyfikator próbek w ramkach danych z czujników)
@app.route("/get-datetime", methods=['GET'])
def date_time():
    return(TimeOperator().send_datetime())


# * route publikujący set requestowanych danych
@app.route("/data-publisher", methods=['POST, GET'])
def data_publisher():
    return "data"

# * route publikujący listę dostępnych w systemie czujników wraz z ich stanami
# TODO: określić kryterium stanu czujnika (aktywny/nieaktywny)
# !!!
@app.route("/sensor-publisher", methods=['POST','GET'])
def sensor_publisher():
#     input_dict = {}
#     BoxGenerator(input_dict).html_dump()
#     # input_file = {1:[1,[2,3,4,5],[]], 2:[1,[2,3,4,5]], 3:[1,[2,3,4,5]], 4:[1,[2,3,4,5]], 5:[1,[2,3,4,5]], 6:[1,[2,3,4,5]], 7:[1,[2,3,4,5]]}
#     for i in range(1, random.randint(2,10)):
#         input_dict[i] = [random.randint(0,1),[2,3,4,5]]
#     print(input_dict)
    # ! dodać generowanie rzeczywistego output_dict
    # DataOperator.generate_output
    print(input_dict)
    # BoxGenerator(input_dict).html_dump()
    return render_template('index.html')




if __name__ == "__main__":
    # serve(app, host="0.0.0.0", threads=2)
    # host 0.0.0.0 po to, żeby odpaliło się w sieci lokalnej a nie tylko na localhoscie
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0")
