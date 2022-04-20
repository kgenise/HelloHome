from codecs import BufferedIncrementalDecoder


from flask import render_template, url_for, flash, redirect, request


from main.forms import createUserForm, LoginForm, PropertyForm


from main.models import Users, Properties


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



@app.route("/register", methods=['GET','POST'])


def register():


    if current_user.is_authenticated:


        return redirect('/')


    form = createUserForm()


    account_type = request.form.get("accountType")


    fname = request.form.get("firstName")


    lname = request.form.get("lastName")


    email = request.form.get("email")


    phone = request.form.get("phone")


    pw = request.form.get("password")


    company = request.form.get("company")



    if form.validate_on_submit():


        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')


        user = Users(account_type=account_type, fname=fname, lname=lname, email=email, pw = hashed_pw, phone = phone, company =company)


        db.session.add(user)


        db.session.commit()
        print(user.id)


        return redirect("/login")



    return render_template("register.html", form=form)



@app.route("/create", methods=['GET','POST'])


def create():


    global isAgent


    print(isAgent)


    if isAgent == False:


            return redirect("/")


    if isAgent == True:
    


        form = PropertyForm()


        sale_type = request.form.get("saleType")


        property_type = request.form.get("propertyType")


        price = request.form.get("price")


        num_bed = request.form.get("bedrooms")


        num_bath = request.form.get("baths")


        building_size = request.form.get("buildingSize")


        land_size = request.form.get("landSize")


        street = request.form.get("street")


        city = request.form.get("city")


        zip = request.form.get("zip")


        state = request.form.get("state")


        # image = request.form.get("image")    


        id = request.form.get("userId")




        if form.validate_on_submit():


            property = Properties(sale_type=sale_type, property_type=property_type, price=price, num_bed=num_bed, num_bath=num_bath, building_size=building_size, land_size=land_size, street=street, city=city, state=state,zip=zip,user_id=id)


            db.session.add(property)


            db.session.commit()
            print(property.sale_type)


            return redirect("/viewing")   



        return render_template("create.html", form=form)



@app.route("/faq")


def faq():


    return render_template("faq.html")



@app.route("/manageproperties")


def manageproperties():


    return render_template("manageproperties.html")



@app.route("/search")


def search():


    return render_template("search.html")



@app.route("/about")


def about():


    return render_template("about.html")



@app.route("/listing")


def listing():


    return render_template("listing.html")



@app.route("/login", methods=['GET', 'POST'])


def login():


    if current_user.is_authenticated:


        return redirect('/')


    form = LoginForm()


    if form.validate_on_submit():


        user = Users.query.filter_by(email = form.email.data).first()


        # check if agent or buyer 


        # buyer = Buyer.query.filter_by(buyer_email = form.email.data).first()


        # agent = Agent.query.filter_by(agent_email = form.email.data).first()


        if not user:


            flash('Email not found. Please create a new account if you do not have one')


        if user and bcrypt.check_password_hash(user.pw, form.password.data):


            login_user(user, remember = form.rememberLogin.data)


            userType = user.account_type


            if userType == 'agent' or userType == 'Agent':


                global isAgent 


                isAgent = True


            print("logged in: " + str(user.fname))


            return redirect("/")
        


    return render_template("login.html", form = form)



@app.route("/viewing")


def view():


    properties = Properties.query.all()



    search = request.args.get('search')
    


    if search: 


        properties = Properties.query.filter(Properties.zip.contains(search))


    else:
        properties = Properties.query.all()




    saletype = request.args.get('saletype')
    price = request.args.get('price')
    propertytype = request.args.get('propertytype')
    beds = request.args.get('beds')
    baths = request.args.get('baths')

    
    # Search Conditions for filters
    if (saletype != None):
        properties = Properties.query.filter(Properties.sale_type == saletype)
    
    if (propertytype != None) :
        properties = Properties.query.filter(Properties.property_type == propertytype)

    if (beds != None) :
        properties = Properties.query.filter(Properties.num_bed >= beds)
    
    if (baths != None) :
        properties = Properties.query.filter(Properties.num_bath >= baths)

    if (price != None):
        properties = Properties.query.filter(Properties.price >= price)

    if (saletype != None and price != None):
        properties = Properties.query.filter(Properties.sale_type == saletype, Properties.price >= price)

    if (saletype != None and propertytype != None):
        properties = Properties.query.filter(Properties.sale_type == saletype, Properties.property_type == propertytype)

    if (saletype != None and beds != None):
        properties = Properties.query.filter(Properties.sale_type == saletype, Properties.num_bed >= beds)

    if (saletype != None and baths != None):
        properties = Properties.query.filter(Properties.sale_type == saletype, Properties.num_bath >= baths)

    if (saletype != None and propertytype != None and price != None):
        properties = Properties.query.filter(Properties.sale_type == saletype , Properties.property_type == propertytype, Properties.price >= price)

    if (saletype != None and propertytype != None and price != None and beds != None):
        properties = Properties.query.filter(Properties.sale_type == saletype , Properties.property_type == propertytype, Properties.price >= price, Properties.num_bed >= beds)

    if (saletype != None and propertytype != None and price != None and beds != None and baths != None):
        properties = Properties.query.filter(Properties.sale_type == saletype , Properties.property_type == propertytype, Properties.price >= price, Properties.num_bed >= beds, Properties.num_bath >= baths)

    if (price != None and propertytype != None):
        properties = Properties.query.filter(Properties.price >= price, Properties.property_type == propertytype)

    if (price != None and beds != None):
        properties = Properties.query.filter(Properties.price >= price, Properties.num_bed >= beds)

    if (price != None and baths != None):
        properties = Properties.query.filter(Properties.price >= price, Properties.num_bath >= baths)
    
    if (price != None and baths != None and beds != None):
        properties = Properties.query.filter(Properties.price >= price, Properties.num_bath >= baths, Properties.num_bed >= beds)

    if (price != None and propertytype != None and beds != None and baths != None):
        properties = Properties.query.filter(Properties.price >= price, Properties.property_type == propertytype, Properties.num_bed >= beds, Properties.num_bath >= baths)

    if (price != None and propertytype != None and beds != None):
        properties = Properties.query.filter(Properties.price >= price, Properties.property_type == propertytype, Properties.num_bed >= beds)

    if (price != None and propertytype != None and baths != None):
        properties = Properties.query.filter(Properties.price >= price, Properties.property_type == propertytype, Properties.num_bath >= baths)

    if (propertytype != None and beds != None):
        properties = Properties.query.filter(Properties.property_type == propertytype, Properties.num_bed >= beds)

    if (propertytype != None and baths != None):
        properties = Properties.query.filter(Properties.property_type == propertytype, Properties.num_bath >= baths)

    if (propertytype != None and beds != None and baths != None):
        properties = Properties.query.filter(Properties.property_type == propertytype, Properties.num_bed >= beds, Properties.num_bath >= baths)

    return render_template("viewing.html", properties = properties)



@app.route("/base")


def base():


    return render_template("base.html")



@app.route("/signup")


def signUp():


    return render_template("signUp.html")



@app.route("/logout")


def logout():


    global isAgent


    isAgent == False
    logout_user()
    print("logged out")


    return redirect('/')



