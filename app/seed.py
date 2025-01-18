from app.models import Role, User


def init_roles_and_admin_user(db):
  if Role.query.count() == 0:
    admin_role = Role(name='Admin')
    user_role = Role(name='User')
    db.session.add(admin_role)
    db.session.add(user_role)
    db.session.commit()

  if User.query.filter_by(username='Admin').first() is None:
    admin_user = User(username='Admin')
    admin_user.set_password('admin')
    admin_role = Role.query.filter_by(name='Admin').first()
    admin_user.roles.append(admin_role)
    db.session.add(admin_user)
    db.session.commit()
