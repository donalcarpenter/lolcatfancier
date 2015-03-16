import datetime
from lolcatfancier import db


class LolCat(db.Document):
    created_at = db.DateTimeField(default = datetime.datetime.now, required=True)
    title = db.StringField(required=True)
    blurb = db.StringField(required=False)
    source = db.StringField(required=False)
    image = db.StringField(required=False)
    up_votes = db.IntField(default=0)
    down_votes = db.IntField(default=0)

    def __repr__(self):
        return '<lolcat {} {}>'.format(self.id, self.title)