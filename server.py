from flask import Flask, render_template, request, redirect, flash, session, jsonify

from model import connect_to_db, db
from speech_transcribe import convert_to_wav, speech_converter

import os


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
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
	# 
	return render_template('home.html')

@app.route('/upload', methods= ['GET', 'POST'])
def upload_file():
	""" Ideally this route wout take in an uploaded file and convert it to a WAV file and then convert to speech to text"""
	
	if request.method == 'POST':
		f = request.files['file']
		session['audio_file'] = f.filename
		f.save('./uploads/'+f.filename)
		new_file = convert_to_wav(f.filename, session.get('audio_file', 'tmp'))

		# speech_converter('./uploads/{}.flac'.format(session.get('audio_file').split('.')[0]))
		return '200. Uploaded files'
	else:
		return 'Upload Page'





###############################################
# Main

if __name__ == '__main__':
	connect_to_db(app)
	app.run(debug=DEBUG, host="0.0.0.0", port=PORT)