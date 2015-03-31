from flask import Flask
from flask.ext.mongoengine import MongoEngine
from os import getenv

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
                                    'db': getenv('MONGOLAB_DB', 'fancied_lolcats'),
                                    'username': getenv('MONGOLAB_USER'),
                                    'password': getenv('MONGOLAB_PASSWORD'),
                                    'host': getenv('MONGOLAB_HOST'),
                                    'port': int(getenv('MONGOLAB_PORT', 0))
                                }
app.config["SECRET_KEY"] = "KeepThisS3cr3t123"
app.debug = True

WTF_CSRF_SECRET_KEY = "this should probbaly be a guid or something random"

db = MongoEngine(app)