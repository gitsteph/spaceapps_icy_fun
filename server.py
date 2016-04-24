from flask import Flask, render_template, request, redirect, flash, session, jsonify

from model import connect_to_db, db, User, UserPath, Photo, AudioVideoRecording, ReportType, Report

import os
import json
import datetime


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

@app.route('/track', methods=["POST"])
def uploadInfo():
	"""" will recieve a JSON with gps data from front-end and saves to DB"""
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
			if report['report'] == "bear":
				rtype = 1
			report_coordinates = {"lat": report['lat'], "lng": report['lng'] }

		
			new_report_entry =  Report(rtype_id=rtype, date_logged=uploaded_datetime, geocoordinates=report_coordinates, user_id=u_id)
		
			db.session.add(new_report_entry)
		db.session.commit()

		return "ok"

###############################################
# Main

if __name__ == '__main__':
	connect_to_db(app)

	app.run(debug=DEBUG, host="0.0.0.0", port=PORT)

