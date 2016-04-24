from flask import Flask, render_template, request, redirect, flash, session, jsonify
<<<<<<< HEAD

from model import connect_to_db, db

=======
from model import connect_to_db, db, User, UserPath, Photo, AudioVideoRecording, ReportType, Report
>>>>>>> d31f5ac80cabbbefcce39a0559e6775077c97340
import os


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


###############################################
# Main

if __name__ == '__main__':
	connect_to_db(app)
<<<<<<< HEAD
	app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
=======
	app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
>>>>>>> d31f5ac80cabbbefcce39a0559e6775077c97340
