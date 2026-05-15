import unittest
from app import create_app, db
from app.config import TestConfig
from app.models import Blocks, User
from app.db_population import *


class BasicTests(unittest.TestCase):

    def setUp(self): # Setup method creates necessary baseline environment for testing
        self.test_app = create_app(TestConfig)
        self.client = self.test_app.test_client()

        self.app_context = self.test_app.app_context()
        self.app_context.push()

        db.create_all()

        populate_blocks()
        populate_conditions()
        populate_users()
        populate_user_stats()

    def tearDown(self): # Removes testing enviornment so that it is able to be safely set up next time
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    """ UNIT TEST #1: TESTS THAT BLOCKS HAS CORRECT CONDITIONS """
    def test_block_conditions(self):
        grass = Blocks.query.filter_by(block_name="Grass").first() 
        condition_ids = grass.condition_compatibility.split(",")

        self.assertIsNotNone(grass, "Block should exist from database population") 
        self.assertIn( 
            "1",
            condition_ids,
            "Grass should have condition ID 1 (Overworld Block)"
        )
        self.assertNotIn( 
            "2",
            condition_ids,
            "Grass should not have condition ID 2 (Otherworld Block)"
        )


    """ UNIT TEST #2: TESTS IF A USER CAN BE CREATED """
    def test_create_user(self):
        user = User( # Creates user 
            username="testuser",
            email="test@test.com",
            password_hash="hashedpassword"
        )
        db.session.add(user)
        db.session.commit()

        saved_user = User.query.filter_by(username="testuser").first()

        self.assertIsNotNone(saved_user, "User should have been saved in the database") 
        self.assertEqual(saved_user.email, "test@test.com", "User's email should have been saved correctly") 


    """ UNIT TEST #3: TESTS THAT A USER CAN ADD A FRIEND """
    def test_add_friend_relationship(self):
        user1 = User( # Creates two users
            username="alan",
            email="alan@test.com",
            password_hash="hashpassword1"
        )

        user2 = User(
            username="beth",
            email="beth@test.com",
            password_hash="hashpassword2"
        )

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        user1.friends.append(user2) # User one adds user two as a friend
        db.session.commit()

        self.assertEqual(len(user1.friends), 1, "User1 should have 1 friend") # Checks if user one has one friend
        self.assertEqual(user1.friends[0].username, "beth", "User1's friend should be named beth") # checks if that friend's name is beth


    """ UNIT TEST #4: TESTS THAT A USER CAN ADD A FRIEND CREATED BEFORE THEM """
    def test_add_older_friend_relationship(self):
        older_user = User.query.filter_by(user_id=1).first() # Gets existing user from database 
        self.assertIsNotNone(older_user, "User should exist from database setup")

        new_user = User( # Creates a new user
            username="callum",
            email="callum@test.com",
            password_hash="hashpassword3"
        )

        db.session.add(new_user)
        db.session.commit()

        new_user.friends.append(older_user) # The newer user adds the older user as a friend
        db.session.commit()

        self.assertEqual(len(new_user.friends), 1, "New_user should have 1 friend") # Checks if user one has one friend
        self.assertEqual(new_user.friends[0].username, older_user.username, "New_user's friend should be named beth") # checks if that friend's name is the older user's


    """ UNIT TEST #5: TESTS IF A USER HAS STATS """
    def test_user_has_stats(self):
        user = User.query.filter_by(user_id=2).first() # Gets existing user from database and checks they exist
        self.assertIsNotNone(user, "User should exist from database setup")

        user_stats = Personal_Stats.query.filter_by(user_id=user.user_id).first() # Gets existing user stats from database and checks they exist
        self.assertIsNotNone(user_stats, "User_stats should exist from database setup")

        self.assertEqual(user_stats.total_games_played, 2, "User should have played two games") 


    """ UNIT TEST #6: TESTS IF LOGIN PAGE LOADS """
    def test_login_page_loads(self):
        response = self.client.get("/login") 

        self.assertEqual(response.status_code, 200, "Should recieve status code 200 signifying a loaded web page")
        self.assertIn(b"Login", response.data, "Login should be in the login page")


    """ UNIT TEST #7: TESTS IF SIGNUP PAGE LOADS """
    def test_signup_page_loads(self):
        response = self.client.get("/signup")

        self.assertEqual(response.status_code, 200, "Should recieve status code 200 signifying a loaded web page")
        self.assertIn(b"Sign Up", response.data, "Signup should be in the signup page")


    """ UNIT TEST #8: TESTS A PAGE THAT REQUIRE LOGINS  """
    def test_account_requires_login(self):
        response = self.client.get("/account", follow_redirects=False)

        self.assertEqual(response.status_code, 302, "Should redirect to login, or get status code 302, if the user is unauthenticated")
