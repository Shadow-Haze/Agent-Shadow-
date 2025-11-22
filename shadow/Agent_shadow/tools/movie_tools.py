# movie_tools.py
import requests
import os
from typing import Dict, Any

# Load the API key from environment variables
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_BASE_URL = "http://www.omdbapi.com/"

def get_movie_details(title: str, year: str = "") -> Dict[str, Any]:
    """
    Retrieves detailed information for a movie or TV show by title.

    Args:
        title: The exact title of the movie or TV show to search for.
        year: The year of release to help find the correct match (optional).

    Returns:
        A dictionary containing the title, year, plot, director, and IMDb rating, 
        or an error message.
    """
    if not OMDB_API_KEY:
        return {"status": "error", "message": "OMDb API Key not found. Please set the OMDB_API_KEY environment variable."}

    params = {
        "apikey": OMDB_API_KEY,
        "t": title, # Search by title
        "y": year,  # Filter by year (if provided)
        "plot": "short", # Keep plot concise
        "r": "json"
    }
    
    try:
        # Use GET to request data
        response = requests.get(OMDB_BASE_URL, params=params, timeout=10)
        response.raise_for_status() # Raise exception for bad status codes
        
        data = response.json()
        
        if data.get("Response") == "True":
            # Format the output clearly for the LLM
            return {
                "title": data.get("Title"),
                "year": data.get("Year"),
                "director": data.get("Director"),
                "actors": data.get("Actors"),
                "genre": data.get("Genre"),
                "imdb_rating": data.get("imdbRating"),
                "plot": data.get("Plot")
            }
        else:
            return {"status": "error", "message": f"Movie/Series '{title}' not found. Error: {data.get('Error')}"}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Could not connect to OMDb API: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {e}"}