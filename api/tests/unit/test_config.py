import os


def test_testing_config(testing_app):
    """
    GIVEN Flask application with test config
    WHEN initialized
    THEN check that the config has relevant variables defined
    """

    assert testing_app.config['SECRET_KEY'] is not None
    assert testing_app.config['SECRET_KEY'] != ''
    assert testing_app.config['SQLALCHEMY_DATABASE_URI'] is not None
