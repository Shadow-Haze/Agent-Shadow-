import requests
import os
from typing import Dict, Any

# Ensure OMDB_API_KEY is set in your environment variables
OMDB_KEY = os.environ.get("OMDB_API_KEY")
OMDB_URL = "http://www.omdbapi.com/"

def search_movie_or_series(title: str, media_type: str = "movie") -> Dict[str, Any]:
    """
    Searches the OMDb API for movie or series information.

    Use this tool when the user asks for details (plot, cast, score, year)
    about a specific movie or TV series.

    Args:
        title: The name of the movie or series to search for (e.g., "Inception").
        media_type: The type of media to search for. Can be 'movie' or 'series'.

    Returns:
        A dictionary containing the title, year, plot, and IMDb rating.
        Returns an error dictionary if the request fails or no result is found.
    """
    if not OMDB_KEY:
        return {"error": "OMDB_API_KEY is not configured."}

    try:
        response = requests.get(
            OMDB_URL,
            params={"t": title, "type": media_type, "apikey": OMDB_KEY}
        )
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "True":
            return {
                "Title": data.get("Title"),
                "Year": data.get("Year"),
                "Plot": data.get("Plot"),
                "IMDb_Rating": data.get("imdbRating")
            }
        else:
            return {"error": f"OMDB search failed: {data.get('Error', 'No result found.')}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"API request error: {e}"}
    
    
JIKAN_API_URL = "https://api.jikan.moe/v4"

def search_anime(query: str) -> List[Dict[str, Any]]:
    """
    Searches for anime titles on MyAnimeList using the Jikan API.

    Use this tool when the user asks for information about a specific anime,
    like its ID, title, score, or synopsis.

    Args:
        query: The name of the anime to search for (e.g., "Attack on Titan").

    Returns:
        A list of search results, where each result is a dictionary containing
        the anime's 'mal_id', 'title', 'score', and 'synopsis'.
    """
    try:
        url = f"{JIKAN_API_URL}/anime"
        response = requests.get(url, params={"q": query})
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

        data = response.json()
        results = []
        # Process the results to return only the most relevant, structured data
        for item in data.get("data", [])[:3]: # Limit to top 3 results
            results.append({
                "mal_id": item.get("mal_id"),
                "title": item.get("title"),
                "score": item.get("score"),
                "synopsis": item.get("synopsis", "")[:200] + "..." # Truncate for brevity
            })
        return results
    except requests.exceptions.RequestException as e:
        return [{"error": f"Failed to connect to Jikan API: {e}"}]
    except Exception as e:
        return [{"error": f"An unexpected error occurred: {e}"}]