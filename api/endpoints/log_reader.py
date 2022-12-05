from flask import request, jsonify
from helpers.log_viewer import LogViewer
from . import blueprint
from decorators import is_authenticated


@blueprint.route('/api/logs/tail', methods=['GET'])
@is_authenticated
def logs_reader_endpoint():
    read_lines = request.args.get('lines')
    if read_lines is None:
        read_lines = 25
    elif type(read_lines) is str:
        read_lines = int(read_lines)

    log_file = request.args.get('log_file')
    if log_file is None:
        return jsonify({'detail': '"log_file" query parameter is required.'}), 400

    try:
        viewer = LogViewer(log_file)
    except Exception as e:
        return jsonify({'detail': f'{e}'}), 400

    logs = viewer.tail(read_lines)

    return jsonify({
        'type': 'tail',
        'lines_requested': read_lines,
        'total_lines': len(logs),
        'logs': logs
    })

