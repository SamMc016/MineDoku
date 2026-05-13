import os
from app import create_app, db
from app.db_population import (
    populate_blocks,
    populate_conditions,
    populate_users 
)
from app.config import DeploymentConfig

app = create_app(DeploymentConfig)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        populate_blocks()
        populate_conditions()
        populate_users()
        
    app.run(debug=True)
