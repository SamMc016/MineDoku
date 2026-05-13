import os 

basedir = os.path.dirname(os.path.dirname(__file__))
default_database_location = "sqlite:///" + os.path.join(basedir, "minedoku.db")

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "sixseven-temp-secret-key"

class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or default_database_location
    #SQLALCHEMY_DATABASE_URI = "sqlilte:///" + os.path.join(basedir, "test.db")

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory" 
    TESTING = True