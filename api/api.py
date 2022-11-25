from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///linuxtower.db'
    db.init_app(app)

    with app.app_context():
        from endpoints import blueprint
        app.register_blueprint(blueprint)

        db.create_all()

        return app
