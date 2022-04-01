from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField 
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.models import Buyer, Agent, Property

class CreateBuyerAccountForm(FlaskForm):
    # buyerId = IntegerField('Buyer ID', validators = [DataRequired()]) -> do we need buyer id or is username okay? if so, should this be automatically generated?
    firstName = StringField('First Name', validators = [DataRequired()])
    lastName = StringField('Last Name', validators= [DataRequired()])
    # username = StringField('Username', validators=[DataRequired(),Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters')])
    confPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class CreateAgentAccountForm(FlaskForm):
    firstName = StringField('First Name', validators = [DataRequired()])
    lastName = StringField('Last Name', validators= [DataRequired()])
    # username = StringField('Username', validators=[DataRequired(),Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters')])
    confPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    agentId = IntegerField('Agent ID Number', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    phoneNumber = IntegerField('Phone Number', validators=[DataRequired()])    
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        currEmail = Agent.query.filter_by(agent_email=email.data).first()
        if currEmail:
            raise ValidationError('Email already in use. Please use another email or sign in if you already have an account.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    rememberLogin = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class PropertyForm(FlaskForm):
    # listingId = IntegerField('Listing Id')
    # maybe make sale type a drop down? options are sale/rent? 
    saleType = StringField('Sale Type', validators = [DataRequired()])
    propertyType = StringField('Property Type', validators = [DataRequired()])
    price = IntegerField('Price', validators = [DataRequired()])
    bedrooms = IntegerField('Number of bedrooms', validators = [DataRequired()])
    baths = IntegerField('Number of Bathrooms', validators = [DataRequired()])
    buildingSize = IntegerField('Square footage', validators = [DataRequired()])
    landSize = IntegerField('Acreage', validators = [DataRequired()])
    address = StringField('Address', validators = [DataRequired()])
    # can we automatically assign the agent id to whatever agent is logged in?
    agentId = StringField('Agent ID', validators = [DataRequired()])
    submit = SubmitField('Post Listing')
