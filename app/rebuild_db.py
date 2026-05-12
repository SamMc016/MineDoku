from app import create_app, db 
from app.config import DeploymentConfig
from app.db_population import populate_blocks, populate_conditions

app = create_app(DeploymentConfig)

with app.app_context():
    db.drop_all()
    db.create_all()

    populate_blocks()
    populate_conditions()
    