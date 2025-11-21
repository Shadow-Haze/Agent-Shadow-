from google.adk.agents import Agent
from google.adk.tools import google_search # Keep the built-in tool

# --- Import all your custom functions ---
from .api_tools import (
    search_movie_or_series, # OMDB Tool
    search_google_books,    # Google Books Tool (Placeholder)
    get_top_games,          # FreeToGame Tool (Placeholder)
    get_place_details,      # Google Places Tool (Placeholder)
    get_top_tracks          # Last.fm Tool (Placeholder)
)

media_agent = Agent(
    model='gemini-2.5-flash',
    name='media_and_info_agent',
    instruction=(
        "You are a general knowledge and media specialist. "
        "Use the appropriate tool for movies, books, games, music, or places. "
        "Use google_search for all other current events or general facts."
    ),
    # Register ALL tools here
    tools=[
        google_search,
        search_movie_or_series,
        search_google_books,
        get_top_games,
        get_place_details,
        get_top_tracks
    ],
)