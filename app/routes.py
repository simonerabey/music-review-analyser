import requests
from app import app, request, text_analytics_endpoint, text_analytics_key
from flask import render_template

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/publish/', methods=['POST'])
def publish():
    artist = request.form.get("artist")
    album = request.form.get("album")
    description = request.form.get("description")
    score = get_score(description)

def get_score(review):
    url = text_analytics_endpoint + "/text/analytics/v3.0/sentiment"
    document = {"documents": [{"id": "1", "language": "en", "text": review}]} 
    headers = {"Ocp-Apim-Subscription-Key": text_analytics_key}
    response = requests.post(url, headers=headers, json=document)
    results = response.json()
    raw_score = results["documents"][0]["confidenceScores"]["positive"]
    return int(raw_score * 100)