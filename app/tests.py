import unittest
from app import create_app, db
from app.config import TestConfig
from app.models import Blocks, User
from app.db_population import populate_blocks, populate_conditions


class BasicTests(unittest.TestCase):

    def setUp(self):
        self.test_app = create_app(TestConfig)
        self.client = self.test_app.test_client()

        self.app_context = self.test_app.app_context()
        self.app_context.push()

        db.create_all()

        populate_blocks()
        populate_conditions()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_block_conditions(self):
        grass = Blocks.query.filter_by(block_name="Grass").first()

        self.assertIsNotNone(grass)

        condition_ids = grass.condition_compatibility.split(",")

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

    def test_create_user(self):
        user = User(
            username="testuser",
            email="test@test.com",
            password_hash="hashedpassword"
        )

        db.session.add(user)
        db.session.commit()

        saved_user = User.query.filter_by(username="testuser").first()

        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.email, "test@test.com")

    def test_add_friend_relationship(self):
        user1 = User(
            username="alice",
            email="alice@test.com",
            password_hash="hash1"
        )

        user2 = User(
            username="bob",
            email="bob@test.com",
            password_hash="hash2"
        )

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        user1.friends.append(user2)
        db.session.commit()

        self.assertEqual(user1.friends.count(), 1)
        self.assertEqual(user1.friends.first().username, "bob")

    def test_login_page_loads(self):
        response = self.client.get("/login")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_signup_page_loads(self):
        response = self.client.get("/signup")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sign Up", response.data)

    def test_account_requires_login(self):
        response = self.client.get("/account", follow_redirects=False)

        self.assertEqual(response.status_code, 302)