from app import app
from views import lol_cat_blueprint
from security.controller import profile_blueprint
import jinja_template_tests
import security
import api

app.register_blueprint(lol_cat_blueprint)
app.register_blueprint(profile_blueprint)



if __name__ == '__main__':


    app.run(debug=True)
