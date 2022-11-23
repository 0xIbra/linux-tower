from . import blueprint
from metrics.system import system_metrics
import json


@blueprint.route('/api/system_metrics', methods=['GET'])
def system_metrics_endpoint():
    return json.dumps(system_metrics()), 200, {'Content-Type': 'application/json'}
