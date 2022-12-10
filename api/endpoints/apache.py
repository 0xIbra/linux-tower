from helpers.programs.apache import Apache
from . import blueprint
from flask import jsonify
from decorators import is_authenticated


@blueprint.route('/api/apache/status', methods=['GET'])
@is_authenticated
def apache_status_endpoint():
    is_installed = Apache.is_installed()
    if is_installed is not True:
        return jsonify({'detail': 'Apache does not seem to be installed on this server.'}), 404

    payload = {
        'data': {
            'status': Apache.status(),
            'details': Apache.state_details()
        }
    }

    return jsonify(payload), 200
