from api import create_app, db
from entities import Alerts
import pytest


@pytest.fixture
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
