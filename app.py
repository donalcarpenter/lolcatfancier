from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'DB': 'heroku_app35290664'}
app.config["SECRET_KEY"] = "KeepThisS3cr3t123"
app.debug = True

WTF_CSRF_SECRET_KEY = "this should probbaly be a guid or something random"

db = MongoEngine(app)