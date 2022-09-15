import email
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

#utilises SQLALCHEMY and sets the name of the database to database.db
db = SQLAlchemy()
DB_NAME = "database.db"

# creates flask app
def create_app():
    app = Flask(__name__)

    #handles routing options to prevent view errors
    app.url_map.strict_slashes = False

    #encrypts session data
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    #prefic url for blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Service_request, Status, Category

    #creates database
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #loads user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    from .models import User
    #ensures database is only created when when the database name doesnt already exist
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all(app=app)
            #inserts an admin user to the database upon inizialisation
            statement = User(email="test@test.com", password=generate_password_hash("1234567", method='sha256'), first_name="test", admin="true") 
            db.session.add(statement)
            db.session.commit()
        print('Created Database!')

 