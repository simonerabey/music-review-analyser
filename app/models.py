from app import db, search
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    reviews = db.relationship('Review', backref='user')

#Mixin that models a database table where searches can be performed
class Searchable(object):
    '''Performs a search using the given query
    @param query(str): a string consisting of the words to be searched for
    @ret List of results
    '''
    @classmethod
    def search(c, query):
        ids = search.query(c.__tablename__, query)
        if len(ids) == 0:
            return c.query.filter_by(id=0)
        order = []
        for i in range(len(ids)):
            order.append((ids[i], i))
        return c.query.filter(c.id.in_(ids)).order_by(db.case(order, value=c.id))
    
    '''
    Defines actions to be carried out during commit
    @param session: the unit of work that the commit is taking place in
    '''
    @classmethod
    def before_commit(c, session):
        session._changes = {
            "add": list(session.new),
            "update": list(session.dirty),
            "delete": list(session.deleted)
        }

    '''
    Updates the model after a commit has occurred
    @param session: the unit of work that the commit has taken place in
    '''
    @classmethod
    def after_commit(c, session):
        for item in session._changes["add"]:
            if isinstance(item, Searchable):
                search.add(item.__tablename__, item)
        for item in session._changes["update"]:
            if isinstance(item, Searchable):
                search.add(item.__tablename__, item)
        for item in session._changes["delete"]:
            if isinstance(item, Searchable):
                search.delete(item.__tablename__, item)
        session._changes = None

    #Adds records to the index
    @classmethod
    def reindex(c):
        for item in c.query:
            search.add(c.__tablename__, item)

db.event.listen(db.session, "before_commit", Searchable.before_commit)
db.event.listen(db.session, "after_commit", Searchable.after_commit)

class Album(Searchable, db.Model):
    __tablename__ = "album"
    __searchable__ = ["name", "artist"]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    reviews = db.relationship('Review', backref='album')

#Database model of a review
class Review(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    description = db.Column(db.String(2000))
    score = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Review: %r - %r - %r - %d>" % self.album, self.artist, self.description, self.score


