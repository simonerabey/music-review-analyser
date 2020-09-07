# MUSIC SENTIMENT REVIEW
This web app allows users to write music reviews, but the score of each review is calculated by the app based on the sentiment of the review.

## Tech Stack
* HTML
* JavaScript
* Bootstrap
* Flask

## How to Run
Ensure all dependencies are installed. You will need to set the environment variables TEXT_ANALYTICS_KEY and TEXT_ANALYTICS_ENDPOINT to the key and endpoint respectively of an Azure Text Analytics instance. Set environment variable ELASTICSEARCH_URL to 'http://localhost:9200'. Enter command 'flask run' into a bash terminal in the base directory. Access localhost:5000 in a web browser to use the application.