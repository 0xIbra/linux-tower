from api import db


class Alerts(db.Model):
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String)
    webhook_method = db.Column(db.String)
    webhook_url = db.Column(db.String)
    logfile_path = db.Column(db.String)
    logfile_first_line_checksum = db.Column(db.String)
    logfile_last_read_checksum = db.Column(db.String)

    def to_json(self):
        return {
            'id': self.id,
            'alert_type': self.alert_type,
            'webhook_method': self.webhook_method,
            'webhook_url': self.webhook_url,
            'logfile_path': self.logfile_path,
            'logfile_first_line_checksum': self.logfile_first_line_checksum,
            'logfile_last_read_checksum': self.logfile_last_read_checksum
        }
