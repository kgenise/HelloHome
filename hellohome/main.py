# IMPORTING FLASK CLASS
from flask import Flask, render_template, url_for


# APP VARIABLE AND SET INSTANCE TO FLASK CLASS
# __name__ SPECIAL VARIABLE IN PYTHON - JUST NAME OF MODULE (= MAIN) RUNS
app = Flask(__name__)

# DATABASE CALL RETURNED
posts = [
	{
		'author' : 'Corey',
		'title': 'Blog Post 1',
		'content': 'First post content',
		'date-posted': 'April 20, 2018'
	},
	{
		'author' : 'Jane',
		'title': 'Blog Post 2',
		'content': 'Second post content',
		'date-posted': 'April 21, 2018'
	}
]

# ROUTES ARE WHAT TYPE INTO BROWSER TO GO TO DIFFERENT PAGES
# ROUTE DECORATORS - ADD ADITIONAL FUNCTIONALITY TO EXISTING FUNCTIONS
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/search")
def search():
    return render_template('search.html')

@app.route("/home_id1")
def home_id1():
    return render_template('home_id1.html')

@app.route("/manageproperties")
def manageproperties():
    return render_template('manageproperties.html')

@app.route("/faq")
def faq():
    return render_template('faq.html')

@app.route("/signin")
def signin():
    return render_template('signin.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/user_landing_mysavedproperties")
def user_landing_mysavedproperties():
    return render_template('user_landing_mysavedproperties.html')

@app.route("/user_accountsettings")
def user_accountsettings():
    return render_template('user_accountsettings.html')

@app.route("/agent_landing_mypostedproperties")
def agent_landing_mypostedproperties():
    return render_template('agent_landing_mypostedproperties.html')

@app.route("/agent_postaproperty")
def agent_postaproperty():
    return render_template('agent_postaproperty.html')


@app.route("/agent_accountsettings")
def agent_accountsettings():
    return render_template('agent_accountsettings.html')

@app.route("/agent_editaproperty")
def agent_editaproperty():
    return render_template('agent_editaproperty.html')


if __name__ == '__main__':
	app.run(debug=True)