-- THIS FILE HAS BEEN KEPT AS REFERENCE FOR THE DATABASE
-- CONSTRUCTED IN SQLALCHEMY.

-- CURRENTLY ALL FAKE JUST TO FILL THE DATABASE FOR TESTING

DELETE FROM User;
DELETE FROM Blocks;
DELETE FROM Conditions;
DELETE FROM Game_Stats;
DELETE FROM Personal_Stats;
DELETE FROM Block_Stats;
DELETE FROM Current_Game;
DELETE FROM Inventory;
DELETE FROM Gameboard;
DELETE FROM Friends;




INSERT INTO User (username, email, password) 
VALUES ("samsTheBest", "sam@gmail.com", "SamMeowMeowmMeow"),
("bensTheBest", "ben@gmail.com", "BenMeowMeowmMeow"),
("hamsasTheBest", "hamsa@gmail.com", "HamsaMeowMeowmMeow"),
("natesTheBest", "nate@gmail.com", "NateMeowMeowmMeow");


INSERT INTO Blocks (block_id, block_name, condition_compatibility, texture_path) 
VALUES (1, "Grass", "1,5,7,10,12,13,15,17,18", "path/to/file/grass.png"),
(2, "Sand", "1,4,10,12,13,15", "path/to/file/sand.png"),
(3, "Gravel", "1,6,10,12,13,15", "path/to/file/gravel.png"),
(4, "Clay", "1,6,10,11,12,13,15,17", "path/to/file/clay.png");

INSERT INTO Conditions (condition_id, condition_name) 
VALUES (1, "Found In The Overworld"),
(10, "Found On The Surface"),
(15, "Can Be Mined By Hand"),
(17, "Requires Silk Touch To Obtain");

INSERT INTO Game_Stats (game_id, global_games_played, lowest_uniqueness, average_uniqueness) 
VALUES (1, 1000, 10, 200),
(2, 100, 8, 400),
(3, 10, 12, 600),
(4, 50, 99, 100);

INSERT INTO Personal_Stats (user_id, total_games_played, total_games_won, average_uniqueness, lowest_uniqueness) 
VALUES (1, 10, 8, 200, 30),
(2, 5, 5, 100, 20),
(3, 4, 1, 400, 50),
(4, 19, 19, 300, 10);

INSERT INTO Block_Stats (square_id, block_id, times_chosen) 
VALUES (1, 1, 100),
(2, 2, 50),
(3, 3, 200),
(4, 4, 500);

INSERT INTO Current_Game (user_id, game_id, square_id, uniqueness) 
VALUES (1, 1, 1, 150),
(2, 2, 2, 100),
(3, 3, 3, 300),
(4, 4, 4, 200);

INSERT INTO Inventory (user_id, block_id) 
VALUES (1, 1),
(2, 2),
(3, 3),
(4, 4);

INSERT INTO Gameboard (square_id, block_id, row_condition_id, column_condition_id) 
VALUES (1, 1, 1, 15),
(2, 2, 1, 15),
(3, 3, 1, 17),
(4, 4, 10, 17);

INSERT INTO Friends (user_id, friend_username, friend_daily_uniqueness, friend_all_time_uniqueness) 
VALUES (1, "natesTheBest", 200, 10),
(2, "hamsasTheBest", 300, 50),
(3, "bensTheBest", 100, 20),
(4, "samsTheBest", 150, 30);