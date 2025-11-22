# lastfm_tools.py
import requests
import os
from typing import List, Dict, Any

# Load the API key from environment variables
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_BASE_URL = "https://ws.audioscrobbler.com/2.0/"
USER_AGENT = "ADKMusicAgent" # Good practice to include a user-agent

def get_top_tracks_global(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieves the current global top tracks chart from Last.fm.
    
    Args:
        limit: The maximum number of tracks to return. Defaults to 5.

    Returns:
        A list of dictionaries, each containing the track title, artist, 
        and listener count for the top global tracks.
    """
    if not LASTFM_API_KEY:
        return [{"status": "error", "message": "Last.fm API Key not found. Please set the LASTFM_API_KEY environment variable."}]

    params = {
        "method": "chart.gettoptracks",
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit
    }
    headers = {'user-agent': USER_AGENT}
    
    try:
        response = requests.get(LASTFM_BASE_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status() # Raise exception for bad status codes
        
        data = response.json()
        tracks_data = data.get('tracks', {}).get('track', [])
        
        # Format the output for the LLM
        formatted_results = []
        for track in tracks_data:
            formatted_results.append({
                "title": track.get("name"),
                "artist": track.get("artist").get("name"),
                "listeners": track.get("listeners")
            })
            
        return formatted_results

    except requests.exceptions.RequestException as e:
        return [{"status": "error", "message": f"Could not connect to Last.fm API: {e}"}]
    except Exception as e:
        return [{"status": "error", "message": f"An unexpected error occurred: {e}"}]