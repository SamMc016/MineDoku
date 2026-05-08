from app import app
from app.populate_blocks import populate_blocks

with app.app_context():
    populate_blocks()

if __name__ == "__main__":
    app.run(debug=True)


"""
ALSO CHANGE AND MAKE A BASE.HTML FOR ALL COMMON HTML STUFF LIKE HEADER BAR 
MAKE A FORMS.PY TO STORE ALL FORM CLASSES
so... for the databases...
    delete all of my sql, and replace it with sqlalchemy
    make a new? or alter? the config.py file to include image (yk which one)
    then in the init file
        copy out the image under the one above
    before starting creation run
        flask db migration
    then create a new file called app/models.py and import db
        code is shown in the image below the ones above
    once the models (tables) are in run
        Flask db init
    to then add dummy data 
        open the flask shell with "flask shell"
        item = Item(attribute1=value, attribute2=value)
        db.session.add(item)
    once dummy data is added
        db.session.commit()
    DONE UP TO HERE
        
    WEBSITE FUNCTIONALITY NEEDS TO BE STARTED BEFORE RELATIONSHIPS ARE DEFINED
    to add relationships (DO THIS AND EVERYTHING FOLLOWING AFTER THE FIRST DB MIGRATION)
        foreignAttribute = db.relationship("foreignAttributeTable", back_populates="objectInstanceName")
    add helper methods like any normal python class
        normal method construction
        for functionality and responsiveness
            one to print?
    THEN in routes.py we can respond to requests for data by building models from database and then populating views w data
    make a controllers.py class to move big functions there
"""
"""
what do i need to do
    download textures for all blocks
    hardcode conditions and blocks in 
    start on game logic
        client side for 
            gameplay
            inventory pop up for guesses
    change condition/stats to grids

"""
