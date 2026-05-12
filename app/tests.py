import unittest
from app import create_app, db
from app.config import TestConfig
from app.models import Blocks
from app.db_population import populate_blocks, populate_conditions

class BasicTests(unittest.TestCase):
    def setUp(self):
        test_app = create_app(TestConfig)
        self.app_context = test_app.app_context()
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

        self.assertIn("1", condition_ids, "Grass should have condition ID 1 (Overworld Block)")
        self.assertNotIn("2", condition_ids, "Grass should not have condition ID 2 (Otherworld Block)")
