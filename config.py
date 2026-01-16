"""
Configuration settings for Modern_USA_News Instagram Automation
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Channel Configuration
CHANNEL_NAME = os.getenv("CHANNEL_NAME", "Modern_USA_News")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE", "@modern_usa_news")

# Instagram Post Dimensions
POST_WIDTH = 1080
POST_HEIGHT = 1080

# News Categories with their styling
CATEGORIES = {
    "politics": {
        "name": "Politics",
        "keywords": ["politics", "government", "election", "congress", "senate", "president", "white house", "biden", "trump", "democrat", "republican"],
        "colors": {
            "primary": "#DC2626",      # Red
            "secondary": "#1E40AF",    # Blue
            "gradient": ["#DC2626", "#1E40AF"],
            "text": "#FFFFFF",
            "accent": "#FCD34D"
        },
        "search_term": "politics OR government OR election OR congress",
        "hashtags": ["#Politics", "#USPolitics", "#Government", "#Election", "#Congress"]
    },
    "technology": {
        "name": "Technology",
        "keywords": ["tech", "technology", "ai", "artificial intelligence", "software", "startup", "silicon valley", "google", "apple", "microsoft", "meta"],
        "colors": {
            "primary": "#7C3AED",      # Purple
            "secondary": "#06B6D4",    # Cyan
            "gradient": ["#7C3AED", "#06B6D4"],
            "text": "#FFFFFF",
            "accent": "#F0ABFC"
        },
        "search_term": "technology OR tech OR AI OR startup",
        "hashtags": ["#TechNews", "#Technology", "#AI", "#Innovation", "#SiliconValley"]
    },
    "business": {
        "name": "Business",
        "keywords": ["business", "economy", "stock", "market", "finance", "wall street", "trading", "inflation", "fed"],
        "colors": {
            "primary": "#F59E0B",      # Gold
            "secondary": "#1F2937",    # Dark
            "gradient": ["#F59E0B", "#78350F"],
            "text": "#FFFFFF",
            "accent": "#FDE68A"
        },
        "search_term": "business OR economy OR market OR finance",
        "hashtags": ["#Business", "#Economy", "#StockMarket", "#Finance", "#WallStreet"]
    },
    "sports": {
        "name": "Sports",
        "keywords": ["sports", "nfl", "nba", "mlb", "football", "basketball", "baseball", "hockey", "super bowl", "score"],
        "colors": {
            "primary": "#059669",      # Green
            "secondary": "#EA580C",    # Orange
            "gradient": ["#059669", "#065F46"],
            "text": "#FFFFFF",
            "accent": "#6EE7B7"
        },
        "search_term": "sports OR NFL OR NBA OR MLB",
        "hashtags": ["#Sports", "#NFL", "#NBA", "#MLB", "#SportNews"]
    },
    "entertainment": {
        "name": "Entertainment",
        "keywords": ["entertainment", "celebrity", "movie", "music", "hollywood", "streaming", "netflix", "star", "film"],
        "colors": {
            "primary": "#EC4899",      # Pink
            "secondary": "#8B5CF6",    # Purple
            "gradient": ["#EC4899", "#8B5CF6"],
            "text": "#FFFFFF",
            "accent": "#FBCFE8"
        },
        "search_term": "entertainment OR hollywood OR movie OR music OR celebrity",
        "hashtags": ["#Entertainment", "#Celebrity", "#Hollywood", "#Movies", "#Music"]
    },
    "general": {
        "name": "Breaking News",
        "keywords": [],
        "colors": {
            "primary": "#EF4444",      # Red
            "secondary": "#111827",    # Black
            "gradient": ["#EF4444", "#B91C1C"],
            "text": "#FFFFFF",
            "accent": "#FCA5A5"
        },
        "search_term": "breaking news",
        "hashtags": ["#BreakingNews", "#USNews", "#NewsAlert", "#Breaking"]
    }
}

# Common hashtags for all posts
COMMON_HASHTAGS = [
    "#ModernUSANews",
    "#USNews",
    "#NewsUpdate",
    "#America",
    "#UnitedStates"
]

# Fonts
FONTS = {
    "headline": "arial.ttf",
    "subheadline": "arial.ttf", 
    "body": "arial.ttf",
    "brand": "arialbd.ttf"
}

# Directories
OUTPUT_DIR = "output"
LOGS_DIR = "logs"
CACHE_DIR = "cache"
