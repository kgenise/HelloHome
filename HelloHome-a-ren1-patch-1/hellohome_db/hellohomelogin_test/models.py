from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Creates tables
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_type = db.Column(db.String(5))
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    pw = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(22))
    company = db.Column(db.String(100))
    properties = db.relationship('Property', backref='user', lazy='dynamic')

    def __init__(self, account_type, fname, lname, email, pw, phone=None, company=None):
        self.account_type = account_type
        self.fname = fname
        self.lname = lname
        self.email = email
        self.pw = pw
        self.phone = phone
        self.company = company

class Property(db.Model):
    __tablename__ = 'properties'

    listing_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sale_type = db.Column(db.CHAR(4))
    property_type = db.Column(db.String(100))
    price = db.Column(db.Numeric(19,2))
    num_bed = db.Column(db.Integer)
    num_bath = db.Column(db.Integer)
    building_size = db.Column(db.Integer)
    land_size = db.Column(db.Integer)
    street = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip = db.Column(db.String(10))
    image = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE', match='FULL'), nullable=False)

    def __init__(self, user_id, sale_type, property_type, price, num_bed, num_bath, building_size, land_size, street, city, state, zip, image=None):
        self.user_id = user_id
        self.sale_type = sale_type
        self.property_type = property_type
        self.price = price
        self.num_bed = num_bed
        self.num_bath = num_bath
        self.building_size = building_size
        self.land_size = land_size
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.image = image