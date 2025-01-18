from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_admin import Admin

db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap5()
admin = Admin(base_template='admin/master-extended.html')

def create_app():
  app = Flask(__name__)
  app.secret_key = 'SOME_SECRET_KEY'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  db.init_app(app)
  login_manager.init_app(app)
  bootstrap.init_app(app)

  from .models import User
  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))

  from .filters import register_filters
  register_filters(app)

  from .routes.user_routes import user_bp
  from .routes.dialogue_routes import dialogue_bp
  from .routes.main_routes import main_bp
  app.register_blueprint(user_bp)
  app.register_blueprint(dialogue_bp)
  app.register_blueprint(main_bp)

  admin.init_app(app)
  from .models import FAQ, Role, User
  from .views.admin_model_view import AdminModelView
  admin.add_view(AdminModelView(FAQ, db.session))
  # admin.add_view(AdminModelView(Role, db.session))
  # admin.add_view(AdminModelView(User, db.session, endpoint='admin_users', url='/admin/user'))

  from .error_handlers import register_error_handlers
  register_error_handlers(app)

  from .seed import init_roles_and_admin_user
  with app.app_context():
    init_roles_and_admin_user(db)

  return app
