import os
import urllib.parse
from flask import Flask
from os.path import join, abspath, dirname
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + join(abspath(dirname(__file__)), "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

text_analytics_key = os.environ["TEXT_ANALYTICS_KEY"]
text_analytics_endpoint = os.environ["TEXT_ANALYTICS_ENDPOINT"]

es = None
if os.environ["ELASTICSEARCH_URL"]:
    es = Elasticsearch(os.environ["ELASTICSEARCH_URL"])

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from app import routes

