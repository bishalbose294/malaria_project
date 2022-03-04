from flask import Flask
from flask_cors import CORS
import os

# Create Flask APP
app = Flask(__name__)

# Make it CORS applicable
CORS(app)

# Set parameters
app.config["DEBUG"] = False
app.config["ENV"] = "development"
app.config["TESTING"] = False

# Import API's from server
from app import server