from app import create_app, db
from app.db_population import *
from app.config import DeploymentConfig

app = create_app(DeploymentConfig)

if __name__ == "__main__": 
    with app.app_context(): # Creates and populates the database on website activation.
        db.create_all()

        populate_blocks()
        populate_conditions()
        populate_users()
        populate_user_stats()
        
    app.run(debug=True)
