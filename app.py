from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.secret_key = 'SECRET KEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(int(uid))

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/api/login')

    bcrypt = Bcrypt()

    from api_routes import register_routes
    register_routes(app, db, bcrypt)

    migrate = Migrate(app, db)

    return app
