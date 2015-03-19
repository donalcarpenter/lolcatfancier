from app import app
from views import lolcatbp

app.register_blueprint(lolcatbp)

if __name__ == '__main__':
    app.run()
