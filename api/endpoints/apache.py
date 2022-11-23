from programs.apache import is_apache_installed, apache_status, apache_state_details
from . import blueprint
import json


@blueprint.route('/api/apache/status', methods=['GET'])
def apache_status_endpoint():
    is_installed = is_apache_installed()
    if is_installed is not True:
        return json.dumps({'detail': 'Apache does not seem to be installed on this server.'}), 404, {'Content-Type': 'application/json'}

    payload = {
        'data': {
            'status': apache_status(),
            'details': apache_state_details()
        }
    }

    return json.dumps(payload), 200, {'Content-Type': 'application/json'}
