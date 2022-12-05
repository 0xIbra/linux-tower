from . import blueprint
from helpers.metrics.system import system_metrics
from flask import jsonify
from decorators import is_authenticated


@blueprint.route('/api/system_metrics', methods=['GET'])
@is_authenticated
def system_metrics_endpoint():
    return jsonify(system_metrics())
