# game_tools.py
import requests
from typing import List, Dict, Any

FREE_TO_GAME_BASE_URL = "https://www.freetogame.com/api"

def get_free_games_by_filter(platform: str = "pc", genre: str = "shooter", limit: int = 3) -> List[Dict[str, Any]]:
    """
    Retrieves a list of free-to-play games filtered by platform and genre.
    
    Args:
        platform: The platform to filter games by (e.g., 'pc', 'browser'). Defaults to 'pc'.
        genre: The genre or tag to filter games by (e.g., 'shooter', 'rpg', 'strategy'). Defaults to 'shooter'.
        limit: The maximum number of games to return. Defaults to 3. (Max is typically 5).

    Returns:
        A list of dictionaries, each containing the title, genre, and platform 
        for the top available games.
    """
    endpoint = f"{FREE_TO_GAME_BASE_URL}/games"
    params = {
        "platform": platform,
        "category": genre # The API uses 'category' for genre/tag filtering
    }
    
    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        
        data = response.json()
        
        # Format the top results clearly for the LLM
        formatted_results = []
        for item in data[:limit]:
            formatted_results.append({
                "title": item.get("title"),
                "genre": item.get("genre"),
                "platform": item.get("platform"),
                "short_description": item.get("short_description")[:100] + "..."
            })
            
        if not formatted_results:
            return [{"status": "No results found", "query": f"Platform: {platform}, Genre: {genre}"}]
            
        return formatted_results

    except requests.exceptions.RequestException as e:
        return [{"status": "error", "message": f"Could not connect to FreeToGame API: {e}"}]