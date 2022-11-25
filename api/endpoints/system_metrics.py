from . import blueprint
from helpers.metrics.system import system_metrics
from flask import jsonify


@blueprint.route('/api/system_metrics', methods=['GET'])
def system_metrics_endpoint():
    return jsonify(system_metrics())
