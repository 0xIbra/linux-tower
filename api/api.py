from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
import secrets


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///linuxtower.db'
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    db.init_app(app)

    handler = logging.FileHandler('instance/api.log')
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.ERROR)

    with app.app_context():
        from endpoints import blueprint
        app.register_blueprint(blueprint)

        db.create_all()

        return app
