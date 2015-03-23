import datetime
from app import db

class CommentReply(db.EmbeddedDocument):
    created_at  = db.DateTimeField(default = datetime.datetime.now, required=True)
    author      = db.StringField(required=False, default="anon")
    comment     = db.StringField(required=True)

    def __repr__(self):
        return '<reply {} {}>'.format(self.id, self.title)

class Comment(db.Document):
    created_at  = db.DateTimeField(default = datetime.datetime.now, required=True)
    author      = db.StringField(required=False, default="anon")
    comment     = db.StringField(required=True)
    replies     = db.ListField(db.EmbeddedDocumentField(CommentReply))
    lolcat      = db.ObjectIdField

    def __repr__(self):
        return '<comment {} {}>'.format(self.id, self.title)

class LolCat(db.Document):
    created_at  = db.DateTimeField(default = datetime.datetime.now, required=True)
    title       = db.StringField(required=True)
    blurb       = db.StringField(required=False)
    source      = db.StringField(required=False)
    image_data  = db.FileField()
    up_votes    = db.IntField(default=0)
    down_votes  = db.IntField(default=0)
    tags        = db.ListField(db.StringField())
    comments    = db.ListField(db.ReferenceField(Comment))

    def __repr__(self):
        return '<lolcat {} {}>'.format(self.id, self.title)
