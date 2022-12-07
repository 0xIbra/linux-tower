from api import db


class Alerts(db.Model):
    __tablename__ = 'alerts'

    ALERT_TYPE_LOG = 'log'
    ALERT_TYPE_SERVICE = 'service'
    ALERT_TYPE_METRIC = 'metric'
    SUPPORTED_ALERT_TYPES = [ALERT_TYPE_LOG, ALERT_TYPE_SERVICE, ALERT_TYPE_METRIC]

    CPU_METRIC = 'cpu'
    MEMORY_PERCENT_METRIC = 'memory_percent'
    DISK_PERCENT_METRIC = 'disk_percent'
    SUPPORTED_METRICS = [CPU_METRIC, MEMORY_PERCENT_METRIC, DISK_PERCENT_METRIC]

    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String)

    # for log type alert
    regex = db.Column(db.String)
    logfile_path = db.Column(db.String)
    logfile_first_line_checksum = db.Column(db.String)
    logfile_last_read_line_number = db.Column(db.Integer)

    # for service type alert
    service_name = db.Column(db.String)

    # for metric type alert
    metric_name = db.Column(db.String)

    last_triggered_at = db.Column(db.DateTime)
    cooldown_time = db.Column(db.Integer)

    webhook_method = db.Column(db.String)
    webhook_url = db.Column(db.String)
    slack_webhook_url = db.Column(db.String)
    discord_webhook_url = db.Column(db.String)

    def to_json(self):
        return {
            'id': self.id,
            'alert_type': self.alert_type,
            'regex': self.regex,
            'logfile_path': self.logfile_path,
            'logfile_first_line_checksum': self.logfile_first_line_checksum,
            'logfile_last_read_line_number': self.logfile_last_read_line_number,
            'service_name': self.service_name,
            'metric_name': self.metric_name,
            'last_triggered_at': self.last_triggered_at,
            'cooldown_time': self.cooldown_time,
            'webhook_method': self.webhook_method,
            'webhook_url': self.webhook_url,
            'slack_webhook_url': self.slack_webhook_url,
            'discord_webhook_url': self.discord_webhook_url
        }
