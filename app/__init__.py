from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = False
app.config["ENV"] = "development"
app.config["TESTING"] = False

from app import server
