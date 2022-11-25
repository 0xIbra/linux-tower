from flask import request, jsonify
from . import blueprint
from helpers.metrics.processes import processes_info


@blueprint.route('/api/processes', methods=['GET'])
def system_processes_endpoint():
    with_cpu_usage = False
    query_arg = request.args.get('cpu_usage')
    if query_arg == 'true' or query_arg == '1':
        with_cpu_usage = True

    return jsonify(processes_info(with_cpu_usage))
