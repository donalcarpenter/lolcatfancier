from flask import Flask
from flask.ext.mongoengine import MongoEngine
from os import getenv
from flask_mail import Mail


app = Flask(__name__)

# security
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_EMAIL_SUBJECT_REGISTER'] = 'welcome to lolcatfancier'
app.config['SECURITY_EMAIL_SENDER'] = 'lolcatfancier@gmail.com'
#app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'security/templates/login_user.html'


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

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'thelolcatfancier@gmail.com'
pw = getenv('SMTP_PASSWORD')
app.config['MAIL_PASSWORD'] = pw
mail = Mail(app)