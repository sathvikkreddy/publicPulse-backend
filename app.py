import backend_functions

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get-reviews')
def get_reviews():
    url = request.args.get('url')
    reviews = backend_functions.getReviews(url)
    return jsonify(reviews)

@app.route('/get-verdicts')
def get_verdicts():
    url = request.args.get('url')
    reviews = backend_functions.getReviews(url)
    verdicts = backend_functions.getVerdict(reviews)
    return jsonify(verdicts)

@app.route('/get-ratings')
def get_ratings():
    url = request.args.get('url')
    reviews = backend_functions.getReviews(url)
    ratings = backend_functions.getRating(reviews)
    return jsonify(ratings)

if __name__ == '__main__':
    app.run(debug=True)
