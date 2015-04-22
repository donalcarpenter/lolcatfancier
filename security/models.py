import mongoengine as db
from flask.ext.security import UserMixin, RoleMixin
from flask.ext.mongoengine.wtf import model_form
__author__ = 'Donal_Carpenter'

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=255, unique=True)
    description = db.StringField(max_length=255)

    def __repr__(self):
        return '<role {} {}>'.format(id, self.name)

class User(db.Document, UserMixin):
    email = db.StringField(max_length=255, unique=True)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
    social_provider = db.StringField()
    social_id = db.StringField()

    def __repr__(self):
        return '<user {} {}>'.format(id, self.email)

UserForm = model_form(User)