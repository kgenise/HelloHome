from main import db

class Agent(db.Model):
  __tablename__='agents'

  agent_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  agent_fname = db.Column(db.String(20))
  agent_lname = db.Column(db.String(20))
  company = db.Column(db.String(100))
  agent_phone = db.Column(db.String(22))
  agent_email = db.Column(db.String(100))

  def __init__(self, agent_fname, agent_lname, company, agent_phone, agent_email):
    self.agent_fname = agent_fname
    self.agent_lname = agent_lname
    self.company = company
    self.agent_phone = agent_phone
    self.agent_email = agent_email

class Buyer(db.Model):
  __tablename__ = 'buyers'

  buyer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  buyer_fname = db.Column(db.String(20))
  buyer_lname = db.Column(db.String(20))
  buyer_email = db.Column(db.String(100))

  def __init__(self, buyer_fname, buyer_lname, buyer_email):
    self.buyer_fname = buyer_fname
    self.buyer_lname = buyer_lname
    self.buyer_email = buyer_email

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
  address = db.Column(db.String(100))
#   image = db.Column(db.LargeBinary)
  agent_id = db.Column(db.ForeignKey('agents.agent_id', ondelete='CASCADE', onupdate='CASCADE', match='FULL'), nullable=False)

  agent = db.relationship('Agent')

  def __init__(self, sale_type, property_type, price, num_bed, num_bath, building_size, land_size, address, image):
    self.sale_type = sale_type
    self.property_type = property_type
    self.price = price
    self.num_bed = num_bed
    self.num_bath = num_bath
    self.building_size = building_size
    self.land_size = land_size
    self.address = address
    # self.image = image