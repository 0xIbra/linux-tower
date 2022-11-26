from endpoints import blueprint
from entities import LogFiles
from flask import request, jsonify
from api import db


@blueprint.route('/api/log_files', methods=['GET'])
def get_log_files_endpoint():
    logfiles = db.session.query(LogFiles)
    return jsonify([file.to_json() for file in logfiles])


@blueprint.route('/api/log_files/<id>', methods=['GET'])
def get_log_file_endpoint(id):
    logfile = db.session.get(LogFiles, id)
    if logfile is None:
        return jsonify({'detail': f'log file with ID "{id}" does not exist.'}), 404

    return jsonify(logfile.to_json())


@blueprint.route('/api/log_files', methods=['POST'])
def create_log_files_endpoint():
    data = request.get_json()

    logfile = db.session.execute(db.select(LogFiles).filter_by(path=data['path'])).first()
    if logfile is not None:
        return jsonify({'detail': 'log file already exists.'}), 400

    logfile = LogFiles(path=data['path'])
    db.session.add(logfile)
    db.session.commit()

    return jsonify({'detail': 'log file successfully created.'}), 200


@blueprint.route('/api/log_files/<id>', methods=['DELETE'])
def delete_log_file_endpoint(id):
    logfile = db.session.execute(db.select(LogFiles).filter_by(id=id)).first()
    if logfile is None:
        return jsonify({'detail': f'log file with id "{id}" does not exist.'}), 404

    logfile = logfile[0]

    db.session.delete(logfile)
    db.session.commit()

    return jsonify({'detail': 'log file deleted.'})
