from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'DB': 'fancied_lolcats'}
app.debug = True

db = MongoEngine(app)

@app.route('/')
def hello_world():
    return 'Hello MonGoose!'


if __name__ == '__main__':
    app.run()
