from app import app
from views import lol_cat_blueprint
import jinja_template_tests
from os import getenv
from mongoengine import connect

app.register_blueprint(lol_cat_blueprint)

if __name__ == '__main__':
    mongourl = getenv("MONGOLAB_URI", "mongodb:localhost:27017/fancied_lolcats")
    connect(app.config['MONGODB_SETTINGS']['DB'], host=mongourl)
    app.run()
