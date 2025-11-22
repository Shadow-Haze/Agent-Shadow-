import os
from dotenv import load_dotenv
load_dotenv()
from google.adk.agents.llm_agent import Agent
from tools.jikan_tools import search_anime
from tools.book_tools import search_books_by_title
from tools.game_tools import get_free_games_by_filter
from tools.lastfm_tools import get_top_tracks_global
from tools.movie_tools import get_movie_details

# Define the Root Agent
ROOT_AGENT = Agent(
    name="Shadow",
    model="models/gemini-2.5-flash", 
    description="A versatile assistant capable of answering questions about anime, music, movies, books, video games.",
    instructions=(
        "You are an all-knowing, multi-tool assistant. Analyze the user's request carefully "
        "and select the single, most appropriate tool from your arsenal to answer the question. "
        "Only call the tool if the request is specific (e.g., 'What is the plot of Dune?', 'Tell me about one piece'). "
        "If multiple tools are needed, use them sequentially or combine the resulting data into a single, cohesive answer."
    ),
    tools=[
        search_anime,
        search_books_by_title,
        get_free_games_by_filter,
        get_top_tracks_global,
        get_movie_details,
    ]
)