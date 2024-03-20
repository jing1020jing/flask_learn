from flask import Flask
from markupsafe import escape


app = Flask(__name__)

# 輸出網頁內容_html
@app.route("/")
def hello_XX():
    return "<p>Hello, willson!</p>"

db=[]

# HTML Escaping
# @app.route("/<name>")
# def hello(name):
#     return f"Hello, {escape(name)}!"

@app.route('/h/<h>')
def get_humidity(h):
    return f'humidity : {escape(h)}!'

@app.route('/t/<t>')
def get_temperature(t):
    return f'temperature : {escape(t)}!'

@app.route("/th")
def get_temperature_humidity():
    global db
    args = request.args
    db += [[args.get("t"), args.get("h")]]
    return db


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'
# Routing
# @app.route('/')
# def index():
#     return 'Index Page'

# @app.route('/hello')
# def hello():
#     return 'Hello, World'