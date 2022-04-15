from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    # check if the user exists
    # hash the user-supplied password and compare it to the hashed password in the database
    user = User.query.filter_by(email=username).first()
    if not user or not check_password_hash(user.pw, password):
        return render_template('fail_login.html')
    else:
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
    if 'agent_form' in request.form:
        fname = request.form.get('agent_fname')
        lname = request.form.get('agent_lname')
        company = request.form.get('company')
        phone = request.form.get('agent_phone')
        email = request.form.get('agent_email')
        pw = generate_password_hash(request.form.get('agent_pw'), method='sha256')
        account_type = 'agent'

        # if this returns true, then the email already exists in database
        agent_email_exists = db.session.query(db.exists().where(User.email==email)).first()

        if True in agent_email_exists:
            return render_template('fail_signup.html')
        else:
            new_agent = User(account_type, fname, lname, email, pw, company, phone)
            db.session.add(new_agent)
    elif 'buyer_form' in request.form:
        fname = request.form.get('buyer_fname')
        lname = request.form.get('buyer_lname')
        email = request.form.get('buyer_email')
        pw = generate_password_hash(request.form.get('buyer_pw'), method='sha256')
        account_type = 'buyer'

        buyer_email_exists = db.session.query(db.exists().where(User.email==email)).first()

        if True in buyer_email_exists:
            return render_template('fail_signup.html')
        else:
            new_buyer = User(account_type, fname, lname, email, pw)
            db.session.add(new_buyer)
    
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))