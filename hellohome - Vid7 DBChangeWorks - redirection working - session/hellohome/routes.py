# from curses.ascii import isdigit
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

#to grab file extension
import os

#random hex for picture filenames
import secrets
# image optimization Image class
from PIL import Image
import io
import base64

from msilib.schema import Property, ServiceControl

from flask import render_template, url_for, flash, redirect, request, abort, url_for, session

#import from package (__init__.py ) : decorators using app
from hellohome import app, db, bcrypt

#create routes for these!
from hellohome.forms import RegistrationForm, LoginForm, SaveProperty, UpdateAgentAccountForm, UpdateUserAccountForm, PostForm, SearchForm, HomeForm

#import models ERROR! Circular import
from hellohome.models import User, Properties, user_property

#User login AND change navigation of logged in users - current_user variable from flask_login extension
# login_required FOR not access http://127.0.0.1:5000/user_accountsettings if not logged in
from flask_login import login_user, current_user, logout_user, login_required

from sqlalchemy import func

# routes: what type into our browser to go to different pages
# route decorators: handle backend for additional functionality will be shown on this SPECIFIC route
# "/" = root = home page


# multiple routes handled by same function: +Decorator
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    app.logger.info('------------------------------------------------------------------------------------------------')
    app.logger.info('>>> HOME PAGE <<<')
    
    properties = Properties.query.join(user_property,(user_property.c.property_id == Properties.id)).group_by(Properties.id).order_by( func.count(user_property.c.property_id).desc() ).limit(3)

    """
    SELECT user_property.property_id, count(property_id) as counts          func.count(User.id)
    FROM user_property                                                          filter(User.age == 25)
    RIGHT JOIN properties ON user_property.property_id = properties.id 
    join(user_property,(user_property.c.property_id == Properties.id))
    group by user_property.property_id                                        group_by(User.id)
    order by counts desc                                                    order_by(User.name.desc())
    limit 3;                                                                limit(2)
"""
    form_HomeForm = HomeForm()
    
    if form_HomeForm.validate_on_submit():
        app.logger.info('------------------------------------------------------------------------------------------------')
        app.logger.info('HOME - VALIDATED ON SUBMIT')
        
        search_data = str(form_HomeForm.home_searchbar.data)
        app.logger.info("searchbar.data = " + search_data)

        for_data = str(form_HomeForm.home_fortype.data)
        app.logger.info("fortype.data = " + for_data)

        session['search_data']=search_data
        session['for_data']=for_data

        return redirect(url_for('search', search_data=session["search_data"], for_data=session["for_data"], image_file=user_image()))
    else:
        app.logger.info('------------------------------------------------------------------------------------------------')
        app.logger.info('HOME - *not* VALIDATED ON SUBMIT')
        return render_template('home.html', properties=properties, form=form_HomeForm, image_file=user_image())

    
   
def user_image():
    if current_user.is_authenticated:
        image_file = current_user.image_file
    else:
        image_file = save_picture('hellohome\static\profile_pics\default.jpg', 'profile', 'default')
    
    return image_file

@app.route("/about")
def about():
    return render_template('about.html', title='About', image_file=user_image())


@app.route("/search", methods=['GET', 'POST'])
def search():
    app.logger.info('------------------------------------------------------------------------------------------------')
    app.logger.info('>>> SEARCH PAGE <<<')
    
    form = SearchForm()

    ## if redirect(GET request) from Home page
    if request.method == 'GET':
        app.logger.info('>>> SEARCH PAGE --- GET (inside)<<')

        try:
            # if session["search_data"] EXISTS
            if (session["search_data"] is not None):

                form = SearchForm(fortype=session["for_data"], searchbar=session["search_data"])
                properties = Properties.query.filter(Properties.zip==session["search_data"], Properties.for_type==session["for_data"]).all()

                # reset values to None so Search link in navbar does not open to same values
                session["search_data"] = None
                session["for_data"] = None
                return render_template('search.html', properties=properties, form=form, image_file=user_image())
        except KeyError:
            # if session["search_data"] does NOT EXIST (navbar Search)
            form = SearchForm()
            properties = Properties.query.filter(Properties.for_type=="Sale").all()
            return render_template('search.html', properties=properties, form=form, image_file=user_image())

    ## if submit(POST request) VALID from Search page
    if form.validate_on_submit():
        app.logger.info("Inside Validate On Submit")
        searchbar = form.searchbar.data
        fortype = form.fortype.data
        minprice = form.minprice.data
        maxprice = form.maxprice.data
        propertytype = form.propertytype.data
        num_bed = form.num_bed.data
        num_bath = form.num_bath.data
        
        # if propertytype == "Any", don't filter based on propertype
        if (propertytype == "Any"):
            properties = Properties.query.filter(Properties.zip==searchbar, Properties.for_type==form.fortype.data, Properties.price >= minprice, Properties.price <= maxprice, Properties.num_bed >= num_bed, Properties.num_bath >= num_bath).all()
        else:
            properties = Properties.query.filter(Properties.zip==searchbar, Properties.for_type==form.fortype.data, Properties.price >= minprice, Properties.price <= maxprice, Properties.gen_property_type == propertytype, Properties.num_bed >= num_bed, Properties.num_bath >= num_bath).all()
        
        return render_template('search.html', properties=properties, form=form, image_file=user_image())

    ## if submit(POST request) NOT VALID from Search page
    else:
        # reset search form
        form.searchbar.data = ""
        form.fortype.data = "Sale"
        form.minprice.data = 0
        form.maxprice.data = 0
        form.propertytype.data = "Any"
        form.num_bed.data = 0
        form.num_bath.data = 0

        # filter only fortype (Sale)
        properties = Properties.query.filter(Properties.for_type==form.fortype.data).all()

        return render_template('search.html', properties=properties, form=form, image_file=user_image())

@app.route("/faq")
def faq():
    return render_template('faq.html', image_file=user_image())

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
            first_name=form.first_name.data.title(), 
            last_name=form.last_name.data.title(),
            email=form.email.data.lower(), 
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
    return render_template('user_landing_mysavedproperties.html', properties=current_user.savedProps, image_file=current_user.image_file)

def save_picture(form_picture, type, default):
    if default == 'default':
        i = Image.open(form_picture)
    else:
        # get bytes from FileStorage object
        input_image = form_picture.read()
        i = Image.open(io.BytesIO(input_image))
    
    #optimize image
    if type == 'profile':
        output_size = (100, 100)
    if type == 'property':
        output_size = (400, 200)

    i.thumbnail(output_size)

    display_image = io.BytesIO()
    
    #save the form_picture
    i.save(display_image, format='PNG')

    # return image bytes
    dataurl = base64.b64encode(display_image.getvalue()).decode('ascii')

    return dataurl

@app.route("/user_accountsettings", methods=['GET', 'POST'])
#need to login to access route
@login_required
def user_accountsettings():

    if current_user.is_agent:
        flash('You do not have access to view this page, Agent.', 'danger')
        return redirect(url_for('home'))

    form = UpdateUserAccountForm()
    
    #if form if valid on submitted
    if form.validate_on_submit():

        #set user's profile picture (optional) to picture file
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'profile', 'no')
            current_user.image_file = picture_file

        current_user.first_name = form.first_name.data.title()
        current_user.last_name = form.last_name.data.title()
        current_user.email = form.email.data.lower()

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('user_accountsettings'))
        #reload get request so no "Are you sure you want to redirect" msg
    elif request.method == 'GET':
        #populate user with current_user's data
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.picture.data = current_user.image_file

    return render_template('user_accountsettings.html', title='User Account Settings', image_file=current_user.image_file, form=form)

##### AGENT PORTAL PAGES

@app.route("/agent_landing_mypostedproperties")
def agent_landing_mypostedproperties():
    properties = Properties.query.filter_by(agent=current_user).all()
    return render_template('agent_landing_mypostedproperties.html', properties=properties, image_file=current_user.image_file)

####################################### agent_postaproperty
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit(): 
        # adding property to DB
        property = Properties(
            for_type = form.for_type.data,
            price = form.price.data,
            num_bed = form.num_bed.data,
            num_bath = form.num_bath.data,
            building_size = form.building_size.data, 
            land_size = form.land_size.data,
            street = form.street.data.title(),
            city = form.city.data.title(),
            state = form.state.data,
            zip = form.zip.data,
            image = form.picture.data,

            description = form.description.data,
            gen_property_type = form.gen_property_type.data,
            gen_year_built = form.gen_year_built.data,
            gen_stories = form.gen_stories.data,
            gen_hoa = form.gen_hoa.data,

            ext_roof = form.ext_roof.data.title(),
            ext_const_materials = form.ext_const_materials.data.title(),
            ext_road_surf_type = form.ext_road_surf_type.data.title(),
            ext_foundation = form.ext_foundation.data.title(),
            ext_fencing = form.ext_fencing.data.title(),
            ext_parking = form.ext_parking.data.title(),
            ext_pool = form.ext_pool.data,
            ext_spa = form.ext_spa.data,
            ext_sprinklers = form.ext_sprinklers.data,
            ext_sewer = form.ext_sewer.data,

            int_app_included = form.int_app_included.data.title(),
            int_flooring = form.int_flooring.data.title(),
            int_fireplace = form.int_fireplace.data,
            agent=current_user)
        
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'property', 'no')
            property.image = picture_file
        
        db.session.add(property)
        db.session.commit() 
        flash('Your post has been created!', 'success')
        # SHOULD REDIRECT TO MYPOSTEDPROPERTIES PAGE
        return redirect(url_for('agent_landing_mypostedproperties'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post', image_file=current_user.image_file)

@app.route("/post/<int:property_id>", methods=['GET', 'POST'])
def post(property_id):
    form = SaveProperty()
    property = Properties.query.get_or_404(property_id)

    ####
    if form.validate_on_submit():
        #create new instance of user-property table
        #if property in current_user.savedProps:
        #for property in current_user.savedProps: print(follower.name)

        if property not in current_user.savedProps:
            current_user.savedProps.append(property)
            ###user_property(form.userid.data, form.propertyid.data)
            db.session.commit() 
        else:
            current_user.savedProps.remove(property)
            db.session.commit()
    ####

    return render_template('property.html', title=property.street, property=property, form=form, image_file=user_image())
    
    
@app.route("/post/<int:property_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(property_id):
    property = Properties.query.get_or_404(property_id)
    #only user who wrote post can update
    if property.agent != current_user:
        abort(403)
    form = PostForm()

    #update post if form validates (Accept post requests)
    if form.validate_on_submit():
        property.for_type = form.for_type.data
        property.price = form.price.data
        property.num_bed = form.num_bed.data
        property.num_bath = form.num_bath.data
        property.building_size = form.building_size.data
        property.land_size = form.land_size.data
        property.street = form.street.data.title()
        property.city = form.city.data.title()
        property.state = form.state.data
        property.zip = form.zip.data
        property.description = form.description.data
        property.gen_property_type = form.gen_property_type.data
        property.gen_year_built = form.gen_year_built.data
        property.gen_stories = form.gen_stories.data
        property.gen_hoa = form.gen_hoa.data
        property.ext_roof = form.ext_roof.data.title()
        property.ext_const_materials = form.ext_const_materials.data.title()
        property.ext_road_surf_type = form.ext_road_surf_type.data.title()
        property.ext_foundation = form.ext_foundation.data.title()
        property.ext_fencing = form.ext_fencing.data.title()
        property.ext_parking = form.ext_parking.data.title()
        property.ext_pool= form.ext_pool.data
        property.ext_spa = form.ext_spa.data
        property.ext_sprinklers = form.ext_sprinklers.data
        property.ext_sewer = form.ext_sewer.data
        property.int_app_included = form.int_app_included.data.title()
        property.int_flooring = form.int_flooring.data
        property.int_fireplace = form.int_fireplace.data
        #no need to db.session.add() since already in database, we are just updating
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'property', 'no')
            property.image = picture_file

        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('post', property_id=property.id))
    elif request.method == 'GET':
        #add current form details as placeholder text - GET method
        form.for_type.data = property.for_type
        form.price.data = property.price
        form.num_bed.data = property.num_bed
        form.num_bath.data = property.num_bath
        form.building_size.data = property.building_size
        form.land_size.data = property.land_size
        form.street.data = property.street
        form.city.data = property.city
        form.state.data = property.state
        form.zip.data = property.zip

        form.picture.data = property.image

        form.description.data = property.description
        form.gen_property_type.data = property.gen_property_type
        form.gen_year_built.data = property.gen_year_built
        form.gen_stories.data = property.gen_stories
        form.gen_hoa.data = property.gen_hoa
        form.ext_roof.data = property.ext_roof
        form.ext_const_materials.data = property.ext_const_materials
        form.ext_road_surf_type.data = property.ext_road_surf_type
        form.ext_foundation.data = property.ext_foundation
        form.ext_fencing.data = property.ext_fencing
        form.ext_parking.data = property.ext_parking
        form.ext_pool.data = property.ext_pool
        form.ext_spa.data = property.ext_spa
        form.ext_sprinklers.data = property.ext_sprinklers
        form.ext_sewer.data = property.ext_sewer
        form.int_app_included.data = property.int_app_included
        form.int_flooring.data = property.int_flooring
        form.int_fireplace.data = property.int_fireplace
        
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post', image_file=current_user.image_file)

@app.route("/post/<int:property_id>/delete", methods=['POST'])
@login_required
def delete_post(property_id):
    property = Properties.query.get_or_404(property_id)
    #only user who wrote post can delete
    if property.agent != current_user:
        abort(403)
    db.session.delete(property)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect( url_for('agent_landing_mypostedproperties') )

############## USER

@app.route("/agent_accountsettings", methods=['GET', 'POST'])
#need to login to access route
@login_required
def agent_accountsettings():

    if not current_user.is_agent:
        flash('You do not have access to view this page, User', 'danger')
        return redirect(url_for('home'))

    form = UpdateAgentAccountForm()
    
    #if form if valid on submitted
    if form.validate_on_submit():

        #set user's profile picture (optional) to picture file
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'profile', 'no')
            current_user.image_file = picture_file

        current_user.first_name = form.first_name.data.title()
        current_user.last_name = form.last_name.data.title()
        current_user.email = form.email.data.lower()
        current_user.phone_number = form.phone_number.data
        current_user.realty_company = form.realty_company.data.title()

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('agent_accountsettings'))
        #reload get request so no "Are you sure you want to redirect" msg
    elif request.method == 'GET':
        #populate user with current_user's data
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.realty_company.data = current_user.realty_company
        form.picture.data = current_user.image_file

    return render_template('agent_accountsettings.html', title='Agent Account Settings', image_file=current_user.image_file, form=form)