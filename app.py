from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.secret_key = 'SECRET KEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'

    db.init_app(app)

    bcrypt = Bcrypt()

    from api_routes import register_routes

    register_routes(app, db, bcrypt)

    migrate = Migrate(app, db)

    return app
