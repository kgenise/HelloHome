from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Creates tables
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    pw = db.Column(db.String(100))
    type = db.Column(db.String(5))

    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':type
    }

    def __init__(self, fname, lname, email, pw):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.pw = pw

class Agent(User):
    __tablename__ = 'agents'

    id = db.Column(db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE', match='FULL'), primary_key=True, nullable=False)
    company = db.Column(db.String(100))
    phone = db.Column(db.String(22))

    user = db.relationship('User')

    __mapper_args__ = {
        'polymorphic_identity':'agent',
    }

    def __init__(self, fname, lname, email, pw, company=None, phone=None):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.pw = pw
        self.company = company
        self.phone = phone      

class Buyer(User):
    __tablename__ = 'buyers'

    id = db.Column(db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE', match='FULL'), primary_key=True, nullable=False)

    user = db.relationship('User')

    __mapper_args__ = {
        'polymorphic_identity':'buyer',
    }

    def __init__(self, fname, lname, email, pw):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.pw = pw

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
    agent_id = db.Column(db.ForeignKey('agents.id', ondelete='CASCADE', onupdate='CASCADE', match='FULL'), nullable=False)

    agent = db.relationship('Agent')

    def __init__(self, agent_id, sale_type, property_type, price, num_bed, num_bath, building_size, land_size, street, city, state, zip, image=None):
        self.agent_id = agent_id
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