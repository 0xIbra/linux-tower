from api import db


class Alerts(db.Model):
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String)
    regex = db.Column(db.String)
    logfile_path = db.Column(db.String)
    logfile_first_line_checksum = db.Column(db.String)
    logfile_last_read_line_number = db.Column(db.Integer)
    last_triggered_at = db.Column(db.DateTime)
    cooldown_time = db.Column(db.Integer)
    webhook_method = db.Column(db.String)
    webhook_url = db.Column(db.String)
    slack_webhook_url = db.Column(db.String)

    def to_json(self):
        return {
            'id': self.id,
            'alert_type': self.alert_type,
            'regex': self.regex,
            'logfile_path': self.logfile_path,
            'logfile_first_line_checksum': self.logfile_first_line_checksum,
            'logfile_last_read_line_number': self.logfile_last_read_line_number,
            'last_triggered_at': self.last_triggered_at,
            'cooldown_time': self.cooldown_time,
            'webhook_method': self.webhook_method,
            'webhook_url': self.webhook_url,
            'slack_webhook_url': self.slack_webhook_url
        }

    @staticmethod
    def format_slack_message(text):
        return {'type': 'mrkdwn', 'text': text}
