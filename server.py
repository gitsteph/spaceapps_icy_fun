from flask import Flask, render_template, request, redirect, flash, session, jsonify

from model import connect_to_db, db, User, UserPath, Photo, AudioVideoRecording, ReportType, Report

import os
import random
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "ABCDEF")
app.secret_key = SECRET_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

PORT = int(os.environ.get("PORT", 5000))
#set debug-mode to false for deployed version but true locally
DEBUG = "NO_DEBUG" not in os.environ

###############################################
# Routes

@app.route('/')
def home():
	return render_template('home.html')


# Helper function to check whether user is logged in.
def confirm_loggedin():
    user_id = session.get("user_id")
    if not user_id:
        print "redirected"
        return None
    else:
        user_obj = User.query.filter(User.id == user_id).first()
    return user_obj


@app.route('/login', methods=['POST'])
def login():
	email = request.form.get("name")
	password = request.form.get("password")

	# Queries "users" table in database to determine whether the user already has an account.
	# If the user has an account, the user's account information and password are verified.
	user_object = User.query.filter(User.email == email).first()
	if user_object:
		if check_password_hash(user_object.password, password):
			session['user_id'] = user_object.id

			flash("Logged in")
			return redirect("/")  # dashboard
		else:
			flash('wrong password')
			return redirect("/")  # login page
	else:
		flash('no such user')
		return redirect("/")


@app.route('/logout', methods=['POST'])
def logout():
	"""Log out."""
	del session['user_id']
	flash("Logged out.")
	return redirect('/')


@app.route('/register', methods=['POST'])
def register():
	pass

def gen_fake_reports(lat, lng, range, num):
    random.seed(1) # for consistent fake data
    things = ['bear', 'hole', 'ice']
    return [{'lat': lat+random.uniform(-range,range), 'lng': lng+random.uniform(-range,range), 'message': random.choice(things)} for i in xrange(num)]

@app.route('/track', methods=['GET'])
def track():
    fake_reports = gen_fake_reports(65, 165, 1, 20)
    return render_template('track.html', reports=fake_reports)

###############################################
# Main

if __name__ == '__main__':
	connect_to_db(app)

	app.run(debug=DEBUG, host="0.0.0.0", port=PORT, ssl_context='adhoc')

