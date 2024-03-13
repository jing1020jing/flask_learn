from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, ccit!</p>"



@app.route('/h/<h>')
def get_humidity(h):
    return f'humidity is {escape(h)}!'

@app.route('/t/<t>')
def get_humidity(t):
    return f'temperature is {escape(t)}!'

