import os
from flask import Flask
from os.path import join, abspath, dirname
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + join(abspath(dirname(__file__)), "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

text_analytics_key = os.environ["TEXT_ANALYTICS_KEY"]
text_analytics_endpoint = os.environ["TEXT_ANALYTICS_ENDPOINT"]

es = None
if os.environ["ELASTICSEARCH_URL"]:
    es = Elasticsearch(os.environ["ELASTICSEARCH_URL"])

from app import routes

