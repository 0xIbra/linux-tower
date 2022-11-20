from flask import Flask
from metrics import system_metrics, processes_info
import json


app = Flask(__name__)


@app.route('/api')
def hello_world():
    return json.dumps({'code': 200, 'message': 'Hello World !', 'author': 'Ibragim Abubakarov'}), 200, {'Content-Type': 'application/json'}


@app.route('/api/system_metrics')
def system_metrics_endpoint():
    return json.dumps(system_metrics()), 200, {'Content-Type': 'application/json'}


@app.route('/api/processes')
def system_processes():
    return json.dumps(processes_info()), 200, {'Content-Type': 'application/json'}
