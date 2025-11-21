import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from datetime import datetime

# Load environment variables at the start of the script
load_dotenv()

@Agent.tool
def get_current_datetime() -> str:
    """Provides the current date, day, and time in a human-readable format. 
    Use this tool whenever the user explicitly asks for the current date or time."""
    now = datetime.now()
    return f"The current date and time is: {now.strftime('%A, %B %d, %Y at %I:%M:%S %p %Z')}"

@Agent.tool
def search_anime(query: str) -> str:
    """Searches the Jikan API for anime based on a user's query. 
    Returns the title, type, and a brief synopsis of the top result."""
    url = "https://api.jikan.moe/v4/anime"
    params = {"q": query, "limit": 1}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data and data.get('data'):
            result = data['data'][0]
            title = result.get('title', 'N/A')
            synopsis = result.get('synopsis', 'No synopsis available.')
            return f"Anime Result: {title}. Type: {result.get('type')}. Synopsis: {synopsis[:150]}..."
        return f"No anime found for '{query}'."
    except requests.RequestException as e:
        return f"Jikan API Error: {e}"

@Agent.tool
def search_movie(title: str) -> str:
    """Searches the OMDb API for movie or TV show details by title. 
    Requires OMDB_API_KEY. Returns the year, rating, and plot summary.
    Use this tool for questions about movies or television series."""
    api_key = os.environ.get("OMDB_API_KEY")
    if not api_key: return "Error: OMDb API key not configured."
    
    url = "http://www.omdbapi.com/"
    params = {"t": title, "apikey": api_key, "plot": "short"}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True":
            return (
                f"Movie/Show: {data.get('Title')} ({data.get('Year')}). "
                f"Rating: {data.get('imdbRating')}. Plot: {data.get('Plot')}"
            )
        return f"Movie/Show '{title}' not found on OMDb."
    except requests.RequestException as e:
        return f"OMDb API Error: {e}"
@Agent.tool
def get_artist_info(artist_name: str) -> str:
    """Retrieves a brief summary of an artist from the Last.fm API. 
    Requires LASTFM_API_KEY. Use this tool for music or artist-related questions."""
    api_key = os.environ.get("LASTFM_API_KEY")
    if not api_key: return "Error: Last.fm API key not configured."
    
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "artist.getinfo",
        "artist": artist_name,
        "api_key": api_key,
        "format": "json"
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get('artist') and data['artist'].get('bio'):
            # Strip HTML/links commonly found in Last.fm summaries
            summary = data['artist']['bio'].get('summary', 'No summary available.').split('<a href')[0].strip()
            return f"Artist Summary: {artist_name}. {summary}"
        return f"Artist '{artist_name}' not found on Last.fm."
    except requests.RequestException as e:
        return f"Last.fm API Error: {e}"
@Agent.tool
def search_books(query: str) -> str:
    """Searches the Google Books API for titles related to the query. 
    Returns the title, author, and description of the top book result. 
    Use this tool for book, author, or publication questions."""
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": query, "maxResults": 1}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get('items'):
            info = data['items'][0]['volumeInfo']
            title = info.get('title', 'N/A')
            authors = ", ".join(info.get('authors', ['Unknown Author']))
            desc = info.get('description', 'No description available.')
            return f"Book Result: {title} by {authors}. Description: {desc[:150]}..."
        return f"No books found for '{query}'."
    except requests.RequestException as e:
        return f"Google Books API Error: {e}"
@Agent.tool
def get_freetogame_list(platform: str) -> str:
    """Retrieves a list of the top free-to-play games for a specific platform. 
    Valid platforms are 'pc' or 'browser'. Returns a list of game titles."""
    if platform.lower() not in ["pc", "browser"]:
        return "Error: Platform must be 'pc' or 'browser'."
    
    url = "https://www.freetogame.com/api/games"
    params = {"platform": platform.lower(), "sort-by": "popularity"}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        titles = [game['title'] for game in data[:5]]
        if titles:
            return f"Top 5 Free-to-Play Games for {platform.upper()}: {', '.join(titles)}"
        return f"No popular free games found for {platform}."
    except requests.RequestException as e:
        return f"FreeToGame API Error: {e}"
@Agent.tool
def search_nearby_places(location: str, place_type: str) -> str:
    """Searches the Google Places API for nearby places (e.g., 'restaurants', 'cafes'). 
    Requires GOOGLE_PLACES_API_KEY. Returns the name and address of the top result.
    Use this for local searches, directions, or business inquiries."""
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not api_key: return "Error: Google Places API key not configured."
    
    # Using the Text Search endpoint
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    query = f"{place_type} near {location}"
    params = {"query": query, "key": api_key}
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get('results'):
            result = data['results'][0]
            name = result.get('name', 'N/A')
            address = result.get('formatted_address', 'Address not found.')
            return f"Top Nearby Result: {name} at {address}"
        return f"No {place_type} found near {location}."
    except requests.RequestException as e:
        return f"Google Places API Error: {e}"

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
# ... (All imports and tool definitions are above this section) ...

def create_multi_tool_agent(tools_list):
    """Creates the ADK Agent with a list of tools."""
    
    # Crucial instruction for the LLM to understand its capabilities
    instruction = (
        "You are a helpful and versatile information agent powered by Gemini. "
        "You have access to specialized tools for movies, music, anime, books, games, "
        "and local places. ALWAYS use the most appropriate tool to answer factual questions. "
        "If the user asks for the current date or time, use that specific tool."
    )

    agent = Agent(
        name="VersatileMultiAPIAgent",
        model=os.environ.get("AGENT_MODEL", "gemini-2.5-flash"),
        instruction=instruction,
        tools=tools_list,  # This is where all your tools are registered
    )
    return agent

async def main():
    # 1. Gather all the tools into a single list
    all_tools = [
        get_current_datetime,
        search_anime,
        search_movie,
        get_artist_info,
        search_books,
        get_freetogame_list,
        search_nearby_places
    ]

    # 2. Initialize the Agent, Session Service, and Runner
    agent = create_multi_tool_agent(all_tools)
    session_service = InMemorySessionService()
    runner = Runner(agent, session_service)

    # 3. Example Query: Test multiple tools in one prompt
    query = "What is the current date, and can you tell me the author of 'Dune' and a popular PC game?"
    print(f"User: {query}\n")

    # 4. Run the conversation and stream the response
    print("--- Agent Response ---")
    async for event in runner.run(user_input=query):
        # ADK events allow you to see the Agent's thought process
        if event.tool_call:
             print(f"**Tool Called:** {event.tool_call.function.name} with arguments: {dict(event.tool_call.function.arguments)}")
        if event.tool_result:
            print(f"**Tool Result:** {event.tool_result.function_response.response[:50]}...")
        if event.text:
            print(event.text)
    print("----------------------")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
