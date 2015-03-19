from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'DB': 'fancied_lolcats'}
app.config["SECRET_KEY"] = "KeepThisS3cr3t123"
app.debug = True

db = MongoEngine(app)