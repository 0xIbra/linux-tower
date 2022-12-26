from api import create_app, db
from entities import Alerts, CpuMetric, MemoryMetric, DiskMetric
from datetime import datetime, timedelta
import pytest
import jwt


@pytest.fixture(scope='module')
def testing_app():
    """fixture for testing the api"""

    app = create_app()
    with app.app_context():
        yield app # tests happen here


@pytest.fixture(scope='module')
def test_database():
    """fixture for testing the db"""

    db.create_all()
    yield db

    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='module')
def add_alert():
    """fixture to create alerts"""

    def _add_alert(**args):
        alert = Alerts(**args)
        db.session.add(alert)
        db.session.commit()

        return alert

    return _add_alert


@pytest.fixture(scope='module')
def add_metric_data():
    """fixture to create metrics (CpuMetric, MemoryMetric, DiskMetric)"""

    def _add_metric_data(metric_type: str, **args):
        if metric_type == 'cpu':
            metric = CpuMetric(**args)
        elif metric_type == 'memory':
            metric = MemoryMetric(**args)
        else:
            metric = DiskMetric(**args)

        db.session.add(metric)
        db.session.commit()

        return metric

    return _add_metric_data

@pytest.fixture(scope='module')
def access_token(testing_app):
    now = datetime.utcnow()
    exp = now + timedelta(minutes=20)
    payload = {
        'username': 'tester',
        'iat': now,
        'exp': exp
    }
    access_token = jwt.encode(payload, testing_app.config['SECRET_KEY'], 'HS256')

    return access_token
