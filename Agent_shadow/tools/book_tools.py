# book_tools.py
from google_books_api_wrapper.api import GoogleBooksAPI
from typing import List, Dict, Any

# Initialize the client globally or pass it if you prefer dependency injection
# For the Google Books API, an API key is generally not required for public data searches.
book_client = GoogleBooksAPI()

def search_books_by_title(title_query: str) -> List[Dict[str, Any]]:
    """
    Searches the Google Books database for volumes matching the title query.
    
    Args:
        title_query: The book title or keywords to search for.

    Returns:
        A list of dictionaries, where each dictionary contains the title, 
        authors, and publication year for the top 3 search results.
    """
    try:
        # Use the wrapper to get books by title
        results = book_client.get_book_by_title(title_query).get_all_results()
        
        # Limit and format the output for the LLM
        formatted_results = []
        for book in results[:3]:
            # Extract volume information from the Book object
            volume_info = book._volume_info 
            
            formatted_results.append({
                "title": volume_info.get("title", "N/A"),
                "authors": volume_info.get("authors", ["N/A"]),
                "published_year": volume_info.get("publishedDate", "N/A").split('-')[0] # Get only the year
            })
        
        if not formatted_results:
            return [{"status": "No results found", "query": title_query}]
            
        return formatted_results

    except Exception as e:
        return [{"status": "error", "message": f"An error occurred during the book search: {e}"}]