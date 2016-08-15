# Import flask and template operators
from flask import Flask, render_template

# MongoDB client
from pymongo import MongoClient

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# connect to the database
client = MongoClient(app.config['MONGODB_HOST'],
                     app.config['MONGODB_PORT'])
db = client[app.config['MONGODB_NAME']]


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Import a module / component using its blueprint handler variable
from app.create import *

# Register blueprint(s)
app.register_blueprint(create)


@app.route('/')
def index():
    return render_template('index.html')
