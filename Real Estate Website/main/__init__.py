from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from main.config import host, port, database, user, password


app = Flask(__name__)

app.config['SECRET_KEY']='12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://iuhoddygfyicbe:40dce1a7748da81a09490e042b87bf3215b135e5099c06460a852a37ca8b1409@ec2-44-194-92-192.compute-1.amazonaws.com/de4f8aa2uagb7k'

db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


# db.create_all()
# db.session.commit()

from main import routes