from endpoints import blueprint
from entities import LogFiles
from flask import jsonify
from api import db


@blueprint.route('/api/log_files', methods=['GET'])
def get_log_files_endpoint():
    logfiles = db.session.query(LogFiles)
    return jsonify([file.to_json() for file in logfiles])
