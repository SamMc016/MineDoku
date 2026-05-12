import os
from app import create_app, db
#from app.populate_blocks import populate_blocks, populate_conditions
from app.config import DeploymentConfig

app = create_app(DeploymentConfig)

if __name__ == "__main__":
    app.run(debug=True)

"""
if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        populate_blocks()
        populate_conditions()

    app.run(debug=True)

app = create_app(DeploymentConfig)
migrate = Migrate(db, app)
"""
