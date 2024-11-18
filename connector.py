import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify
import numpy as np

# Load pre-trained models (make sure you have saved your models as .pkl files)
scaler = joblib.load('scaler.pkl')  # Load feature scaler if needed
model = joblib.load('model.pkl')  # Load your recommendation model (replace recommendation_model.pkl with model.pkl)

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('frontend.html')  # Serve the HTML page for the recommendation form

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        movie_name = request.form['movie']  # Get the movie name input from the form
        
        # Here you would use your recommendation model to get predictions for the input movie_name
        recommendations = get_movie_recommendations(movie_name)

        return render_template('frontend.html', recommendations=recommendations, movie_name=movie_name)

@app.route('/recommend', methods=['POST'])
def recommend():
    # API endpoint to receive POST request and return movie recommendations as JSON
    try:
        data = request.get_json()
        movie_name = data.get('movie', '')  # Extract the movie name from JSON request

        # Generate recommendations for the given movie name
        recommendations = get_movie_recommendations(movie_name)

        # Format the recommendations as a JSON response
        response = {
            'success': True,
            'recommendations': recommendations
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def get_movie_recommendations(movie_name):
    # Here you will call your recommendation model to generate predictions
    # This is where you'd integrate your logic to query the model

    # For illustration, assume we query the model and get the top 5 recommendations
    # Replace the logic with actual code that fetches recommendations
    try:
        # Simulated logic for demo (Replace this with actual model querying logic)
        # For example, if using collaborative filtering, you would process the `movie_name`
        # and get similar movies using your model and scaling if necessary
        movie_data = pd.read_csv('movies.csv')  # Your dataset of movies

        # This is a placeholder for actual recommendation logic
        similar_movies = movie_data[movie_data['title'].str.contains(movie_name, case=False)]

        if not similar_movies.empty:
            recommendations = similar_movies.head(5).to_dict(orient='records')
        else:
            recommendations = []

        return recommendations
    except Exception as e:
        return [{"error": str(e)}]

if __name__ == '__main__':
    app.run(debug=True)
