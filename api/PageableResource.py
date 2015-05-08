__author__ = 'Donal_Carpenter'

import re
from functools import wraps
from flask import request

class pageable_resource(object):
    def __init__(self, range_entity):
        self.range_entity = range_entity
        self.compiled_regex = re.compile('^{}=(\\d+)-(\\d*)$'.format(range_entity))
        self.start_index = 0
        self.end_index = None

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            vals = dict(kwargs)
            range_header = request.headers.get('Range')
            resp, data, code, headers, total_count = None, None, 200, {}, 0
            if(not range_header):
                return f(*args, **kwargs)

            range_values = self.compiled_regex.match(range_header)
            if(not range_values):
                return f(*args, **kwargs)

            self.start_index = int(range_values.groups()[0])
            try:
                self.end_index = int(range_values.groups()[1])
            except (TypeError, IndexError, ValueError):
                pass

            vals['start_index'] = self.start_index
            vals['end_index'] = self.end_index

            resp = f(args, **vals)

            if isinstance(resp, tuple):
                data, code, headers, total_count = resp
            else:
                data = resp

            if not headers:
                headers = {}

            headers['Accept-Range'] = self.range_entity
            if(self.start_index != 0 or (self.end_index or total_count) < total_count - 1):
                headers['Content-Range'] = '{} {}-{}/{}'.format(self.range_entity, self.start_index, self.end_index, total_count)
                code = 206

            return data, code, headers

        return wrapper