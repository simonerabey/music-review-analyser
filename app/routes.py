import requests
from app import app, text_analytics_endpoint, text_analytics_key, models, db
from flask import render_template, request, redirect, url_for, jsonify, g, flash
from app.forms import SearchForm
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

Review = models.Review

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    if User.query.filter_by(email=email).first():
        flash('Email address already in use')
        return redirect(url_for('signup'))

    if User.query.filter_by(username=username).first():
        flash('Username taken')
        return redirect(url_for('signup'))
    
    user = User(username=username, password=generate_password_hash(password, method='sha256'), email=email)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        flash('Login details incorrect')
        return redirect(url_for(login))
    login_user(user)
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#Tasks performed before a request is carried out
@app.before_request
def before_request():
    db.session.commit()
    g.search_form = SearchForm(meta={"csrf": False}, formdata=request.args)

#Logic for main page consisting of the review form
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    db.create_all()
    if request.method == "POST":
        artist = request.form.get("artist")
        album = request.form.get("album")
        description = request.form.get("description")
        score = get_score(description)
        return render_template("index.html", artist=artist, album=album, description=description, score=score)
    return render_template("index.html", artist="", album="", description="", score="-")

#Displays page that shows search results
@app.route('/search')
def search():
    if not g.search_form.validate():
        return redirect(url_for("index"))
    results = Review.search(g.search_form.search.data)
    return render_template("search.html", results=results)

#Publishes a review
@app.route('/publish/', methods=['POST'])
@login_required
def publish():
    artist = request.form.get("artist")
    album = request.form.get("album")
    description = request.form.get("description")
    score = get_score(description)
    user_id = current_user.id
    review = Review(artist=artist, album=album, description=description, score=score, user_id=user_id)
    db.session.add(review)
    db.session.commit()
    return redirect(url_for("show_review", id=review.id))

'''Displays a review
@param id: the id of the review in the database
'''
@app.route('/review/<int:id>', methods=['GET', 'POST'])
def show_review(id):
    review = Review.query.filter_by(id=id)
    r = review.first()
    if r:
        author = User.query.filter_by(id=r.user_id).first().username
        return render_template("review.html", id=id, artist=r.artist, album=r.album, review=r.description, score=r.score, author=author)
    flash("Review not found")
    return render_template("review.html")

'''Deletes a review
@param id: the id of the review to be deleted from the database
'''
@app.route("/delete/<int:id>", methods=["DELETE"])
@login_required
def delete(id):
    review = Review.query.filter_by(id=id)
    try:
        db.session.delete(review.first())
        db.session.commit()
        flash("Review successfully deleted")
    except:
        return jsonify({"msg": "Could not delete review"}), 200
    return jsonify({"msg": "Successfully deleted review"}), 204

'''
Calculates the score of a review
@param review: the description of the review
@ret score of the review out of 100
'''
def get_score(review):
    url = text_analytics_endpoint + "/text/analytics/v3.0/sentiment"
    document = {"documents": [{"id": "1", "language": "en", "text": review}]} 
    headers = {"Ocp-Apim-Subscription-Key": text_analytics_key}
    response = requests.post(url, headers=headers, json=document)
    results = response.json()
    raw_score = results["documents"][0]["confidenceScores"]["positive"]
    return int(raw_score * 100)