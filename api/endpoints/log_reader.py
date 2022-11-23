from flask import request
from helpers.log_viewer import LogViewer
from . import blueprint
import json


@blueprint.route('/api/logs/tail', methods=['GET'])
def logs_reader_endpoint():
    read_lines = request.args.get('lines')
    if read_lines is None:
        read_lines = 25
    elif type(read_lines) is str:
        read_lines = int(read_lines)

    log_file = request.args.get('log_file')
    if log_file is None:
        return json.dumps({'detail': '"log_file" query parameter is required.'}), 400, {'Content-Type': 'application/json'}

    try:
        viewer = LogViewer(log_file)
    except Exception as e:
        return json.dumps({'detail': f'{e}'}), 400, {'Content-Type': 'application/json'}

    logs = viewer.tail(read_lines)

    return json.dumps({
        'type': 'tail',
        'lines_requested': read_lines,
        'total_lines': len(logs),
        'logs': logs
    }), 200, {'Content-Type': 'application/json'}

