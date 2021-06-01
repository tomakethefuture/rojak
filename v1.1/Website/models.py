from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

class Attendance(db.Model):
    num_log = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(20))
    name = db.Column(db.String(30))
    date = db.Column(db.String(10))
    time = db.Column(db.String(8))
    status = db.Column(db.String(3))

class Profiles(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(30))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(6))
    department = db.Column(db.String(20))
    birthdate = db.Column(db.String(12))

class User(db.Model, UserMixin):
    def get_id(self):
        return (self.username)
    username = db.Column(db.String(20), primary_key=True, unique=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(30))
    password = db.Column(db.String(1000))
