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


#Create an Association Table
user_property = db.Table('user_property',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('property_id', db.Integer, db.ForeignKey('properties.id'))
)

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
    properties = db.relationship('Properties', backref='agent', lazy=True)

    # savers - fake column on Properties
    savedProps = db.relationship('Properties', secondary=user_property, backref='savers')

    #user_name.savedProps.append(property.id)
    
    #how object printed when printed out
    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}', '{self.image_file}')"

## NO AUTHOR TO POST MODEL: RELATIONSHIP : USERS AUTHOR MANY POSTS : 1-MANY

"""
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
"""
class Properties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    for_type = db.Column(db.String(4), nullable=False)
    price = db.Column(db.Integer)
    num_bed = db.Column(db.Integer)
    num_bath = db.Column(db.Integer)
    building_size = db.Column(db.Integer)
    land_size = db.Column(db.Integer)
    street = db.Column(db.String(60))
    city = db.Column(db.String(20))
    state = db.Column(db.String(2))
    zip = db.Column(db.Integer)

    description = db.Column(db.Text, nullable=False)
    gen_property_type = db.Column(db.String(13))
    gen_year_built = db.Column(db.Integer)
    gen_stories = db.Column(db.Integer)
    gen_hoa = db.Column(db.Boolean)

    ext_roof = db.Column(db.String(20))
    ext_const_materials = db.Column(db.String(20))
    ext_road_surf_type = db.Column(db.String(20))
    ext_foundation = db.Column(db.String(20))
    ext_fencing = db.Column(db.String(20))
    ext_parking = db.Column(db.String(20))
    ext_pool = db.Column(db.Boolean)
    ext_spa = db.Column(db.Boolean)
    ext_sprinklers = db.Column(db.Boolean)
    ext_sewer = db.Column(db.Boolean)

    int_app_included = db.Column(db.Text, nullable=False)
    int_flooring = db.Column(db.String(20))
    int_fireplace = db.Column(db.Boolean)
    property_image_file = db.Column(db.String(20), nullable=False, default='default.png') #hash: defaultable

    # u ser : referencing TABLENAME & COLUMNNAME
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    #how object printed when printed out
    def __repr__(self):
        return f"Properties('[{self.id}]', \
        ['{self.for_type}'], \
        ['{self.price}'], \
        ['{self.num_bed}'] \
        ['{self.num_bath}'], \
        ['{self.building_size}'],\
        ['{self.street}'],\
        ['{self.city}'],\
        ['{self.state}'],\
        ['{self.zip}'],\
        ['{self.description}'],\
        ['{self.gen_property_type}'],\
        ['{self.gen_year_built}'],\
        ['{self.gen_stories}'],\
        ['{self.gen_hoa}'],\
        ['{self.ext_roof}'],\
        ['{self.ext_const_materials}'],\
        ['{self.ext_road_surf_type}'],\
        ['{self.ext_foundation}'],\
        ['{self.ext_fencing}'],\
        ['{self.ext_parking}'],\
        ['{self.ext_pool}'],\
        ['{self.ext_spa}'],\
        ['{self.ext_sprinklers}'],\
        ['{self.ext_sewer}'],\
        ['{self.int_app_included}'],\
        ['{self.int_flooring}'],\
        ['{self.int_fireplace}'] "
#--------------------------------------------------------------------------
