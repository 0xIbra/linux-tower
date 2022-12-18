from endpoints import blueprint
from entities import Alerts
from flask import request, jsonify
from api import db
from decorators import is_authenticated
from json import dumps as json_encode


@blueprint.route('/api/alerts', methods=['GET'])
@is_authenticated
def get_alerts_endpoint():
    alerts = db.session.query(Alerts)
    return jsonify([a.to_json() for a in alerts])


@blueprint.route('/api/alerts/<id>', methods=['GET'])
@is_authenticated
def get_alert_by_id_endpoint(id):
    alert = db.session.get(Alerts, id)
    if alert is None:
        return jsonify({'detail': f'alert with ID "{id}" does not exist.'}), 404

    return jsonify(alert.to_json())


@blueprint.route('/api/alerts', methods=['POST'])
@is_authenticated
def create_alerts_endpoint():
    data = request.get_json()

    if 'alert_type' not in data:
        return jsonify({'detail': '"alert_type" attribute is required'}), 400

    alert_type = data['alert_type']
    if alert_type not in Alerts.SUPPORTED_ALERT_TYPES:
        return jsonify({'detail': f'"{alert_type}" alert type is not supported. Supported: {json_encode(Alerts.SUPPORTED_ALERT_TYPES)}'})

    if alert_type == Alerts.ALERT_TYPE_LOG:
        alert = db.session.execute(db.select(Alerts).filter_by(logfile_path=data['logfile_path'])).first()
    elif alert_type == Alerts.ALERT_TYPE_SERVICE:
        alert = db.session.execute(db.select(Alerts).filter_by(service_name=data['service_name'])).first()
    elif alert_type == Alerts.ALERT_TYPE_METRIC:
        alert = db.session.execute(db.select(Alerts).filter_by(metric_name=data['metric_name'])).first()
    else:
        return jsonify({'detail': f'unsupported "alert_type": "{alert_type}".'}), 400

    if alert is not None:
        return jsonify({'detail': 'alert already exists.'}), 400

    alert = Alerts(alert_type=data['alert_type'])

    if 'regex' in data:
        alert.regex = data['regex']
    if 'logfile_path' in data:
        alert.logfile_path = data['logfile_path']
    if 'service_name' in data:
        alert.service_name = data['service_name']
    if 'metric_name' in data:
        alert.metric_name = data['metric_name']
    if 'metric_rule' in data:
        alert.set_metric_rule(data['metric_rule'])
    if 'website_url' in data:
        alert.website_url = data['website_url']

    if 'cooldown_time' in data:
        alert.cooldown_time = data['cooldown_time']
    if 'webhook_method' in data:
        alert.webhook_method = data['webhook_method']
    if 'webhook_url' in data:
        alert.webhook_url = data['webhook_url']
    if 'slack_webhook_url' in data:
        alert.slack_webhook_url = data['slack_webhook_url']
    if 'discord_webhook_url' in data:
        alert.discord_webhook_url = data['discord_webhook_url']

    db.session.add(alert)
    db.session.commit()

    return jsonify({'detail': 'alert successfully created.'})


@blueprint.route('/api/alerts/<id>', methods=['PUT'])
@is_authenticated
def update_alert_endpoint(id):
    data = request.get_json()

    alert = db.session.get(Alerts, id)
    if alert is None:
        return jsonify({'detail': f'alert with ID "{id}" does not exist.'}), 404

    if 'alert_type' in data:
        alert.alert_type = data['alert_type']
    if 'regex' in data:
        alert.regex = data['regex']
    if 'logfile_path' in data:
        alert.logfile_path = data['logfile_path']

    if 'service_name' in data:
        alert.service_name = data['service_name']
    if 'metric_name' in data:
        alert.metric_name = data['metric_name']
    if 'metric_rule' in data:
        alert.set_metric_rule(data['metric_rule'])
    if 'website_url' in data:
        alert.website_url = data['website_url']
    if 'cooldown_time' in data:
        alert.cooldown_time = data['cooldown_time']

    if 'webhook_method' in data:
        alert.webhook_method = data['webhook_method']
    if 'webhook_url' in data:
        alert.webhook_url = data['webhook_url']
    if 'slack_webhook_url' in data:
        alert.slack_webhook_url = data['slack_webhook_url']
    if 'discord_webhook_url' in data:
        alert.discord_webhook_url = data['discord_webhook_url']

    db.session.commit()

    return jsonify({'detail': 'alert updated successfully.'})


@blueprint.route('/api/alerts/<id>', methods=['DELETE'])
@is_authenticated
def delete_alert_endpoint(id):
    alert = db.session.get(Alerts, id)
    if alert is None:
        return jsonify({'detail': f'alert with id "{id}" does not exist.'}), 404

    db.session.delete(alert)
    db.session.commit()

    return jsonify({'detail': 'alert deleted.'})
