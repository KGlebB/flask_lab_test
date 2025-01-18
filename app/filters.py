from flask import current_app
from datetime import datetime

def register_filters(app):
  @app.template_filter('current_year')
  def current_year(value=None):
    return datetime.now().year
