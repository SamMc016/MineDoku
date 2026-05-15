from app import db, login
from flask_login import UserMixin
import datetime

# Association table for friends. Association tables represention relationships rather than entities.
friends_table = db.Table('friends_table',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
)

class User(UserMixin, db.Model): # UserMixin allows flask-login to track things such as is_authenticated, etc... 
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) # Stored as a salted hash in the database for security

    friends = db.relationship( # Joins the User and friends table to allow for the association table to exist
        'User',
        secondary='friends_table',
        primaryjoin=(user_id == friends_table.c.user_id),
        secondaryjoin=(user_id == friends_table.c.friend_id),
        backref='friend_of'
    )

    def get_id(self): # Necessary for UserMixin to work
        return str(self.user_id)

@login.user_loader # Is essentially the memory of UserMixin
def load_user(user_id):
    return User.query.get(int(user_id))

class Blocks(db.Model):
    block_id = db.Column(db.Integer, primary_key=True)
    block_name = db.Column(db.String(100), nullable=False)
    condition_compatibility = db.Column(db.String(100), nullable=False) # Stored as integers in a comma seperated list in a string
    face_texture_path = db.Column(db.String(200), nullable=False) 
    inv_texture_path = db.Column(db.String(200), nullable=False) 

class Conditions(db.Model):
    condition_id = db.Column(db.Integer, primary_key=True) 
    condition_name = db.Column(db.String(100), nullable=False)

class Game_Stats(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    global_games_played = db.Column(db.Integer, nullable=False)
    lowest_uniqueness = db.Column(db.Integer)
    average_uniqueness = db.Column(db.Integer)
    last_reset_date = db.Column(db.String(10), default="2000-01-01")

class Personal_Stats(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True)
    total_games_played = db.Column(db.Integer, nullable=False)
    total_games_won = db.Column(db.Integer, nullable=False)
    lowest_uniqueness = db.Column(db.Integer)
    average_uniqueness = db.Column(db.Integer)
    daily_uniqueness = db.Column(db.Integer)

class Current_Game(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True) 
    board_state = db.Column(db.Text, nullable=False, default="{}")
    puzzle_date = db.Column(db.String(10), nullable=False, default="2000-01-01")
    current_durability = db.Column(db.Integer, default=9)
    current_us = db.Column(db.Integer, default=900)

    def is_expired(self): # Returns true if the date of the puzzle is not the current date
        return self.puzzle_date != datetime.now().strftime("%Y-%m-%d")

class Inventory(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True) 
    block_id = db.Column(db.Integer, db.ForeignKey("blocks.block_id"), primary_key=True) 

class Block_Stats(db.Model):
    square_id = db.Column(db.Integer, primary_key=True)
    block_id = db.Column(db.Integer, db.ForeignKey("blocks.block_id"), primary_key=True) 
    times_chosen = db.Column(db.Integer, nullable=False)
