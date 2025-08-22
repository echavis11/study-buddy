from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/<name>')
def hello_world(name):
    return "Hello, {escape(name)}!"