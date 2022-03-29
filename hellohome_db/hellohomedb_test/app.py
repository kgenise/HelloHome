from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# You need to create the database DBNAME in postgresql first
# postgresql://USERNAME:PASSWORD@localhost/DBNAME
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:admin@localhost/hellohometest'

db = SQLAlchemy(app)

# Creates tables
class Agent(db.Model):
  __tablename__='agents'

  agent_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  agent_fname = db.Column(db.String(20), nullable=False)
  agent_lname = db.Column(db.String(20), nullable=False)
  company = db.Column(db.String(100))
  agent_phone = db.Column(db.String(22), nullable=False)
  agent_email = db.Column(db.String(100), nullable=False, unique=True)
  agent_pw = db.Column(db.String(60), nullable=False)

  def __init__(self, agent_fname, agent_lname, company, agent_phone, agent_email, agent_pw):
    self.agent_fname = agent_fname
    self.agent_lname = agent_lname
    self.company = company
    self.agent_phone = agent_phone
    self.agent_email = agent_email
    self.agent_pw = agent_pw

class Buyer(db.Model):
  __tablename__ = 'buyers'

  buyer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  buyer_fname = db.Column(db.String(20), nullable=False)
  buyer_lname = db.Column(db.String(20), nullable=False)
  buyer_email = db.Column(db.String(100), nullable=False, unique=True)
  buyer_pw = db.Column(db.String(60), nullable=False)

  def __init__(self, buyer_fname, buyer_lname, buyer_email, buyer_pw):
    self.buyer_fname = buyer_fname
    self.buyer_lname = buyer_lname
    self.buyer_email = buyer_email
    self.buyer_pw = buyer_pw

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
  image = db.Column(db.LargeBinary)
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
    self.image = image

db.create_all()
db.session.commit()

# Chooses which information to input into database
@app.route('/', methods=['GET', 'POST'])
def index():
  if 'options' in request.form:
    selectedValue = request.form['options']
    return redirect(url_for('click', selectedValue=selectedValue))

  return render_template('index.html')

@app.route('/<selectedValue>')
def click(selectedValue):
    if selectedValue == 'agent':
      return render_template('agent.html')
    elif selectedValue == 'buyer':
      return render_template('buyer.html')
    else:
      return render_template('index.html')

# Form information for agents and buyers
@app.route('/submit', methods=['GET', 'POST'])
def submit():
  if request.method =='POST':
    if 'agent_form' in request.form:
      agent_fname = request.form['agent_fname']
      agent_lname = request.form['agent_lname']
      company = request.form['company']
      agent_phone = request.form['agent_phone']
      agent_email = request.form['agent_email']
      agent_pw = request.form['agent_pw']

      aemail_exists = db.session.query(db.exists().where(Agent.agent_email==agent_email)).first()

      if True in aemail_exists:
        return render_template('fail.html')
      else:
        agent = Agent(agent_fname, agent_lname, company, agent_phone, agent_email, agent_pw)
        db.session.add(agent)
        db.session.commit()

      # Fetch certain agent
      agentResult=db.session.query(Agent).filter(Agent.agent_id==1)
      for result in agentResult:
        return render_template('success.html', data=agent_fname)
    
    elif 'buyer_form' in request.form:
      buyer_fname = request.form['buyer_fname']
      buyer_lname = request.form['buyer_lname']
      buyer_email = request.form['buyer_email']
      buyer_pw = request.form['buyer_pw']

      bemail_exists = db.session.query(db.exists().where(Buyer.buyer_email==buyer_email)).first()

      if True in bemail_exists:
        return render_template('fail.html')
      else:
        buyer = Buyer(buyer_fname, buyer_lname, buyer_email, buyer_pw)
        db.session.add(buyer)
        db.session.commit()
        return render_template('success.html', data=buyer_fname)
        
    else:
      return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)