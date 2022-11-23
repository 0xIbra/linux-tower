from programs.nginx import is_nginx_installed, nginx_status, nginx_state_details
from . import blueprint
import json


@blueprint.route('/api/nginx/status', methods=['GET'])
def nginx_status_endpoint():
    is_installed = is_nginx_installed()
    if is_installed is not True:
        return json.dumps({'detail': 'Nginx does not seem to be installed on this server.'}), 404, {'Content-Type': 'application/json'}

    payload = {
        'data': {
            'status': nginx_status(),
            'details': nginx_state_details()
        }
    }

    return json.dumps(payload), 200, {'Content-Type': 'application/json'}
