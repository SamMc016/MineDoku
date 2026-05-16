from flask import Blueprint

main = Blueprint("main", __name__) # essentially acts like traffic coordinator. Main tells the routes where to go  

from app import models, routes