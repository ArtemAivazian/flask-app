from flask_login import UserMixin

from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    measurements = db.relationship('Measurements', backref='user', lazy=True)

    def __repr__(self):
        return f'<User: {self.email}>'

    def get_id(self):
        return str(self.uid)

    def get_email(self):
        return self.email


class Measurements(db.Model):
    __tablename__ = 'data'

    measurement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    temp = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
