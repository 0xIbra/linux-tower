from api import db


class DiskMetric(db.Model):
    __tablename__ = 'disk_metric_data'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    created_at = db.Column(db.DateTime)

    def to_json(self):
        return {
            'id': self.id,
            'value': self.value,
            'created_at': self.created_at
        }
