from flask import Flask

app = Flask(__name__)


# prompt: flask --app main run
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
