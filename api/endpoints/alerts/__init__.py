from endpoints import blueprint
from entities import Alerts
from flask import request, jsonify
from api import db


@blueprint.route('/api/alerts', methods=['GET'])
def get_alerts_endpoint():
    alerts = db.session.query(Alerts)
    return jsonify([a.to_json() for a in alerts])


@blueprint.route('/api/alerts/<id>', methods=['GET'])
def get_alert_by_id_endpoint(id):
    alert = db.session.get(Alerts, id)
    if alert is None:
        return jsonify({'detail': f'alert with ID "{id}" does not exist.'}), 404

    return jsonify(alert.to_json())


@blueprint.route('/api/alerts', methods=['POST'])
def create_alerts_endpoint():
    data = request.get_json()

    alert = db.session.execute(db.select(Alerts).filter_by(logfile_path=data['logfile_path'])).first()
    if alert is not None:
        return jsonify({'detail': 'alert already exists.'}), 400

    alert = Alerts(
        alert_type='logfile',
        webhook_method=data['webhook_method'],
        webhook_url=data['webhook_url'],
        logfile_path=data['logfile_path']
    )
    db.session.add(alert)
    db.session.commit()

    return jsonify({'detail': 'alert successfully created.'})


@blueprint.route('/api/alerts/<id>', methods=['PUT'])
def update_alert_endpoint(id):
    data = request.get_json()

    alert = db.session.get(Alerts, id)
    if alert is None:
        return jsonify({'detail': f'alert with ID "{id}" does not exist.'}), 404

    if 'webhook_method' in data:
        alert.webhook_method = data['webhook_method']
    if 'webhook_url' in data:
        alert.webhook_url = data['webhook_url']
    if 'logfile_path' in data:
        alert.logfile_path = data['logfile_path']

    db.session.commit()

    return jsonify({'detail': 'alert updated successfully.'})


@blueprint.route('/api/alerts/<id>', methods=['DELETE'])
def delete_alert_endpoint(id):
    alert = db.session.get(Alerts, id)
    if alert is None:
        return jsonify({'detail': f'alert with id "{id}" does not exist.'}), 404

    db.session.delete(alert)
    db.session.commit()

    return jsonify({'detail': 'alert deleted.'})
