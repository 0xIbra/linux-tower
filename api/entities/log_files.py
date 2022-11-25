from api import db


class LogFiles(db.Model):
    __tablename__ = 'log_files'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String)

    def to_json(self):
        return {
            'id': self.id,
            'path': self.path
        }
