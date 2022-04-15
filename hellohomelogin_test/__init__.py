from flask import Flask
from flask_login import LoginManager
from models import db, User
from sqlalchemy import *
from config import host, port, database, user, password

def create_app():
    app = Flask(__name__)

    # Create the database DBNAME in postgresql first
    # postgresql://USERNAME:PASSWORD@localhost/DBNAME
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/hellohomelogin_test'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{password}@{host}/{database}"

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # how to find a specific user from the ID that is stored in session cookie
    @login_manager.user_loader
    def load_user(user_id):
        # return User.query.get(int(user_id))
        return User.query.get(user_id)

    with app.test_request_context():
        db.create_all()

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
