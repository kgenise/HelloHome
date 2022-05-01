from ast import Pass
from tokenize import Number, String
from typing import Optional
from wsgiref.validate import validator
from xml.dom import ValidationErr
from xmlrpc.client import Boolean
from flask_wtf import FlaskForm

#FileField(type of field allowed) & FileAllowed(validator of file type - jpg,png,jpeg)
from flask_wtf.file import FileField, FileAllowed

#import current_user to ensure UpdateAccount validation checks only if first_name-last_name/email changed
from flask_login import current_user
from sqlalchemy import Integer

from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, Regexp, NoneOf
# need for validating first_name-last_name/email
from hellohome.models import User, Properties

#python classes representative of forms -> automatically created into html forms within template

#class RegistrationForm inherit from FlaskForm

invalidWords = ("select", "insert","*", "from", "where", "update", "delete")

def sqlCheck(FlaskForm, field):
    fieldData = field.data
    if isinstance(fieldData, str):
        words = fieldData.split(' ')
        for word1 in words:
            for word2 in invalidWords:
                if word1.lower() == word2.lower():
                    raise ValidationError("Invalid input: cannot use this statement")
        # if word == "select" or "insert" or "*" or "from" or "update" or "delete":
        #     raise ValidationError("Invalid input 1")

class RegistrationForm(FlaskForm):
    #form fields ALSO imported classes

    #First Name is going to be LABEL in html
    # Checks/validations - another argument pass into field (also imported)
    # 1) Not empty
    # 2) Length btw 2-20 characters

    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20), sqlCheck])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20), sqlCheck ])
    email = StringField('Email', validators=[DataRequired(), Email(), sqlCheck])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20), sqlCheck])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password'), sqlCheck])

    is_agent = BooleanField('I am an Agent')
    
    phone_number = StringField('Phone Number', validators=[sqlCheck])
    realty_company = StringField('Realty Company', validators = [sqlCheck])

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
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20), sqlCheck ])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20), sqlCheck ])
    email = StringField('Email', validators=[DataRequired(), Email(), sqlCheck])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg']), sqlCheck])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=2, max=20), sqlCheck ])
    realty_company = StringField('Realty Company', validators=[DataRequired(), Length(min=2, max=20), sqlCheck ])
    
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
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20), sqlCheck ])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20), sqlCheck ])
    email = StringField('Email', validators=[DataRequired(), Email(), sqlCheck])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg']), sqlCheck])
    
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
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=1, max=2147483647), sqlCheck])
    num_bed = IntegerField('Number of Beds', validators=[DataRequired(), NumberRange(min=1, max=100), sqlCheck])
    num_bath = IntegerField('Number of Baths', validators=[DataRequired(), NumberRange(min=1, max=100), sqlCheck])
    building_size = IntegerField('Building Size', validators=[DataRequired(), NumberRange(min=1, max=2147483647), sqlCheck])
    land_size = IntegerField('Land Size', validators=[DataRequired(), NumberRange(min=1, max=2147483647), sqlCheck])
    street = StringField('Street', validators=[DataRequired(), Length(max=60), sqlCheck])
    city = StringField('City', validators=[DataRequired(), Length(max=20), sqlCheck])
    state = SelectField('State', 
                            validators=[DataRequired(), sqlCheck],
                            choices= [("AL","Alabama"),("AK","Alaska"),("AZ","Arizona"),("AR","Arkansas"),("CA", "California"),("CO", "Colorado"),
                                        ("CT","Connecticut"),("DC","Washington DC"),("DE","Delaware"),("FL","Florida"),("GA","Georgia"),
                                        ("HI","Hawaii"),("ID","Idaho"),("IL","Illinois"),("IN","Indiana"),("IA","Iowa"),("KS","Kansas"),("KY","Kentucky"),
                                        ("LA","Louisiana"),("ME","Maine"),("MD","Maryland"),("MA","Massachusetts"),("MI","Michigan"),("MN","Minnesota"),
                                        ("MS","Mississippi"),("MO","Missouri"),("MT","Montana"),("NE","Nebraska"),("NV","Nevada"),("NH","New Hampshire"),
                                        ("NJ","New Jersey"),("NM","New Mexico"),("NY","New York"),("NC","North Carolina"),("ND","North Dakota"),("OH","Ohio"),
                                        ("OK","Oklahoma"),("OR","Oregon"),("PA","Pennsylvania"),("RI","Rhode Island"),("SC","South Carolina"),("SD","South Dakota"),
                                        ("TN","Tennessee"),("TX","Texas"),("UT","Utah"),("VT","Vermont"),("VA","Virginia"),("WA","Washington"),("WV","West Virginia"),
                                        ("WI","Wisconsin"),("WY","Wyoming")])
    zip = StringField('Zip', validators=[DataRequired(), Length(min=5,max=5), Regexp('[0-9]{5}', message="Please enter a 5-digit zipcode. For example: 33617"), sqlCheck])

    description = TextAreaField('Description', validators=[DataRequired(), sqlCheck])
    gen_property_type = SelectField('Property Type', 
                            validators=[DataRequired(), sqlCheck],
                            choices=[('Single Family', 'Single Family'), ('Townhouse', 'Townhouse'), ('Condo', 'Condo'), ('Multifamily', 'Multifamily'), ('House', 'House'), ('Apartment', 'Apartment')])
    gen_year_built = IntegerField('Year Built', validators=[DataRequired(), NumberRange(min=1000,max=2022,message="Please enter a 4-digit year. For example: 2010"), sqlCheck])
    gen_stories = IntegerField('Stories', validators=[DataRequired(), NumberRange(min=0), sqlCheck])
    gen_hoa = BooleanField('HOA')
    
    ext_roof = StringField('Roof', validators=[DataRequired(), sqlCheck]) 
    ext_const_materials = StringField('Construction Materials', validators=[DataRequired(), sqlCheck]) 
    ext_road_surf_type = StringField('Road Surface Type', validators=[DataRequired(), sqlCheck]) 
    ext_foundation = StringField('Foundation', validators=[DataRequired(), sqlCheck]) 
    ext_fencing = StringField('Fencing', validators=[DataRequired(), sqlCheck]) 
    ext_parking = StringField('Parking', validators=[DataRequired(), sqlCheck]) 
    ext_pool = BooleanField('Pool')
    ext_spa = BooleanField('Spa')
    ext_sprinklers = BooleanField('Sprinklers')
    ext_sewer = BooleanField('Sewer')

    int_app_included = TextAreaField('Appliances Included', validators=[DataRequired(), sqlCheck])
    int_flooring = StringField('Flooring', validators=[DataRequired(), sqlCheck])
    int_fireplace = BooleanField('Fireplace')

    picture = FileField('Add Property Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg']), sqlCheck])

    submit = SubmitField('Post')

## SaveProperty Form

#class SaveProperty inherit from FlaskForm
class SaveProperty(FlaskForm):

    ###NO NEED
    # userid = IntegerField('userid')
    # propertyid = IntegerField('propertyid')

    submit = SubmitField('Save Property')


#class SearchForm inherit from FlaskForm
class SearchForm(FlaskForm):
    searchbar = StringField('Search', render_kw={"placeholder": "Enter a 5 digit zipcode"}, validators=[Length(min=5,max=5), Regexp('[0-9]{5}', message="search : Please enter a 5-digit zipcode. For example: 33617"), sqlCheck])

    fortype = SelectField('Type',
                            choices=[('Sale', 'Sale'), 
                            ('Rent', 'Rent')])

    minprice = SelectField('Min Price',
                            choices=[(0, 'No Min'),
                            (10000, '$10000'),
                            (20000, '$20000'),
                            (30000, '$30000'),
                            (40000, '$40000'),
                            (50000, '$50000'),
                            (60000, '$60000'),
                            (70000, '$70000'),
                            (80000, '$80000'),
                            (90000, '$90000'),
                            (100000, '$100000'),
                            (110000, '$110000'),
                            (120000, '$120000'),
                            (130000, '$130000'),
                            (140000, '$140000'),
                            (150000, '$150000'),
                            (160000, '$160000'),
                            (170000, '$170000'),
                            (180000, '$180000'),
                            (190000, '$190000'),
                            (200000, '$200000'),
                            (210000, '$210000'),
                            (220000, '$220000'),
                            (230000, '$230000'),
                            (240000, '$240000'),
                            (250000, '$250000'),
                            (260000, '$260000'),
                            (270000, '$270000'),
                            (280000, '$280000'),
                            (290000, '$290000'),
                            (300000, '$300000'),
                            (310000, '$310000'),
                            (320000, '$320000'),
                            (330000, '$330000'),
                            (340000, '$340000'),
                            (350000, '$350000'),
                            (360000, '$360000'),
                            (370000, '$370000'),
                            (380000, '$380000'),
                            (390000, '$390000'),
                            (400000, '$400000'),
                            (410000, '$410000'),
                            (420000, '$420000'),
                            (430000, '$430000'),
                            (440000, '$440000'),
                            (450000, '$450000'),
                            (460000, '$460000'),
                            (470000, '$470000'),
                            (480000, '$480000'),
                            (490000, '$490000'),
                            (500000, '$500000'),
                            (510000, '$510000'),
                            (520000, '$520000'),
                            (530000, '$530000'),
                            (540000, '$540000'),
                            (550000, '$550000'),
                            (560000, '$560000'),
                            (570000, '$570000'),
                            (580000, '$580000'),
                            (590000, '$590000'),
                            (600000, '$600000'),
                            (610000, '$610000'),
                            (620000, '$620000'),
                            (630000, '$630000'),
                            (640000, '$640000'),
                            (650000, '$650000'),
                            (660000, '$660000'),
                            (670000, '$670000'),
                            (680000, '$680000'),
                            (690000, '$690000'),
                            (700000, '$700000'),
                            (710000, '$710000'),
                            (720000, '$720000'),
                            (730000, '$730000'),
                            (740000, '$740000'),
                            (750000, '$750000'),
                            (760000, '$760000'),
                            (770000, '$770000'),
                            (780000, '$780000'),
                            (790000, '$790000'),
                            (800000, '$800000'),
                            (810000, '$810000'),
                            (820000, '$820000'),
                            (830000, '$830000'),
                            (840000, '$840000'),
                            (850000, '$850000'),
                            (860000, '$860000'),
                            (870000, '$870000'),
                            (880000, '$880000'),
                            (890000, '$890000'),
                            (900000, '$900000'),
                            (910000, '$910000'),
                            (920000, '$920000'),
                            (930000, '$930000'),
                            (940000, '$940000'),
                            (950000, '$950000'),
                            (960000, '$960000'),
                            (970000, '$970000'),
                            (980000, '$980000'),
                            (990000, '$990000'),
                            (1000000, '$1000000')], 
                            validate_choice=False)

    maxprice = SelectField('Max Price',
                            choices=[('1000000', 'No Max'),
                            (10000, '$10000'),
                            (20000, '$20000'),
                            (30000, '$30000'),
                            (40000, '$40000'),
                            (50000, '$50000'),
                            (60000, '$60000'),
                            (70000, '$70000'),
                            (80000, '$80000'),
                            (90000, '$90000'),
                            (100000, '$100000'),
                            (110000, '$110000'),
                            (120000, '$120000'),
                            (130000, '$130000'),
                            (140000, '$140000'),
                            (150000, '$150000'),
                            (160000, '$160000'),
                            (170000, '$170000'),
                            (180000, '$180000'),
                            (190000, '$190000'),
                            (200000, '$200000'),
                            (210000, '$210000'),
                            (220000, '$220000'),
                            (230000, '$230000'),
                            (240000, '$240000'),
                            (250000, '$250000'),
                            (260000, '$260000'),
                            (270000, '$270000'),
                            (280000, '$280000'),
                            (290000, '$290000'),
                            (300000, '$300000'),
                            (310000, '$310000'),
                            (320000, '$320000'),
                            (330000, '$330000'),
                            (340000, '$340000'),
                            (350000, '$350000'),
                            (360000, '$360000'),
                            (370000, '$370000'),
                            (380000, '$380000'),
                            (390000, '$390000'),
                            (400000, '$400000'),
                            (410000, '$410000'),
                            (420000, '$420000'),
                            (430000, '$430000'),
                            (440000, '$440000'),
                            (450000, '$450000'),
                            (460000, '$460000'),
                            (470000, '$470000'),
                            (480000, '$480000'),
                            (490000, '$490000'),
                            (500000, '$500000'),
                            (510000, '$510000'),
                            (520000, '$520000'),
                            (530000, '$530000'),
                            (540000, '$540000'),
                            (550000, '$550000'),
                            (560000, '$560000'),
                            (570000, '$570000'),
                            (580000, '$580000'),
                            (590000, '$590000'),
                            (600000, '$600000'),
                            (610000, '$610000'),
                            (620000, '$620000'),
                            (630000, '$630000'),
                            (640000, '$640000'),
                            (650000, '$650000'),
                            (660000, '$660000'),
                            (670000, '$670000'),
                            (680000, '$680000'),
                            (690000, '$690000'),
                            (700000, '$700000'),
                            (710000, '$710000'),
                            (720000, '$720000'),
                            (730000, '$730000'),
                            (740000, '$740000'),
                            (750000, '$750000'),
                            (760000, '$760000'),
                            (770000, '$770000'),
                            (780000, '$780000'),
                            (790000, '$790000'),
                            (800000, '$800000'),
                            (810000, '$810000'),
                            (820000, '$820000'),
                            (830000, '$830000'),
                            (840000, '$840000'),
                            (850000, '$850000'),
                            (860000, '$860000'),
                            (870000, '$870000'),
                            (880000, '$880000'),
                            (890000, '$890000'),
                            (900000, '$900000'),
                            (910000, '$910000'),
                            (920000, '$920000'),
                            (930000, '$930000'),
                            (940000, '$940000'),
                            (950000, '$950000'),
                            (960000, '$960000'),
                            (970000, '$970000'),
                            (980000, '$980000'),
                            (990000, '$990000')], 
                            validate_choice=False)

    propertytype = SelectField('Property Type',
                            choices=[('Any', 'Any'),
                            ('Single Family', 'Single Family'), 
                            ('Townhouse', 'Townhouse'), 
                            ('Condo', 'Condo'), 
                            ('Multifamily', 'Multifamily'), 
                            ('House', 'House'), 
                            ('Apartment', 'Apartment')],
                            validate_choice=False)
    num_bed = SelectField('Beds',
                            choices=[(0, 'Any'), (1, '1+'), (1, '2+'), (3, '3+'), (4, '4+')], 
                            validate_choice=False)
    
    num_bath = SelectField('Baths',
                            choices=[(0, 'Any'), (1, '1+'), (2, '2+'), (3, '3+'), (4, '4+')], 
                            validate_choice=False)

    submit = SubmitField('Search')


#class HomeForm inherit from FlaskForm
class HomeForm(FlaskForm):
    home_searchbar = StringField('Search', render_kw={"placeholder": "Enter a 5 digit zipcode"}, validators=[Length(min=5,max=5), Regexp('[0-9]{5}', message="home : Please enter a 5-digit zipcode. For example: 33617"), sqlCheck])

    home_fortype = SelectField('Type',
                            choices=[('Sale', 'Sale'), 
                            ('Rent', 'Rent')],
                            validate_choice=False)
    home_submit = SubmitField('Search')