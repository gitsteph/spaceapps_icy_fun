"""Models and database functions"""

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.dialects.postgresql import JSON

import psycopg2, os



db = SQLAlchemy()


####################################################################
#Model definitions

# class Users(db.Model):
	# pass

##############################################################################
# Helper functions for flask app

def connect_to_db(app):
	"""Connect the database to our Flask app."""

	# Configure to use postgresql database depending on if it's deployed or local
	DATABASE_URL = os.environ.get("DATABASE_URL", 'postgresql://test@localhost:5432/icyfun')

	app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	db.app = app
	db.init_app(app)

if __name__ == "__main__":
	# As a convenience, if we run this module interactively, it will leave
	# you in a state of being able to work with the database directly.

	from server import app
	connect_to_db(app)
	print "Connected to DB."

