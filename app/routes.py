import requests
from app import app, text_analytics_endpoint, text_analytics_key, models, db
from flask import render_template, request, redirect, url_for, jsonify, g, flash
from app.forms import SearchForm

Review = models.Review

@app.before_request
def before_request():
    db.session.commit()
    g.search_form = SearchForm(meta={"csrf": False}, formdata=request.args)

@app.route('/', methods=['GET', 'POST'])
def index():
    db.create_all()
    if request.method == "POST":
        artist = request.form.get("artist")
        album = request.form.get("album")
        description = request.form.get("description")
        score = get_score(description)
        return render_template("index.html", artist=artist, album=album, description=description, score=score)
    return render_template("index.html", artist="", album="", description="", score="-")

@app.route('/search')
def search():
    if not g.search_form.validate():
        return redirect(url_for("index"))
    results = Review.search(g.search_form.search.data)
    return render_template("search.html", results=results)

@app.route('/publish/', methods=['POST'])
def publish():
    artist = request.form.get("artist")
    album = request.form.get("album")
    description = request.form.get("description")
    score = get_score(description)
    review = Review(artist=artist, album=album, description=description, score=score)
    db.session.add(review)
    db.session.commit()
    return redirect(url_for("show_review", id=review.id))

@app.route('/review/<int:id>', methods=['GET', 'POST'])
def show_review(id):
    review = Review.query.filter_by(id=id)
    r = review.first()
    if r:
        return render_template("review.html", id=id, artist=r.artist, album=r.album, review=r.description, score=r.score)
    flash("Review not found")
    return render_template("review.html")


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
    review = Review.query.filter_by(id=id)
    try:
        db.session.delete(review.first())
        db.session.commit()
        flash("Review successfully deleted")
    except:
        return jsonify({"msg": "Could not delete review"}), 200
    return jsonify({"msg": "Successfully deleted review"}), 204

def get_score(review):
    url = text_analytics_endpoint + "/text/analytics/v3.0/sentiment"
    document = {"documents": [{"id": "1", "language": "en", "text": review}]} 
    headers = {"Ocp-Apim-Subscription-Key": text_analytics_key}
    response = requests.post(url, headers=headers, json=document)
    results = response.json()
    raw_score = results["documents"][0]["confidenceScores"]["positive"]
    return int(raw_score * 100)