from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
# from waitress import serve

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    print(f"method: {request.method} | time: {time.ctime()} | data: {request.data} ")
    return "stary wstał"


if __name__ == "__main__":
    # serve(app, host="0.0.0.0", threads=2)
    app.run()