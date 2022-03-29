from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from models import Agent, Buyer, User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    username = request.form.get('username')
    password = request.form.get('password')

    # check if user exists
    user = User.query.filter_by(email=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.pw, password):
        return render_template('fail_login.html')
    else:
        # if the above check passes, then we know the user has the right credentials
        login_user(user)
        return redirect(url_for('main.properties'))

@auth.route('/signup_options', methods=['GET', 'POST'])
def signup_options():
  if 'options' in request.form:
    selectedValue = request.form['options']
    return click(selectedValue)

  return render_template('signup.html')

@auth.route('/click')
def click(selectedValue):
    if selectedValue == 'agent':
      return render_template('agent.html')
    elif selectedValue == 'buyer':
      return render_template('buyer.html')
    else:
      return render_template('index.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    if 'agent_form' in request.form:
        agent_fname = request.form.get('agent_fname')
        agent_lname = request.form.get('agent_lname')
        company = request.form.get('company')
        agent_phone = request.form.get('agent_phone')
        agent_email = request.form.get('agent_email')
        agent_pw = generate_password_hash(request.form.get('agent_pw'), method='sha256')

        # if this returns a user, then the email already exists in database
        agent_email_exists = db.session.query(db.exists().where(Agent.email==agent_email)).first()

        # if a user is found, we want to redirect back to signup page so user can try again
        if True in agent_email_exists:
            return render_template('fail_signup.html')
        else:
            new_agent = Agent(agent_fname, agent_lname, agent_email, agent_pw, company, agent_phone)
            db.session.add(new_agent)
    elif 'buyer_form' in request.form:
        buyer_fname = request.form.get('buyer_fname')
        buyer_lname = request.form.get('buyer_lname')
        buyer_email = request.form.get('buyer_email')
        buyer_pw = generate_password_hash(request.form.get('buyer_pw'), method='sha256')
        account_type = 'buyer'

        buyer_email_exists = db.session.query(db.exists().where(Buyer.email==buyer_email)).first()

        if True in buyer_email_exists:
            return render_template('fail_signup.html')
        else:
            new_buyer = Buyer(buyer_fname, buyer_lname, buyer_email, buyer_pw)
            db.session.add(new_buyer)
    
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))