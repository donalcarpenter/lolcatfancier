__author__ = 'Donal_Carpenter'

from flask import url_for
from flask.ext.restful import Resource, reqparse, marshal_with, fields
from models.LolCat import LolCat as LolCatDAO
from werkzeug.datastructures import FileStorage
import re
from  api.PageableResource import pageable_resource

lolcat_parser = reqparse.RequestParser()
lolcat_parser.add_argument('title', type=str, help='you need to add a title', required=True)
lolcat_parser.add_argument('blurb', type=str)
lolcat_parser.add_argument('source', type=str)
lolcat_parser.add_argument('image', type=FileStorage, location='files')

class ImageUriGenerator(fields.Raw):
    def format(self, value):
        return url_for('lolcat.image_data', catid=value)

lolcat_fields = {
    'title': fields.String,
    'blurb': fields.String,
    'source': fields.String,
    'image_uri': ImageUriGenerator(attribute='id'),
    'uri' : fields.Url('lolcat', absolute=True),
}

range_regex = re.compile("^lolcat=(\\d+)-(\\d*)$")

class LolCatListAPI(Resource):

    @marshal_with(lolcat_fields, envelope='lolcats')
    @pageable_resource('lolcat')
    def get(self, start_index=0, end_index=None):
        lolcats = LolCatDAO.objects.order_by("-created_at")[start_index:end_index]
        res = [m._data for m in lolcats]
        return res, 200, {}, lolcats.count(with_limit_and_skip=False)

    @marshal_with(lolcat_fields)
    def post(self):
        args = lolcat_parser.parse_args()
        lolcat = LolCatDAO()
        LolCatListAPI.update_lolcat_with_args(lolcat, args)
        lolcat.save()
        return lolcat._data, 201

    @staticmethod
    def update_lolcat_with_args(lolcat, args):
        lolcat.blurb = args['blurb']

        image = args['image']
        if image and isinstance(image, FileStorage):
            lolcat.image_data.new_file()
            lolcat.image_data.content_type = image.content_type
            lolcat.image_data.write(image.stream.read())
            lolcat.image_data.close()
            image.close()
        lolcat.title = args['title']
        lolcat.source = args['source']

class LolCatAPI(Resource):
    @marshal_with(lolcat_fields, envelope='lolcats')
    def get(self, id):
        puss = LolCatDAO.objects.get_or_404(id=id)
        return puss._data

    def put(self, id):
        args = lolcat_parser.parse_args()
        lolcat = LolCatDAO.objects.get_or_404(id=id)
        LolCatListAPI.update_lolcat_with_args(lolcat, args)
        lolcat.save()
        return 200

    def delete(self, id ):
        cat = LolCatDAO.objects.get_or_404(id=id)
        cat.delete()
        return 200