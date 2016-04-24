"""Models and database functions"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import os


db = SQLAlchemy()

#### TODO:  Complete __repr__ methods ####

####################################################################
#Model definitions


class User(db.Model):
	"""User of site.  Includes superusers."""

	__tablename__ = "users"

	id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
	email = db.Column(db.String(40), nullable=False, unique=True)
	name = db.Column(db.String(40), nullable=False)
	password = db.Column(db.String(40), nullable=False)
	superuser_status = db.Column(db.Boolean, nullable=False, default=False)
	created_at = db.Column(db.DateTime, nullable=False)
	updated_at = db.Column(db.DateTime, nullable=False)

	def __repr__(self):
		"""Helpful representation when printed."""
		return "< User id=%s Name=%s >" % (self.id, self.name)


class UserPath(db.Model):
	"""GPS paths for each trip a user takes."""

	__tablename__ = "userpaths"

	id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	gps_path = db.Column(JSON, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False)


class Photo(db.Model):
	"""Photos (ptrs to AWS) -- can be connected to specific userpaths."""

	__tablename__ = "photos"

	id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
	photo_ptr = db.Column(db.String, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False)
	geocoordinates = db.Column(JSON)
	public = db.Column(db.Boolean, nullable=False, default=True)
	userpath_id = db.Column(db.Integer, db.ForeignKey('userpaths.id'), nullable=True)


class AudioVideoRecording(db.Model):
	"""Audio & video recording ptrs -- can be connected to userpaths."""

	__tablename__ = "recordings"

	id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
	recording_ptr = db.Column(db.String, nullable=False)
	start_dt = db.Column(db.DateTime, nullable=False)
	end_dt = db.Column(db.DateTime, nullable=False)
	public = db.Column(db.Boolean, nullable=False, default=False)
	userpath_id = db.Column(db.Integer, db.ForeignKey('userpaths.id'), nullable=True)


class ReportType(db.Model):
	"""Types of events, like bears, holes, cracks, etc."""

	__tablename__ = "reporttypes"

	id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
	rtype = db.Column(db.String, nullable=False)


class Report(db.Model):
	"""Logs of actual reports made."""

	__tablename__ = "reports"

	id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
	rtype_id = db.Column(db.Integer, db.ForeignKey('reporttypes.id'), nullable=False)
	date_logged = db.Column(db.DateTime, nullable=False)
	geocoordinates = db.Column(JSON)
	public = db.Column(db.Boolean, nullable=False, default=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


##############################################################################
# Helper functions for flask app

def connect_to_db(app):
	"""Connect the database to our Flask app."""

	# Configure to use postgresql database depending on if it's deployed or local
	DATABASE_URL = os.environ.get("DATABASE_URL", 'postgresql://test@localhost:5432/icyfun')

	app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

	db.app = app
	db.init_app(app)

if __name__ == "__main__":
	# As a convenience, if we run this module interactively, it will leave
	# you in a state of being able to work with the database directly.

	from server import app
	connect_to_db(app)
	print "Connected to DB."
