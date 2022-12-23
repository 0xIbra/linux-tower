from flask import request, jsonify
from helpers.log_viewer import LogViewer
from . import blueprint
from decorators import is_authenticated


@blueprint.route('/api/logs/tail', methods=['GET'])
@is_authenticated
def logs_reader_endpoint():
    read_lines = request.args.get('lines')
    from_line = request.args.get('start_line')
    to_line = request.args.get('end_line')

    if read_lines is None:
        read_lines = 50
    elif type(read_lines) is str:
        read_lines = int(read_lines)

    if from_line is not None:
        from_line = int(from_line)
    if to_line is not None:
        to_line = int(to_line)

    log_file = request.args.get('log_file')
    if log_file is None:
        return jsonify({'detail': '"log_file" query parameter is required.'}), 400

    try:
        viewer = LogViewer(log_file)
    except Exception as e:
        return jsonify({'detail': f'{e}'}), 400

    logs, from_line, to_line = viewer.read(from_line=from_line, to_line=to_line, lines=read_lines)

    return jsonify({
        'type': 'tail',
        'start_line': from_line,
        'end_line': to_line,
        'total_lines': len(logs),
        'logs': logs
    })

