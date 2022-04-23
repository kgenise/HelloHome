from ast import Pass
from tokenize import Number, String
from typing import Optional
from wsgiref.validate import validator
from xml.dom import ValidationErr
from xmlrpc.client import Boolean
from flask_wtf import FlaskForm

#FileField(type of field allowed) & FileAllowed(validator of file type - jpg,png)
from flask_wtf.file import FileField, FileAllowed

#import current_user to ensure UpdateAccount validation checks only if first_name-last_name/email changed
from flask_login import current_user
from sqlalchemy import Integer

from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, Regexp
# need for validating first_name-last_name/email
from hellohome.models import User, Properties

#python classes representative of forms -> automatically created into html forms within template

#class RegistrationForm inherit from FlaskForm
class RegistrationForm(FlaskForm):
    #form fields ALSO imported classes

    #First Name is going to be LABEL in html
    # Checks/validations - another argument pass into field (also imported)
    # 1) Not empty
    # 2) Length btw 2-20 characters

    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20) ])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20) ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])

    is_agent = BooleanField('I am an Agent')
    
    phone_number = StringField('Phone Number')
    realty_company = StringField('Realty Company')

    #phone_number = StringField('Realty Company', validators=[Length(min=2, max=20) ])
    #realty_company = StringField('Realty Company', validators=[Length(min=2, max=20) ])
    

    submit = SubmitField('Sign Up')
    """
    #create a custom validation
    def validate_field(self, field):
        if True:
            raise ValidationError('Validation Message')
    """
    # check whether email already exists in database
    def validate_email(self, email):
        # value returned if exists, or is None
        user = User.query.filter_by(email=email.data).first()
        # if user exists with that EMAIL, raise error
        if user:
            raise ValidationError('That email is taken. Please choose a different one')

#class LoginForm inherit from FlaskForm
class LoginForm(FlaskForm):
    #form fields ALSO imported classes

    #Email is going to be LABEL in html
    # Checks/validations - another argument pass into field (also imported)
    # 1) Not empty
    # 2) Length btw 2-20 characters

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    #remember field - login using secured cookie
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

#>>>>>>>>>>> class UpdateAgentAccountForm inherit from FlaskForm
class UpdateAgentAccountForm(FlaskForm):
    #form fields ALSO imported classes

    #Email is going to be LABEL in html
    # Checks/validations - another argument pass into field (also imported)
    # 1) Not empty
    # 2) Length btw 2-20 characters

    ### now have
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20) ])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20) ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=2, max=20) ])
    realty_company = StringField('Realty Company', validators=[DataRequired(), Length(min=2, max=20) ])
    
    submit = SubmitField('Update')
    """
    #create a custom validation
    def validate_field(self, field):
        if True:
            raise ValidationError('Validation Message')
    """

    # only run validation checks if data submitted is DIFFERENT/CHANGED - import current_user
    # check whether email already exists in database
    def validate_email(self, email):
        
        if email.data != current_user.email:
            # value returned if exists, or is None
            user = User.query.filter_by(email=email.data).first()
            # if user exists with that EMAIL, raise error
            if user:
                raise ValidationError('That email is taken. Please choose a different one')


#+++++++++++ class UpdateUserAccountForm inherit from FlaskForm
class UpdateUserAccountForm(FlaskForm):
    #form fields ALSO imported classes

    #Email is going to be LABEL in html
    # Checks/validations - another argument pass into field (also imported)
    # 1) Not empty
    # 2) Length btw 2-20 characters

    ### now have
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20) ])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20) ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    
    submit = SubmitField('Update')
    """
    #create a custom validation
    def validate_field(self, field):
        if True:
            raise ValidationError('Validation Message')
    """

    # only run validation checks if data submitted is DIFFERENT/CHANGED - import current_user
    # check whether email already exists in database
    def validate_email(self, email):
        
        if email.data != current_user.email:
            # value returned if exists, or is None
            user = User.query.filter_by(email=email.data).first()
            # if user exists with that EMAIL, raise error
            if user:
                raise ValidationError('That email is taken. Please choose a different one')

class PostForm(FlaskForm):
    for_type = SelectField('For Type', 
                            validators=[DataRequired()],
                            choices=[('Sale', 'For Sale'), ('Rent', 'For Rent')])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=1, max=2147483647)])
    num_bed = IntegerField('Number of Beds', validators=[DataRequired(), NumberRange(min=1, max=100)])
    num_bath = IntegerField('Number of Baths', validators=[DataRequired(), NumberRange(min=1, max=100)])
    building_size = IntegerField('Building Size', validators=[DataRequired(), NumberRange(min=1, max=2147483647)])
    land_size = IntegerField('Land Size', validators=[DataRequired(), NumberRange(min=1, max=2147483647)])
    street = StringField('Street', validators=[DataRequired(), Length(max=60)])
    city = StringField('City', validators=[DataRequired(), Length(max=20)])
    state = SelectField('State', 
                            validators=[DataRequired()],
                            choices=[('FL', 'Florida'), ('GA', 'Georgia')])
    zip = StringField('Zip', validators=[DataRequired(), Length(min=5,max=5), Regexp('[0-9]{5}', message="Please enter a 5-digit zipcode. For example: 33617")])
    picture = FileField('Property Picture', validators=[FileAllowed(['jpg', 'png'])])

    description = TextAreaField('Description', validators=[DataRequired()])
    gen_property_type = SelectField('Property Type', 
                            validators=[DataRequired()],
                            choices=[('Single Family', 'Single Family'), ('Townhouse', 'Townhouse'), ('Condo', 'Condo'), ('Multifamily', 'Multifamily')])
    gen_year_built = IntegerField('Year Built', validators=[DataRequired(), NumberRange(min=1000,max=2022,message="Please enter a 4-digit year. For example: 2010")])
    gen_stories = IntegerField('Stories', validators=[DataRequired(), NumberRange(min=0)])
    gen_hoa = BooleanField('HOA')
    
    ext_roof = StringField('Roof', validators=[DataRequired()]) 
    ext_const_materials = StringField('Construction Materials', validators=[DataRequired()]) 
    ext_road_surf_type = StringField('Road Surface Type', validators=[DataRequired()]) 
    ext_foundation = StringField('Foundation', validators=[DataRequired()]) 
    ext_fencing = StringField('Fencing', validators=[DataRequired()]) 
    ext_parking = StringField('Parking', validators=[DataRequired()]) 
    ext_pool = BooleanField('Pool')
    ext_spa = BooleanField('Spa')
    ext_sprinklers = BooleanField('Sprinklers')
    ext_sewer = BooleanField('Sewer')

    int_app_included = TextAreaField('Appliances Included', validators=[DataRequired()])
    int_flooring = StringField('Flooring', validators=[DataRequired()])
    int_fireplace = BooleanField('Fireplace')

    submit = SubmitField('Post')