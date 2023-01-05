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


@blueprint.route('/api/logs/query', methods=['GET'])
@is_authenticated
def logs_query_endpoint():
    start_line = request.args.get('start_line')
    end_line = request.args.get('end_line')
    query_str = request.args.get('query')
    if query_str is None:
        return jsonify({'detail': '"query" search parameter is needed.'}), 400

    if start_line is not None:
        start_line = int(start_line)
    if end_line is not None:
        end_line = int(end_line)

    log_file = request.args.get('log_file')
    if log_file is None:
        return jsonify({'detail': '"log_file" query parameter is required.'}), 400

    try:
        viewer = LogViewer(log_file)
    except Exception as e:
        return jsonify({'detail': f'{e}'}), 400

    logs, from_line, to_line = viewer.read_regex(query_str, start_line, end_line)

    return jsonify({
        'type': 'query',
        'start_line': from_line,
        'end_line': to_line,
        'total_lines': len(logs),
        'logs': logs
    })
