from app import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    album = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    description = db.Column(db.String(2000))
    score = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)
