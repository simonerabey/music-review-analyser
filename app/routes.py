import requests
from app import app, text_analytics_endpoint, text_analytics_key, models, db
from flask import render_template, request, redirect, url_for

Review = models.Review

@app.route('/', methods=['GET', 'POST'])
def index():
    db.create_all()
    if request.method == "POST":
        description = request.form.get("description")
        score = get_score(description)
        return render_template("index.html", score=score)
    return render_template("index.html", score="-")

@app.route('/review/', methods=['GET', 'POST'])
def show_review():
    artist = request.form.get("artist")
    album = request.form.get("album")
    description = request.form.get("description")
    score = get_score(description)
    review = Review(artist=artist, album=album, description=description, score=score)
    db.session.add(review)
    db.session.commit()
    return render_template("review.html", artist=artist, album=album, review=description, score=score)

#@app.route('/search/', methods=['POST'])
#def search():
    #pass

def get_score(review):
    url = text_analytics_endpoint + "/text/analytics/v3.0/sentiment"
    document = {"documents": [{"id": "1", "language": "en", "text": review}]} 
    headers = {"Ocp-Apim-Subscription-Key": text_analytics_key}
    response = requests.post(url, headers=headers, json=document)
    results = response.json()
    raw_score = results["documents"][0]["confidenceScores"]["positive"]
    return int(raw_score * 100)