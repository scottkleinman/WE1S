# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from mongokit import Connection

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# connect to the database
connection = Connection(app.config['MONGODB_HOST'],
                        app.config['MONGODB_PORT'])


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Import a module / component using its blueprint handler variable
from app.create import *

# Register blueprint(s)
app.register_blueprint(create)
# app.register_blueprint(xyz_module)
# ..

# register the User document with our current connection
connection.register([PublicationManifest])


@app.route('/')
def index():
    return render_template("index.html")
