import os


def test_testing_config(testing_app):
    assert testing_app.config['SECRET_KEY'] is not None
    assert testing_app.config['SECRET_KEY'] != ''
    assert testing_app.config['SQLALCHEMY_DATABASE_URI'] is not None
