from flask import redirect, request, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class AdminModelView(ModelView):
  def is_accessible(self):
    return (current_user.is_authenticated and any(role.name == 'Admin' for role in current_user.roles))

  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('admin.index', next=request.url))
