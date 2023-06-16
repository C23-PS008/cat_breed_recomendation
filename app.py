import pickle
import pandas as pd
import requests
import os

from flask import Flask, jsonify, request
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv


app = Flask(__name__)

# Load the cat breeds data
data = pd.read_csv('cat_breeds.csv')

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv('API_KEY')

# Initialize the similarity matrix
similarity_matrix = None

@app.route('/')
def index():
    try:
        hello_json = {
            'status_code': 200,
            'message': 'Success testing the API!',
            'data': [],
        }
        return jsonify(hello_json)
    except Exception as e:
        error_json = {
            'status_code': 500,
            'message': 'Error occurred.',
            'error_details': str(e),
        }
        return jsonify(error_json), 500


@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Get user ratings from the request
        user_ratings = request.get_json()

        # Append user ratings to the DataFrame
        user_ratings_df = pd.DataFrame(user_ratings, index=[0])
        df_join = pd.concat([data, user_ratings_df], ignore_index=True)

        # Compute the similarity matrix
        global similarity_matrix
        similarity_matrix = cosine_similarity(df_join[['family_friendly', 'shedding', 'general_health', 'playfulness', 'children_friendly', 'grooming', 'intelligence', 'other_pets_friendly']])

        user_index = df_join.shape[0] - 1
        similar_kitten_index = similarity_matrix[user_index].argsort()[:-1][::-1]
        
        similarities = similarity_matrix[user_index][similar_kitten_index]

        top_five_cats = df_join.loc[similar_kitten_index[:5]]

        # Get the top 10 recommended cat breeds with characteristics, similarity scores, and breed images
        recommended_cat_breeds = []
        for idx in top_five_cats.index:
            if idx < len(similarities):  # Check if idx is within the valid range
                cat_breed = {
                    "breed": df_join.loc[idx, 'name'],
                    "length": df_join.loc[idx, 'length'],
                    "origin": df_join.loc[idx, 'origin'],
                    "min_life_expectancy": df_join.loc[idx, 'min_life_expectancy'],
                    "max_life_expectancy": df_join.loc[idx, 'max_life_expectancy'],
                    "min_weight": df_join.loc[idx, 'min_weight'],
                    "max_weight": df_join.loc[idx, 'max_weight'],
                    "family_friendly": int(df_join.loc[idx, 'family_friendly']),
                    "shedding": int(df_join.loc[idx, 'shedding']),
                    "general_health": int(df_join.loc[idx, 'general_health']),
                    "playfulness": int(df_join.loc[idx, 'playfulness']),
                    "children_friendly": int(df_join.loc[idx, 'children_friendly']),
                    "grooming": int(df_join.loc[idx, 'grooming']),
                    "intelligence": int(df_join.loc[idx, 'intelligence']),
                    "other_pets_friendly": int(df_join.loc[idx, 'other_pets_friendly']),
                    "similarity_score": float(similarities[idx])
                }
                breed_image = retrieve_breed_image(cat_breed["breed"])

                cat_breed["breed_image"] = breed_image

                recommended_cat_breeds.append(cat_breed)
        
        # # Sort the recommended cat breeds by similarity score in descending order
        recommended_cat_breeds = sorted(recommended_cat_breeds, key=lambda x: x['similarity_score'], reverse=True)

        return jsonify(recommendations=recommended_cat_breeds)

    except Exception as e:
        error_json = {
            'status_code': 500,
            'message': 'Error occurred during prediction.',
            'error_details': str(e),
        }
        return jsonify(error_json), 500

def retrieve_breed_image(breed_name):
    api_url = 'https://api.api-ninjas.com/v1/cats?name={}'.format(breed_name)
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    breed_data = response.json()
    if breed_data:
        breed_image_url = breed_data[0]['image_link']  # Use index [0] to access the first item in the list
        return breed_image_url
    return ''        

if __name__ == '__main__':
    app.run()
