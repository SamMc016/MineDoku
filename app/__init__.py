from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager

# Initialising the extensions without the app allows the create_app function to bind them to different app instances 
db = SQLAlchemy() 
migrate = Migrate()
login = LoginManager()
login.login_view = "main.login"

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class) # Creates the app given a config class

    # Binds the extensions to the app instance 
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.blueprints import main
    app.register_blueprint(main)

    return app
