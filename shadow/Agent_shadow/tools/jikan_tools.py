# jikan_tools.py
from jikanpy import Jikan
from typing import List, Dict, Any

jikan = Jikan()

def search_anime(query: str) -> List[Dict[str, Any]]:
    """
    Searches for anime titles based on a user's query.

    Args:
        query: The title or keywords to search for.

    Returns:
        A list of dictionaries, where each dictionary contains the title, 
        mal_id, and synopsis for the top search results.
    """
    try:
        results = jikan.search('anime', query)['results'][:3] # Get top 3
        
        # Format the output clearly for the LLM
        formatted_results = []
        for item in results:
            formatted_results.append({
                "title": item.get("title"),
                "mal_id": item.get("mal_id"),
                "synopsis": item.get("synopsis", "No synopsis available")[:150] + "..."
            })
        return formatted_results

    except Exception as e:
        return [{"error": f"Could not perform Jikan search: {e}"}]

# You can add other functions like get_top_anime, get_character_info, etc.
# ...