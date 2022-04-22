# python thinks its a pkg if contains __init__.py

### sourced from flask.pocoo.org
# import flask class
from contextlib import nullcontext

from flask import Flask

#import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

#import Bcrypt - password hashing algorithm
from flask_bcrypt import Bcrypt

# Login handling
from flask_login import LoginManager

#extract from config.py file
#from config import host, port, database, user, password

# import app varia  ble: set to instance of flask class, passing __name__
# __name__: special python variable represents module name
# run python main.py directly: __name__ = __main__
# flask look for templates & static files
# >>instantiated flask application
app = Flask(__name__)

#secret key - prevent against modification of cookies & Cross-Site requests/forgery attacks
#set of random characters
# 16 = no. of bytes
#cmd: python | import secrets | secrets.token_hex(16) | exit() | clear
#NEED TO MAKE THIS ENVIORNMENT VARIABLE
app.config['SECRET_KEY'] = '7d43f48cb2361993c56d7d2012803df7'

#Set URI
#app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{password}@{host}/{database}"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zxkcchntuqdmgn:097bdf7f9637792a36d5ec03acc859bda681f78611c2ffc180eea5e33750c174@ec2-18-214-134-226.compute-1.amazonaws.com:5432/d31no865tm4dj8'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zxkcchntuqdmgn:097bdf7f9637792a36d5ec03acc859bda681f78611c2ffc180eea5e33750c174@ec2-18-214-134-226.compute-1.amazonaws.com:5432/d31no865tm4dj8'

#SQLAlchemy database instance
#db structure as classes/models
db = SQLAlchemy(app)

# pass in app to bcrypt to initialize
bcrypt =Bcrypt(app)

#create an instance of LoginManager & pass in app in class
login_manager = LoginManager(app)
#extension where login route located (@loginrequired) = function name of route/url_for
login_manager.login_view = 'login'
#clean up flash messages (blue)
login_manager.login_message_category = 'info'

from hellohome import routes

db.create_all()