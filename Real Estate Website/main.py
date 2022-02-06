import flask

app = flask.Flask(__name__)

app.config['SECRET_KEY']='12345'


@app.route("/")
def home():
    return flask.render_template("home.html")

@app.route("/account")
def account():
    return flask.render_template("account.html") 

@app.route("/edit")
def edit():
    return flask.render_template("edit.html")

@app.route("/faq")
def faq():
    return flask.render_template("faq.html")

@app.route("/listing")
def listing():
    return flask.render_template("listing.html")

@app.route("/signInOut")
def signInOut():
    return flask.render_template("signInOut.html")

@app.route("/viewing")
def view():
    return flask.render_template("viewing.html")


if __name__ == '__main__':
    app.run()