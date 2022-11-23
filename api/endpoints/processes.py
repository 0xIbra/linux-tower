from flask import request
from . import blueprint
from metrics.processes import processes_info
import json


@blueprint.route('/api/processes', methods=['GET'])
def system_processes_endpoint():
    with_cpu_usage = False
    query_arg = request.args.get('cpu_usage')
    if query_arg == 'true' or query_arg == '1':
        with_cpu_usage = True

    return json.dumps(processes_info(with_cpu_usage)), 200, {'Content-Type': 'application/json'}
