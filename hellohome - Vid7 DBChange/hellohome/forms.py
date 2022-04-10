from ast import Pass
from tokenize import String
from xml.dom import ValidationErr
from xmlrpc.client import Boolean
from flask_wtf import FlaskForm

#FileField(type of field allowed) & FileAllowed(validator of file type - jpg,png)
from flask_wtf.file import FileField, FileAllowed

#import current_user to ensure UpdateAccount validation checks only if first_name-last_name/email changed
from flask_login import current_user

from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# need for validating first_name-last_name/email
from hellohome.models import User

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