from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
  app = Flask(__name__)
  app.secret_key = 'SOME_SECRET_KEY'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  db.init_app(app)
  login_manager.init_app(app)

  from .models import User
  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))

  from .filters import register_filters
  register_filters(app)

  from .routes.user_routes import user_bp
  from .routes.dialogue_routes import dialogue_bp
  app.register_blueprint(user_bp)
  app.register_blueprint(dialogue_bp)

  return app
