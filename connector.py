from flask import Flask, render_template, request, jsonify
import re
import os
import pickle
import pandas as pd
import tensorflow as tf  # For loading .keras model

# Initialize Flask app
app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))

# Path to your dataset and model file
DATASET_PATH = os.path.join(os.getcwd(), 'path_to_your_dataset', 'movies.csv')  # Replace with your dataset path
MODEL_PATH = os.path.join(os.getcwd(), 'path_to_your_model', 'model.keras')  # Replace with your .keras model path
TFIDF_PATH = os.path.join(os.getcwd(), 'path_to_your_tfidf', 'tfidf_vectorizer.pkl')  # Replace with actual path

# Use raw strings to handle backslashes in file paths
movies_data = pd.read_csv(r"D:\neceties\projects\Movie-recommendation-system-final\movies.csv")
recommendation_model = tf.keras.models.load_model(r"D:\neceties\projects\Movie-recommendation-system-final\my_model.keras")

# Ensure the TFIDF file path is correct
TFIDF_PATH = r"D:\neceties\projects\Movie-recommendation-system-final\path_to_your_tfidf\tfidf_vectorizer.pkl"

# Open the TFIDF vectorizer file
with open(TFIDF_PATH, 'rb') as file:
    tfidf_vectorizer = pickle.load(file)

# Route for the home page
@app.route('/')
def index():
    return render_template('frontpage.html')  # Ensure 'frontpage.html' is in the 'templates' folder

# Route to validate SQL query and recommend movies
@app.route('/validate', methods=['POST'])
def validate_query():
    query = request.json.get('query')
    result = {}

    # Basic SQL Injection validation pattern (for demonstration)
    sql_injection_pattern = re.compile(r"(union|select|drop|--|#|\*|insert|update|delete|;|\\)", re.IGNORECASE)

    if sql_injection_pattern.search(query):
        result['safe'] = False
        result['message'] = 'SQL Injection Detected!'
        result['dl_score'] = 0.1  # You can adjust this with real model score
    else:
        result['safe'] = True
        result['message'] = 'SQL Query is Safe.'
        result['dl_score'] = 0.9  # You can adjust this with real model score

    return jsonify(result)

# Route to get movie recommendations
@app.route('/recommend', methods=['POST'])
def recommend_movies():
    """
    Endpoint to recommend movies based on user input.
    Expected input (JSON):
    {
        "movie_name": "The Matrix"
    }
    """
    user_movie = request.json.get('movie_name')  # Replace 'movie_name' based on your request structure
    if not user_movie:
        return jsonify({"error": "No movie name provided"}), 400

    try:
        # Preprocess user input using the TF-IDF vectorizer
        input_data = preprocess_input(user_movie)

        # Get predictions from the model
        predictions = recommendation_model.predict(input_data)

        # Get movie recommendations based on predictions
        recommended_movies = get_recommendations(predictions, movies_data)

        return jsonify({"recommendations": recommended_movies})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define preprocessing function
def preprocess_input(movie_name):
    """
    Transforms the user movie name into a TF-IDF vector.
    """
    if not movie_name:
        raise ValueError("Movie name cannot be empty.")
    return tfidf_vectorizer.transform([movie_name])

# Define recommendation mapping function
def get_recommendations(predictions, dataset):
    """
    Maps model predictions to movie recommendations.
    """
    # Get the top 10 movie indices based on predictions
    sorted_indices = predictions.flatten().argsort()[::-1][:10]

    # Fetch movie details for these indices
    recommended_movies = dataset.iloc[sorted_indices].to_dict(orient='records')

    return recommended_movies

if __name__ == '__main__':
    app.run(debug=True)
