from flask import Flask, render_template, request, redirect, flash, session, jsonify
from model import connect_to_db, db, User, UserPath, Photo, AudioVideoRecording, ReportType, Report
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
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
