from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
import json
import csv
import random
from datetime import datetime
from data_operator import DataOperator, TimeOperator, BoxGenerator, OutputGenerator, DataReturner

app = Flask(__name__)
output_generator = OutputGenerator()

class DataStore:
    def __init__(self):
        self.a = None
        
    def update_a(self, variable):
        print(variable)
        self.a = variable

memory = DataStore()




# ! route testowy - później zostanie usunięty
@app.route("/", methods=['GET', 'POST'])
def index():
    
    return render_template('index.html')
    

# * route dodbierający ramki danych z esp32
@app.route("/data-collector", methods=['POST'])
def collector():
    if request.method == "POST":
        try:
            
            data = DataOperator(request.data)
            data.csv_dump()

            output_generator.update_records(data.sensor_id, data.values, data.timestamp)
            output_generator.update_states()
            generator = BoxGenerator(output_generator.return_output())
            generator.html_dump()

            print(output_generator.latest_records)
            print("data collected")
        except ValueError:
            print("Decoding failed")
    print(type(request.data))

    return "data-collector"


# * route publikujący czas - pozwala na zrezygnowanie z fizycznego RTC w ESP32
# * (czas jest potrzebny jako identyfikator próbek w ramkach danych z czujników)
@app.route("/get-datetime", methods=['GET'])
def date_time():
    return(TimeOperator().send_datetime())

@app.route("/redirecting", methods = ['GET', 'POST'])
def redirecting_hub():
    data = request.form.get("button")
    if data == "go_back":
        return redirect("/", code=302)
    else:
        memory.update_a(data)
        return redirect("/plotting", code=302)

@app.route("/plotting", methods = ['GET', 'POST'])
def plotter():
    d = DataReturner(memory.a).return_data()
    return render_template('plotting.html',  temperatureJSON=d[0], humidityJSON = d[1])


if __name__ == "__main__":
    # * host 0.0.0.0 po to, żeby odpaliło się w sieci lokalnej a nie tylko na localhoscie
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0")


