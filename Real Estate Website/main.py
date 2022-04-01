from flask import Flask
from flask import request, redirect, url_for, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY']='12345'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/account")
def account():
    return flask.render_template("account.html") 

@app.route("/accountCreation")
def accountCreation():
    return render_template("accountCreation.html")

@app.route("/edit")
def edit():
    return render_template("edit.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/listing")
def listing():
    return render_template("listing.html")

@app.route("/signInOut", methods=["POST","GET"])
def signInOut():
    if request.method == "POST":
        user = request.form["nm"]
        session["user"] = user
        flash("Logged in!")

        return redirect(url_for('home'))
    else:
        return render_template("signInOut.html")

@app.route("/viewing")
def view():
    return render_template("viewing.html")

@app.route("/post")
def post():
    return render_template("post.html")

if __name__ == '__main__':
    app.run(debug=True)