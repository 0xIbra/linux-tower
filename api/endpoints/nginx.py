from helpers.programs.nginx import Nginx
from . import blueprint
from flask import jsonify
from decorators import is_authenticated


@blueprint.route('/api/nginx/status', methods=['GET'])
@is_authenticated
def nginx_status_endpoint():
    is_installed = Nginx.is_installed()
    if is_installed is not True:
        return jsonify({'detail': 'Nginx does not seem to be installed on this server.'}), 404

    payload = {
        'data': {
            'status': Nginx.status(),
            'details': Nginx.state_details()
        }
    }

    return jsonify(payload)
