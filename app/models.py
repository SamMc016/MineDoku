from app import db, login
from flask_login import UserMixin

# Association table for friends
friends_table = db.Table('friends_table',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
)

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    lowest_us = db.Column(db.Integer, default=9999)
    average_us = db.Column(db.Float, default=0)

    friends = db.relationship(
        'User',
        secondary='friends_table',
        primaryjoin=(user_id == friends_table.c.user_id),
        secondaryjoin=(user_id == friends_table.c.friend_id),
        backref='friend_of',
        lazy='dynamic'
    )

    def get_id(self):
        return str(self.user_id)

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Blocks(db.Model):
    block_id = db.Column(db.Integer, primary_key=True)
    block_name = db.Column(db.String(100), nullable=False)
    condition_compatibility = db.Column(db.String(100), nullable=False) # integers in a csl in a strong. e.g. "1,2,5"
    face_texture_path = db.Column(db.String(200), nullable=False) # stores a string with the path to the image file
    inv_texture_path = db.Column(db.String(200), nullable=False) # stores a string with the path to the image file

class Conditions(db.Model):
    condition_id = db.Column(db.Integer, primary_key=True) 
    condition_name = db.Column(db.String(100), nullable=False)

class Game_Stats(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    global_games_played = db.Column(db.Integer, nullable=False)
    lowest_uniqueness = db.Column(db.Integer)
    average_uniqueness = db.Column(db.Integer)
    last_reset_date = db.Column(db.String(10), default="2000-01-01")

class Friends(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True)
    friend_username = db.Column(db.String(20),  db.ForeignKey("user.username"), primary_key=True)
    friend_daily_uniqueness = db.Column(db.Integer)
    friend_all_time_uniqueness = db.Column(db.Integer)

class Personal_Stats(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True)
    total_games_played = db.Column(db.Integer, nullable=False)
    total_games_won = db.Column(db.Integer, nullable=False)
    lowest_uniqueness = db.Column(db.Integer)
    average_uniqueness = db.Column(db.Integer)
    daily_uniqueness = db.Column(db.Integer)

class Current_Game(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True) 
    game_id = db.Column(db.Integer, db.ForeignKey("game__stats.game_id"), primary_key=True)
    square_id = db.Column(db.Integer, nullable=False)
    uniqueness = db.Column(db.Integer, nullable=False)

class Inventory(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True) 
    block_id = db.Column(db.Integer, db.ForeignKey("blocks.block_id"), primary_key=True) 

class Gameboard(db.Model):
    square_id = db.Column(db.Integer, primary_key=True)
    block_id = db.Column(db.Integer, db.ForeignKey("blocks.block_id"), primary_key=True) 
    row_condition_id = db.Column(db.Integer, db.ForeignKey("conditions.condition_id"), nullable=False)
    column_condition_id = db.Column(db.Integer, db.ForeignKey("conditions.condition_id"), nullable=False) 

class Block_Stats(db.Model):
    square_id = db.Column(db.Integer, primary_key=True)
    block_id = db.Column(db.Integer, db.ForeignKey("blocks.block_id"), primary_key=True) 
    times_chosen = db.Column(db.Integer, nullable=False)
