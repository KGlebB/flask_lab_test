from flask import render_template

def register_error_handlers(app):
  @app.errorhandler(404)
  def page_not_found(e):
    return render_template('errors/404.html'), 404

  @app.errorhandler(403)
  def forbidden(e):
    return render_template('errors/403.html'), 403
