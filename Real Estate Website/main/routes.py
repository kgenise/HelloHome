from codecs import BufferedIncrementalDecoder
from flask import render_template, url_for, flash, redirect, request
from main.forms import CreateAgentAccountForm, CreateBuyerAccountForm, LoginForm, PropertyForm
from main.models import Buyer, Agent, Property
from main import app, db, bcrypt
from flask_login import login_user, current_user, logout_user

properties = []
buyers = []
agents = []

isAgent = False

@app.route("/")
def home():
    global isAgent
    return render_template("home.html", isAgent = isAgent)

@app.route("/account")
def account():

    return render_template("account.html") 

@app.route("/create", methods=['GET','POST'])
def create():
    global isAgent 
    form = PropertyForm()
    sale_type = request.form.get("saleType")
    property_type = request.form.get("propertyType")
    price = request.form.get("price")
    num_bed = request.form.get("bedrooms")
    num_bath = request.form.get("baths")
    building_size = request.form.get("buildingSize")
    land_size = request.form.get("landSize")
    address = request.form.get("address")
    id = request.form.get("agentId")


    if form.validate_on_submit():
        if current_user.is_authenticated and isAgent == True:
            property = Property(sale_type=sale_type, property_type=property_type, price=price, num_bed=num_bed, num_bath=num_bath, building_size=building_size, land_size=land_size, address=address, id = id)
            db.session.add(property)
            db.session.commit()
            print(property.sale_type)
            return redirect("/viewing")



    # if form.validate_on_submit():
    #     property = Property(sale_type=sale_type, property_type=property_type, price=price, num_bed=num_bed, num_bath=num_bath, building_size=building_size, land_size=land_size, address=address, image = 0)
    #     global properties
    #     properties.append(property)
    #     print(property.sale_type)
    #     return redirect("/viewing")
    # #     db.session.add(property)
    # #     db.session.commit()
    # #     return redirect('/viewing')
    # # else:
    # #     return redirect('/viewing')
        


    return render_template("create.html", form=form)

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/listing")
def listing():
    return render_template("listing.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        # check if agent or buyer 
        buyer = Buyer.query.filter_by(buyer_email = form.email.data).first()
        agent = Agent.query.filter_by(agent_email = form.email.data).first()
        if not buyer and not agent:
            flash('Email not found. Please create a new account if you do not have one')
        if buyer and bcrypt.check_password_hash(buyer.password, form.password.data):
            login_user(buyer, remember = form.rememberLogin.data)
            print("logged in: " + str(buyer.buyer_email))
            return redirect("/")
        if agent and bcrypt.check_password_hash(agent.password, form.password.data):
            login_user(agent, remember = form.rememberLogin.data)
            print("logged in: " + str(agent.agent_email))
            global isAgent 
            isAgent = True
            return redirect("/")
    return render_template("login.html", form = form)

@app.route("/viewing")
def view():
    properties = Property.query.all()
    
    return render_template("viewing.html", properties = properties)

@app.route("/base")
def base():
    return render_template("base.html")

@app.route("/signup")
def signUp():
    return render_template("signUp.html")

@app.route("/buyersignup", methods=['GET', 'POST'] )
def buyersignup():
    if current_user.is_authenticated:
        return redirect('/')
    form = CreateBuyerAccountForm()
    buyer_fname = request.form.get("firstName")
    buyer_lname = request.form.get("lastName")
    buyer_email = request.form.get("email")
    password = request.form.get("password")
    confPassword = request.form.get("confPassword")

    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        buyer = Buyer(buyer_email= buyer_email, buyer_fname=buyer_fname, buyer_lname=buyer_lname, password= hashed_pw)
        db.session.add(buyer)
        db.session.commit()
        # global buyers
        # buyers.append(buyer)
        # print(buyer.buyer_email)
        return redirect("/login")



    return render_template("buyersignup.html", form=form)

@app.route("/agentsignup", methods=['GET', 'POST'])
def agentsignup():
    if current_user.is_authenticated:
        return redirect('/')
    form = CreateAgentAccountForm()
    agent_fname = request.form.get("firstName")
    agent_lname = request.form.get("lastName")
    company = request.form.get("company")
    agent_phone = request.form.get("phoneNumber")
    agent_email = request.form.get("email")
    password = request.form.get("password")
    
    
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        agent = Agent(agent_fname=agent_fname, agent_lname=agent_lname, company=company, agent_phone=agent_phone, agent_email=agent_email, password=hashed_pw)
        db.session.add(agent)
        db.session.commit()
        flash('Your account has been created. Please log in', 'success')
        # agents.append(agent)
        # print(agent.agent_email)
        return redirect("/login")

    return render_template("agentsignup.html", form = form)


@app.route("/logout")
def logout():
    global isAgent
    isAgent == False
    logout_user()
    print("logged out")
    return redirect('/')

