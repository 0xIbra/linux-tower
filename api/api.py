from flask import Flask, request
from metrics import system_metrics, processes_info
from programs.apache import is_apache_installed, apache_status, apache_service_show
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
    with_cpu_usage = False
    query_arg = request.args.get('cpu_usage')
    if query_arg == 'true' or query_arg == '1':
        with_cpu_usage = True

    return json.dumps(processes_info(with_cpu_usage)), 200, {'Content-Type': 'application/json'}


@app.route('/api/apache/status')
def apache_status_endpoint():
    is_installed = is_apache_installed()
    if is_installed is not True:
        return json.dumps({'detail': 'Apache does not seem to be installed on this server.'}), 404, {'Content-Type': 'application/json'}

    payload = {
        'data': {
            'status': apache_status(),
            'details': apache_service_show()
        }
    }

    return json.dumps(payload), 200, {'Content-Type': 'application/json'}
