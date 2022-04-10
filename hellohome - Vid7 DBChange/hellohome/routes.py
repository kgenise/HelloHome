#to grab file extension
import os

#random hex for picture filenames
import secrets

# image optimization Image class
from PIL import Image

from msilib.schema import ServiceControl


from flask import render_template, url_for, flash, redirect, request

#import from package (__init__.py ) : decorators using app
from hellohome import app, db, bcrypt

#create routes for these!
from hellohome.forms import RegistrationForm, LoginForm, UpdateAgentAccountForm, UpdateUserAccountForm

#import models ERROR! Circular import
from hellohome.models import User, Post

#User login AND change navigation of logged in users - current_user variable from flask_login extension
# login_required FOR not access http://127.0.0.1:5000/user_accountsettings if not logged in
from flask_login import login_user, current_user, logout_user, login_required

#db.create_all()


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

# routes: what type into our browser to go to different pages
# route decorators: handle backend for additional functionality will be shown on this SPECIFIC route
# "/" = root = home page

# multiple routes handled by same function: +Decorator
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)
    
@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/search")
def search():
    return render_template('search.html')

@app.route("/manageproperties")
def manageproperties():
    return render_template('manageproperties.html')

@app.route("/faq")
def faq():
    return render_template('faq.html')

##### REGISTER

# Method Not Allowed: list of allowed methods on route
@app.route("/register", methods=['GET', 'POST'])
def register():

    """
    #simply redirect logged in users who go to register page BACK to home page
    if current_user.is_authenticated:
        return redirect( url_for('home') )
    # weird for user to even see the register page!
    """
    

    # 1. create an instance of form to send to application
    form = RegistrationForm()
    # 2. pass form to template

    #AFTER create form & BEFORE create template: Validate on Submit: 
    # flash message in Flask - 1 time alert | alert styles 2nd argument category
    if form.validate_on_submit():
        #1. if form valid, hash password so ready to save from database
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #2. create new instance of User

        #Ensures that if no phone_number / realty_company (isAgent = False), then values are None instead of ""
        if form.phone_number.data == "":
            form.phone_number.data = None

        if form.realty_company.data == "":
            form.realty_company.data = None

        user = User(
            first_name=form.first_name.data, 
            last_name=form.last_name.data,
            email=form.email.data, 
            password=hashed_pw,
            is_agent=form.is_agent.data,
            phone_number=form.phone_number.data,
            realty_company=form.realty_company.data,
            )

        #3. add newly created user to database
        db.session.add(user)
        db.session.commit()
        #4. flash msg to user about account creation
        flash(f'Your account has been created {form.first_name.data + " " + form.last_name.data}! You are now able to log in', 'success')
        #5. redirect user to log in screen
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

##### LOGIN IN
@app.route("/login", methods=['GET', 'POST'])
def login():
    # 1. create an instance of form to send to application
    form = LoginForm()
    # 2. pass form to template

    #AFTER create form & BEFORE create template: Validate on Submit: 
    # flash message in Flask - 1 time alert | alert styles 2nd argument category
    if form.validate_on_submit():
        #1. Query database to make sure user exists: exists return OR None
        user = User.query.filter_by(email=form.email.data).first()
        #2. user exists, check if password matches database
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #3. log user in (import login_user)
            # form.remember.data = true of checked
            login_user(user, remember=form.remember.data)

            """
             #redirect us to page we now have access to after logging in
            http://127.0.0.1:5000/login?next=%2Fuser_accountsettings
            query parameter "next" = to route trying to login to before redirected
            quert parameters import
            """
            next_page = request.args.get('next')
    
            #4. redirect user to homepage
            #redirect to next page if exists, else redirect to home (ternary condition)
            return redirect(next_page) if next_page else redirect(url_for('home')) 
        else:
            #Unsuccessful login
            flash('Login Unsuccessful. Please check email and password', 'danger')
    #Unsuccessful login - show same login page
    return render_template('login.html', title='Log In', form=form)



   

##### LOGIN OUT
@app.route("/logout")
#import logout user
def logout():
    # known which user is currently logged in
    logout_user()
    return redirect(url_for('home')) 

##### USER PORTAL PAGES

@app.route("/user_landing_mysavedproperties")
def user_landing_mysavedproperties():
    return render_template('user_landing_mysavedproperties.html')

def save_picture(form_picture):
    #random hex name
    random_hex = secrets.token_hex(8)

    #grab file extension: filename w/o extension AND extension itself
    # _ throw away an unused variable
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    #root path all they way upto pkg dir 
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    #optimize image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    #save the form_picture to filesystem
    i.save(picture_path)

    #update user's profile picture in SEPARATE function
    return picture_fn

@app.route("/user_accountsettings", methods=['GET', 'POST'])
#need to login to access route
@login_required
def user_accountsettings():

    if current_user.is_agent:
        flash('You do not have access to view this page.', 'danger')
        return redirect(url_for('home'))

    form = UpdateUserAccountForm()
    
    #if form if valid on submitted
    if form.validate_on_submit():

        #set user's profile picture (optional) to picture file
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('user_accountsettings'))
        #reload get request so no "Are you sure you want to redirect" msg
    elif request.method == 'GET':
        #populate user with current_user's data
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('user_accountsettings.html', title='User Account Settings', image_file=image_file, form=form)

##### AGENT PORTAL PAGES

@app.route("/agent_landing_mypostedproperties")
def agent_landing_mypostedproperties():
    return render_template('agent_landing_mypostedproperties.html')

@app.route("/agent_postaproperty")
def agent_postaproperty():
    return render_template('agent_postaproperty.html')

@app.route("/agent_editaproperty")
def agent_editaproperty():
    return render_template('agent_editaproperty.html')

############## USER

@app.route("/agent_accountsettings", methods=['GET', 'POST'])
#need to login to access route
@login_required
def agent_accountsettings():

    if not current_user.is_agent:
        flash('You do not have access to view this page.', 'danger')
        return redirect(url_for('home'))

    form = UpdateAgentAccountForm()
    
    #if form if valid on submitted
    if form.validate_on_submit():

        #set user's profile picture (optional) to picture file
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.realty_company = form.realty_company.data

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('user_accountsettings'))
        #reload get request so no "Are you sure you want to redirect" msg
    elif request.method == 'GET':
        #populate user with current_user's data
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.realty_company.data = current_user.realty_company

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('agent_accountsettings.html', title='Agent Account Settings', image_file=image_file, form=form)