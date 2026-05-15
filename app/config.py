import os 
from dotenv import load_dotenv # allows secret key to be provided by a .env file

load_dotenv()

basedir = os.path.dirname(os.path.dirname(__file__)) 
default_database_location = "sqlite:///" + os.path.join(basedir, "minedoku.db") # This automatically places the database in the root directory  

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") 

class DeploymentConfig(Config): # Extends Config. this deployment version and is used for live application
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or default_database_location

class TestConfig(Config): # Extends Config. this is the testing version and is used for the unit and system tests. stored in the RAM of the device
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:" 
    TESTING = True