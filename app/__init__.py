import os
from flask import Flask
from os.path import join, abspath, dirname
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + join(abspath(dirname(__file__)), "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

text_analytics_key = os.environ["TEXT_ANALYTICS_KEY"]
text_analytics_endpoint = os.environ["TEXT_ANALYTICS_ENDPOINT"]

from app import routes

