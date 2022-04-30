from email.policy import default
from multiprocessing.dummy import active_children
from wsgiref.validate import validator
from hellohome import db, login_manager
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from PIL import Image
import io
import base64

import zlib

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
    #return user for id
    return User.query.get(user_id)

##### need default image for tables
def default_picture(file_path, type):
    # open default profile image from static folder
    image = Image.open(file_path)

    if type == 'profile':
        output_size = (100, 100)
    elif type == 'property':
        output_size = (400, 200)
    
    image.thumbnail(output_size)
    default_image = io.BytesIO()
    
    # save so that PIL know what image format
    image.save(default_image, format='PNG')

    # retrieve byte string to save in database
    byte_image = base64.b64encode(default_image.getvalue()).decode('ascii')

    # compress string
    # compressed = zlib.compress(byte_image)

    return byte_image

#Create an Association Table
user_property = db.Table('user_property',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id')),
    db.Column('property_id', db.Integer, db.ForeignKey('properties.id'))
)

#Create models

#inherit from db.Model
class User(db.Model, UserMixin):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) #hashed to 60 characters
    image_file = db.Column(db.Text, default=default_picture('hellohome\static\profile_pics\default.jpg', 'profile'))

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

    #how object printed when printed out
    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}', '{self.image_file}')"


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
    image = db.Column(db.Text, default=default_picture('hellohome\static\house1.jpg', 'property'))

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

    # u ser : referencing TABLENAME & COLUMNNAME
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE', match='FULL'), nullable=False)

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

        Properties = Properties(many=True)
#--------------------------------------------------------------------------