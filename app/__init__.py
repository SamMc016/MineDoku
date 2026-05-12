from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "login"

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.blueprints import main
    app.register_blueprint(main)

    return app

from app import routes, models