__author__ = 'Donal_Carpenter'
from app import app
from flask.ext.restful import Api
from api.models import LolCatAPI, LolCatListAPI

api = Api(app)

api.add_resource(LolCatAPI, '/api/lolcats/<string:id>', endpoint='lolcat')
api.add_resource(LolCatListAPI, '/api/lolcats', endpoint='lolcats')

