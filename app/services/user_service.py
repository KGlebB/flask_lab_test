from app import db
from app.models import User

class UserService:
  _instance = None

  def __new__(cls, *args, **kwargs):
    if not cls._instance:
      cls._instance = super(UserService, cls).__new__(cls)
    return cls._instance

  def create_user(self, username, password):
    if User.query.filter_by(username=username).first():
      return False
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return True

  def authenticate_user(self, username, password):
    return User.query.filter_by(username=username, password=password).first()
