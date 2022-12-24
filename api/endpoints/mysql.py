from helpers.programs.mysql import MySQL
from . import blueprint
from flask import jsonify
from decorators import is_authenticated
from exceptions import ProcessNotFound


@blueprint.route('/api/mysql/status')
@is_authenticated
def mysql_status_endpoint():
    is_installed = MySQL.is_installed()
    if is_installed is not True:
        return jsonify({'detail': 'MySQL does not seem to be installed on this server.'}), 404

    payload = {
        'data': {
            'status': MySQL.status(),
            'details': MySQL.state_details()
        }
    }

    return jsonify(payload)


@blueprint.route('/api/mysql/metrics')
@is_authenticated
def mysql_metrics_endpoint():
    is_installed = MySQL.is_installed()
    if is_installed is not True:
        return jsonify({'detail': 'Apache does not seem to be installed on this server.'}), 404

    try:
        metrics = MySQL.metrics()
    except ProcessNotFound:
        return jsonify({'detail': 'MySQL is not running.'}), 400

    return jsonify(metrics)
