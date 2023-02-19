from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
import json
import csv
import random
from datetime import datetime
from data_operator import DataOperator, TimeOperator, BoxGenerator, OutputGenerator, DataPlotter


app = Flask(__name__)
output_generator = OutputGenerator()

class DataStore:
    def __init__(self):
        self.a = None
        self.b = None
        
    def update_a(self, variable):
        print(variable)
        self.a = variable
    
    def update_b(self, variable):
        self.b = variable

memory = DataStore()




# ! route testowy - później zostanie usunięty
@app.route("/", methods=['GET', 'POST'])
def index():
    
    return render_template('index.html')
    

# * route odbierający ramki danych z esp32
@app.route("/data-collector", methods=['POST'])
def collector():
    if request.method == "POST":
        try:
            print(request.data)
            data = DataOperator(request.data)
            data.csv_dump()

            output_generator.update_records(data.sensor_id, data.values, data.timestamp)
            output_generator.update_states()
            generator = BoxGenerator(output_generator.return_output(), output_generator.return_timestamps())
            generator.html_dump()

            print(output_generator.latest_records)
            print("data collected")
            memory.update_b(1)
        
        except ValueError:
            memory.update_b(2)
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

# TODO: podzielić na plotting dla ostatnich x próbek i do wszystkich próbek
@app.route("/plotting", methods = ['GET', 'POST'])
def plotter():
    d = DataPlotter(memory.a).return_all_data()
    return render_template('plotting.html',  temperatureJSON=d[0], humidityJSON = d[1], moistureJSON = d[2])

@app.route("/feedback", methods = ['GET'])
def feedback():
    feedback_dict = {"state":memory.b}
    memory.update_b
    return json.dumps(feedback_dict)

if __name__ == "__main__":
    # * host 0.0.0.0 po to, żeby odpaliło się w sieci lokalnej a nie tylko na localhoscie
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0")


