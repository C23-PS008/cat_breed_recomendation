# Project Name

## Cat Breed Recommender

## Project Description

This project is a recommendation system that recommends cat breeds based on user preferences. The system uses cosine similarity algorithm to match user preferences with the characteristics of cat breeds in the dataset. The cat breed characteristics data is obtained from the `cat_breeds.csv` CSV file. After obtaining the similarity scores, the system provides recommendations for the top 10 cat breeds that best match the user's preferences.

## Usage

1.  Clone this repository to your local machine:

bashCopy code
```
git clone https://github.com/{username}/{repository}.git
```

2.  Navigate to the project directory:

bashCopy code
```
cd {repository}
```

3.  Install the required dependencies:

Copy code
```
pip install -r requirements.txt
```

4.  Make sure the `cat_breeds.csv` file is located in the project directory.
5.  Set the `API_KEY` environment variable with the API key from API-Ninjas:
6.  Run the Flask application:

Copy code
```
python app.py
```

7.  Open a web browser and access the URL `http://localhost:5000` to test the API. You should see the message "Success testing the API!" if the application is running successfully.

8.  To get cat recommendations, use the HTTP POST method to the URL `http://localhost:5000/recommend` by sending user preference data in JSON format. Example:

jsonCopy code
```
{
  "family_friendly": 5,
  "shedding": 3,
  "general_health": 4,
  "playfulness": 4,
  "children_friendly": 4,
  "grooming": 3,
  "intelligence": 4,
  "other_pets_friendly": 3
}
```

9.  The Flask application will respond with JSON containing cat breed recommendations that match the user's preferences.

Project Structure

-   `app.py`: The main file that contains the Flask application code and cat breed recommendation logic.
-   `cat_breeds.csv`: The CSV file that contains the data of cat breed characteristics.
-   `requirements.txt`: The list of dependencies required by the project.
