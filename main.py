from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
import json
import csv
#TODO: dodać routing i threading 

# from waitress import serve


def parser(some_json):
    d = json.loads(some_json)
    # d_keys = list(d.keys())
    # d_values = list(d.values())
    with open('test4.csv', 'a') as csvfile:
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


@app.route("/data_collector", methods=['POST'])
def collector():
    if request.method == "POST":
        try:
            # print(request.data)
            # print(json.loads(request.data.decode("utf-8")))
            # print(type(json.loads(request.data)))
            parser(request.data)
        except ValueError:
            print("Decoding failed")
    return "test"


if __name__ == "__main__":
    # serve(app, host="0.0.0.0", threads=2)
    # host 0.0.0.0 po to, żeby odpaliło się w sieci lokalnej a nie tylko na localhoscie
    app.run(host="0.0.0.0")
