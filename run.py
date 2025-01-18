from app import create_app, db
from flask_migrate import Migrate, upgrade, migrate, init
import os

app = create_app()
Migrate(app, db)

if __name__ == '__main__':
  with app.app_context():
    if not os.path.exists('migrations'):
      init()
    migrate()
    upgrade()

  app.run(debug=True)
