from flask import render_template, url_for, flash, redirect
from main.forms import CreateAgentAccountForm, CreateBuyerAccountForm, LoginForm, PropertyForm
from main.models import Buyer, Agent, Property
from main import app

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/account")
def account():
    return render_template("account.html") 

@app.route("/create", methods=['GET','POST'])
def create():
    form = PropertyForm()
    return render_template("create.html", form=form)

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/listing")
def listing():
    return render_template("listing.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template("login.html", form = form)

@app.route("/viewing")
def view():
    return render_template("viewing.html")

@app.route("/base")
def base():
    return render_template("base.html")

@app.route("/signup")
def signUp():
    return render_template("signUp.html")

@app.route("/buyersignup", methods=['GET', 'POST'] )
def buyersignup():
    form = CreateBuyerAccountForm()
    return render_template("buyersignup.html", form=form)

@app.route("/agentsignup", methods=['GET', 'POST'])
def agentsignup():
    form = CreateAgentAccountForm()
    return render_template("agentsignup.html", form = form)