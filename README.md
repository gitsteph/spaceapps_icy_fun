# spaceapps_icy_fun
SpaceApps Challenge Submission 042316

# Running the server locally:

## Setup:

From the terminal in the project directory, run:

1. `pip install virtualenv`
2. `virtualenv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`

## Setup the DB:

1. Open (or install) postgres (there should be an elephant in your toolbar) (http://postgresapp.com/)
2. After opening postgres on your mac, press the `open psql` button
3. Create the user by entering `CREATE USER HBspaceapps;`
5. Create the database by entering `CREATE DATABASE icyfun;`
6. Grant privileges on the DB by entering: `GRANT ALL PRIVILEGES ON DATABASE icyfun to HBspaceapps;`

## Run the server locally:

1. Run `python server.py`

## Access the page:

1. Once the server is running, navigate to: http://0.0.0.0:5000/

## 
