import backend_functions

# Example usage of the getReviews function
reviews = backend_functions.getReviews('https://www.yelp.com/biz/mejico-sydney-2')

# Example usage of the getVerdict function
verdicts = backend_functions.getVerdict(reviews)

# Example usage of the getRating function
ratings = backend_functions.getRating(reviews)

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/get-reviews')
def get_reviews():
    reviews = backend_functions.getReviews('https://www.yelp.com/biz/mejico-sydney-2')
    return jsonify(reviews)

@app.route('/get-verdicts')
def get_verdicts():
    reviews = backend_functions.getReviews('https://www.yelp.com/biz/mejico-sydney-2')
    verdicts = backend_functions.getVerdict(reviews)
    return jsonify(verdicts)

@app.route('/get-ratings')
def get_ratings():
    reviews = backend_functions.getReviews('https://www.yelp.com/biz/mejico-sydney-2')
    ratings = backend_functions.getRating(reviews)
    return jsonify(ratings)

if __name__ == '__main__':
    app.run(debug=True)
