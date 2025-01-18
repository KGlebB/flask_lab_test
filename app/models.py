from . import db
from flask_login import UserMixin
from flask_security import RoleMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

roles_users = db.Table(
  'roles_users',
  db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
  db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(150), unique=True, nullable=False)
  password = db.Column(db.String(150), nullable=False)
  created_on = db.Column(db.DateTime(), default=datetime.utcnow)
  updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
  active = db.Column(db.Boolean(), default=True)
  roles = db.relationship('Role', secondary=roles_users, backref='user')

  def has_role(self, *args):
    return set(args).issubset({role.name for role in self.roles})

  def set_password(self, password):
    self.password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)

class Role(db.Model, RoleMixin):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))
  def __str__(self):
    return self.name

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

class FAQ(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  question = db.Column(db.String(500), nullable=False)
  answer = db.Column(db.String(500), nullable=False)
