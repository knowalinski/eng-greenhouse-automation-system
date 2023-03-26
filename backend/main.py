from flask import Flask, render_template, request, redirect, url_for, jsonify
from data_operator import DataOperator, TimeOperator, BoxGenerator, OutputGenerator, DataPlotter


app = Flask(__name__)
output_generator = OutputGenerator()

class DataStore:
    def __init__(self):
        self.a = None
        
    def update_a(self, variable):
        # print(variable)
        self.a = variable
    

memory = DataStore()



@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')
    


@app.route("/data-collector", methods=['POST'])
def collector():
    try:
        data = DataOperator(request.data)
        data.csv_dump()
        output_generator.update_records(data.sensor_id,
                                        data.values,
                                        data.timestamp)
        output_generator.update_states()
        generator = BoxGenerator(output_generator.return_output(),
                                output_generator.return_timestamps())
        generator.html_dump()
        # print("data collected")
        print(request.data)
    except ValueError:
        print("Decoding failed")

    return "data-collector"


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
    d = DataPlotter(memory.a).return_all_data()
    return render_template('plotting.html',
                           temperatureJSON = d[0],
                           humidityJSON = d[1],
                           moistureJSON = d[2])


@app.route("/get-data", methods = ['GET', 'POST'])
def get_data():
    return output_generator.return_output()

if __name__ == "__main__":
    # * host 0.0.0.0 po to, żeby odpaliło się w sieci lokalnej a nie tylko na localhoscie
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0")


