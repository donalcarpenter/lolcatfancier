from app import app
from views import lol_cat_blueprint
import jinja_template_tests

app.register_blueprint(lol_cat_blueprint)

if __name__ == '__main__':
    app.run()
