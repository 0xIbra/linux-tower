from flask import Flask
from endpoints import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint)
