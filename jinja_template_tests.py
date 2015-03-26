from app import app

__author__ = 'Donal_Carpenter'

app.jinja_env.tests['equalto'] = lambda value, other : value == other
