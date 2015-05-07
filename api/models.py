__author__ = 'Donal_Carpenter'

from flask import request, url_for
from flask.ext.restful import Resource, reqparse, marshal_with, fields
from models.LolCat import LolCat as LolCatDAO
from werkzeug.datastructures import FileStorage, Range
from views import items_per_page
import re

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
    def get(self):
        start_index = 0
        end_index = start_index + items_per_page

        range_header = request.headers.get('Range')

        if range_header:
            range_values = range_regex.match(range_header)
            if range_values:
                start_index = int(range_values.groups()[0])
                try:
                    end_index = int(range_values.groups()[1])
                except (TypeError, IndexError, ValueError):
                    end_index = None

        lolcats = LolCatDAO.objects.order_by("-created_at")[start_index:end_index]
        total_count = lolcats.count(with_limit_and_skip=False)
        headers = {'Accept-Ranges': 'lolcat'}
        if(start_index != 0 or end_index < total_count - 1):
            headers['Content-Range'] = 'lolcat {}-{}/{}'.format(start_index, end_index or total_count - 1, total_count)
        res = [m._data for m in lolcats]
        return res, 200, headers

    def post(self):
        pass

class LolCatAPI(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id ):
        pass
