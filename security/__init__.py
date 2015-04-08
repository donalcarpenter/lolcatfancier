__author__ = 'Donal_Carpenter'
from app import app, db
from flask.ext.security import Security, MongoEngineUserDatastore
from security.models import User, Role

user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

#app.config['SECURITY_URL_PREFIX'] = 'security'
#app.config['SECURITY_PASSWORD_HASH'] = bcrypt




@app.before_first_request
def create_dummy_user():
    pass
    #user_datastore.create_user(email='donal.carpenter@yahoo.com', password='password')


