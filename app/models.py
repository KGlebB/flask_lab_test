from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(150), unique=True, nullable=False)
  password = db.Column(db.String(150), nullable=False)

class Dialogue(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  title = db.Column(db.String(150), nullable=False)
  messages = db.relationship('Message', backref='dialogue', lazy=True)

class Message(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  dialogue_id = db.Column(db.Integer, db.ForeignKey('dialogue.id'), nullable=False)
  content = db.Column(db.String(500), nullable=False)
  response = db.Column(db.String(500), nullable=False)
  timestamp = db.Column(db.DateTime, default=datetime.utcnow)
