import os 

basedir = os.path.dirname(os.path.dirname(__file__))
default_database_location = "sqlite:///" + os.path.join(basedir, "minedoku.db")

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or default_database_location
    SECRET_KEY = "meowmeowmeow"