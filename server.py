from flask import Flask, render_template, request, redirect, flash, session, jsonify

from model import connect_to_db, db, User, UserPath, Photo, AudioVideoRecording, ReportType, Report

import os
import json
import datetime

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
def register_user():
	if request.method == 'POST':
		"""Processes new user registration."""

		# Requests information provided by the user from registration form.
		value_types = ["email", "name"]
		values_dict = {val:request.form.get(val) for val in value_types}
		values_dict["created_at"] = datetime.datetime.now()
		values_dict["updated_at"] = values_dict["created_at"]
		values_dict["superuser_status"] = False
		unhashed_pw = request.form.get("password")
		password = generate_password_hash(unhashed_pw)  # hashes and salts pw
		values_dict["password"] = password

		# Queries "users" table in database to determine whether user already has an account.
		# If the user has an account, the user is redirected to login page.
		# Otherwise, a new account is created and the user is logged in via the session.
		user_object = User.query.filter(User.email == values_dict["email"]).first()
		if user_object:
			flash('account exists')
			return redirect("/")
		else:
			new_user = User(**values_dict)
			db.session.add(new_user)
			db.session.commit()
			user_object = User.query.filter(User.email == values_dict["email"]).first()
			session['user_id'] = user_object.id

		return redirect("/")


@app.route('/user_profile/delete', methods=['POST'])
def delete_user_profile():
	"""Deletes user profile and returns to home page, logged out."""
	db.session.delete(User.query.filter(User.id == session["user_id"]).first())
	db.session.commit()
	flash('Your account has been deleted.')
	return redirect("/logout")


@app.route('/user_profile/update', methods=['POST'])
def update_user_profile():
	"""AJAX route to update user profile from modal."""

	value_types = ["email", "password", "name"]
	values_dict = {val:request.form.get(val) for val in value_types}

	values_dict["updated_at"] = datetime.datetime.now()
	values_dict = {k:v for k,v in values_dict.iteritems() if v}

	ind_update = update(User.__table__).where(User.id == session['user_id']).values(**values_dict)
	db.session.execute(ind_update)
	db.session.commit()
	return "Your user profile has been updated."


#### ADD TO MAP/PATH WHEN ONLINE

#### STORE IN AWS S3

def gen_fake_reports(lat, lng, range, num):
    random.seed(1) # for consistent fake data
    things = ['bear', 'hole', 'ice']
    return [{'lat': lat+random.uniform(-range,range), 'lng': lng+random.uniform(-range,range), 'message': random.choice(things)} for i in xrange(num)]

@app.route('/track', methods=['GET', 'POST'])
def track():
	if request.method == "GET":
	    fake_reports = gen_fake_reports(65, 165, 1, 20)
	    return render_template('track.html', reports=fake_reports)
	
	if request.method == "POST":
		# get the JSON object with lat/long tracking data
		info_json = request.get_json()
		
		path_info = info_json['path'] 
		#list of coordinates - i.e. [{u'lat': 65.5, u'lng': 165.6}, {u'lat': 65.5, u'lng': 165.7}, {u'lat': 65.5, u'lng': 165.9}]
		
		# get user id from session
		u_id = session.get("user_id", 1)

		# get current datetime
		uploaded_datetime = datetime.datetime.now()

		new_tracking_entry = UserPath(user_id=u_id, gps_path=path_info, created_at=uploaded_datetime)
		db.session.add(new_tracking_entry)
		# list of reports made
		reports_info = info_json['reports']
		# go thru each report and grab the report made and coordinates
		for report in reports_info:
			# TODO: Change this so that instead of recieving text (i.e. "bear") of the type of report, we get the id to match what we have in db
			if report['message'] == "bear":
				rtype = 1
			elif report['message'] == "hole":
				rtype = 2
			elif report['message'] == "thin ice":
				rtype = 3
			report_coordinates = {"lat": report['lat'], "lng": report['lng'] }

		
			new_report_entry =  Report(rtype_id=rtype, date_logged=uploaded_datetime, geocoordinates=report_coordinates, user_id=u_id)
		
			db.session.add(new_report_entry)
		db.session.commit()

		return "ok"


###############################################
# Main

if __name__ == '__main__':
	connect_to_db(app)

	app.run(debug=DEBUG, host="0.0.0.0", port=PORT, ssl_context='adhoc')

