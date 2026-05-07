-- THIS FILE HAS BEEN KEPT AS REFERENCE FOR THE DATABASE
-- CONSTRUCTED IN SQLALCHEMY.

DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Blocks;
DROP TABLE IF EXISTS Conditions;
DROP TABLE IF EXISTS Game_Stats;
DROP TABLE IF EXISTS Friends;
DROP TABLE IF EXISTS Personal_Stats;
DROP TABLE IF EXISTS Current_Game;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS Gameboard;
DROP TABLE IF EXISTS Block_Stats;

CREATE TABLE User(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username CHAR(20),
    email TEXT,
    password TEXT -- possibly switch this to char depending on if we use hashes
);

CREATE TABLE Blocks(
    block_id INT NOT NULL, 
    block_name TEXT,
    condition_compatibility TEXT, -- stored as integers in a string as csv's. e.g. "1,2,5". 
    texture_path TEXT, -- stores a string that is the path to where the image of the texture is instead of the actual image

    PRIMARY KEY (block_id)
);

CREATE TABLE Conditions(
    condition_id INT NOT NULL,
    condition_name TEXT, 

    PRIMARY KEY (condition_id)
);

CREATE TABLE Game_Stats(
    game_id INT NOT NULL,
    global_games_played INT,
    lowest_uniqueness INT,
    average_uniqueness INT,

    PRIMARY KEY (game_id)
);

CREATE TABLE Friends(
    user_id INT NOT NULL, 
    friend_username TEXT NOT NULL,
    friend_daily_uniqueness TEXT,
    friend_all_time_uniqueness TEXT,

    PRIMARY KEY (user_id, friend_username),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Personal_Stats(
    user_id INT NOT NULL,
    total_games_played INT,
    total_games_won INT,
    average_uniqueness INT,
    lowest_uniqueness INT,

    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Current_Game(
    user_id INT NOT NULL,
    game_id INT NOT NULL,
    square_id INT, -- numbered 1-9 from left to right, top to bottom
    uniqueness INT,

    PRIMARY KEY (user_id, game_id)
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON UPDATE CASCADE ON DELETE CASCADE 
    -- ideally here on delete we set null, but because we cant set any part of the primary key to null, we aren't able to.
    -- basically this means if a user is deleted, we will lose their stats for the global stats.
);

CREATE TABLE Inventory(
    user_id INT NOT NULL,
    block_id INT NOT NULL, 

    PRIMARY KEY (user_id, block_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON UPDATE CASCADE ON DELETE CASCADE, 
    FOREIGN KEY (block_id) REFERENCES Blocks(block_id) ON UPDATE CASCADE ON DELETE CASCADE 
);

CREATE TABLE Gameboard(
    square_id INT NOT NULL,
    block_id INT NOT NULL,
    row_condition_id INT,
    column_condition_id INT,

    PRIMARY KEY (square_id, block_id),
    FOREIGN KEY (block_id) REFERENCES Blocks(block_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (row_condition_id) REFERENCES Conditions(condition_id) ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY (column_condition_id) REFERENCES Conditions(condition_id) ON UPDATE NO ACTION ON DELETE NO ACTION 
    -- no action on these two because this stops the condition from being deleted if the board is currently using it.
);

CREATE TABLE Block_Stats(
    square_id INT NOT NULL,
    block_id INT NOT NULL,
    times_chosen INT,

    PRIMARY KEY (square_id, block_id),
    FOREIGN KEY (block_id) REFERENCES Blocks(block_id) ON UPDATE CASCADE ON DELETE CASCADE
);