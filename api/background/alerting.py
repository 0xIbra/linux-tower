from background.tasks import LogAlertTask, ServiceAlertTask, MetricAlertTask
from entities import Alerts
from api import db


def alerting_task(*args):
    app = args[0]
    with app.app_context():
        alerts = db.session.query(Alerts).all()
        for alert in alerts:
            if alert.alert_type == Alerts.ALERT_TYPE_LOG:
                log_alert_task = LogAlertTask(app, db, alert)
                log_alert_task.execute()
            elif alert.alert_type == Alerts.ALERT_TYPE_SERVICE:
                service_alert_task = ServiceAlertTask(app, db, alert)
                service_alert_task.execute()
            elif alert.alert_type == Alerts.ALERT_TYPE_METRIC:
                metric_alert_task = MetricAlertTask(app, db, alert)
                metric_alert_task.execute()
