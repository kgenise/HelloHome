from email.policy import default
from multiprocessing.dummy import active_children
from wsgiref.validate import validator
from hellohome import db, login_manager
from datetime import datetime

# Class UserMixin adds 4 attributes/methods for us
#extension expect user model to have 4 attributes/methods > Extension add all for us! > Class UserMixin
"""
isAuthenticated     True    valid credentials
isActive
isAnonymous
getId()
"""
from flask_login import UserMixin

# create function with decorator called USERLOADER | reloading user from user_id stored in the session | extension knows get user by id | naming convention required
@login_manager.user_loader 
def load_user(user_id):
    #return user for id (casted to an int)
    return User.query.get(int(user_id))

#Create models

#inherit from db.Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) #hashed to 60 characters
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') #hash: defaultable

    is_agent = db.Column(db.Boolean)
    phone_number = db.Column(db.String(10), nullable=True)
    realty_company = db.Column(db.String(20), nullable=True)

    
    # P ost CLASS
    #backref = another column to Post; author who wrote the post
    #lazy = SQLAlchemy loads from database (1 go)
    #NOT see post column
    posts = db.relationship('Post', backref='author', lazy=True)

    #how object printed when printed out
    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}', '{self.image_file}')"

## NO AUTHOR TO POST MODEL: RELATIONSHIP : USERS AUTHOR MANY POSTS : 1-MANY

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    # u ser : referencing TABLENAME & COLUMNNAME
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    #how object printed when printed out
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"