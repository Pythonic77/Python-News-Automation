"""
RSS Configuration for Modern_USA_News
Free news sources using public RSS feeds
"""

# RSS Feed Sources (All FREE)
RSS_FEEDS = {
    "cnn": {
        "name": "CNN",
        "feeds": {
            "top": "http://rss.cnn.com/rss/cnn_topstories.rss",
            "politics": "http://rss.cnn.com/rss/cnn_allpolitics.rss",
            "business": "http://rss.cnn.com/rss/money_latest.rss",
            "tech": "http://rss.cnn.com/rss/cnn_tech.rss"
        }
    },
    "nbc": {
        "name": "NBC News",
        "feeds": {
            "top": "https://feeds.nbcnews.com/nbcnews/public/news",
            "politics": "https://feeds.nbcnews.com/nbcnews/public/politics",
            "business": "https://feeds.nbcnews.com/nbcnews/public/business"
        }
    },
    "fox": {
        "name": "Fox News",
        "feeds": {
            "top": "https://moxie.foxnews.com/google-publisher/latest.xml",
            "politics": "https://moxie.foxnews.com/google-publisher/politics.xml"
        }
    },
    "ap": {
        "name": "Associated Press",
        "feeds": {
            "top": "https://feeds.apnews.com/rss/apf-topnews",
            "politics": "https://feeds.apnews.com/rss/apf-usnews",
            "business": "https://feeds.apnews.com/rss/apf-business"
        }
    },
    "reuters": {
        "name": "Reuters",
        "feeds": {
            "top": "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best",
            "business": "https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best",
            "world": "https://www.reutersagency.com/feed/?best-topics=international-news&post_type=best"
        }
    },
    "nyt": {
        "name": "New York Times",
        "feeds": {
            "top": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
            "politics": "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
            "business": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml"
        }
    },
    "politico": {
        "name": "Politico",
        "feeds": {
            "top": "https://www.politico.com/rss/politicopicks.xml",
            "congress": "https://www.politico.com/rss/congress.xml"
        }
    }
}

# Priority Keywords (for ranking)
PRIORITY_KEYWORDS = {
    "critical": {
        "keywords": ["president", "biden", "trump", "white house", "congress", "senate", 
                    "supreme court", "election", "vote", "pentagon", "war", "russia", 
                    "china", "nuclear", "terrorism", "shooting", "bomb", "coup"],
        "score": 10
    },
    "high": {
        "keywords": ["economy", "inflation", "federal reserve", "stock market", "unemployment",
                    "gas prices", "nato", "military", "fbi", "justice department", "governor",
                    "mayor", "law", "bill", "impeach", "investigation"],
        "score": 7
    },
    "medium": {
        "keywords": ["sports", "nfl", "nba", "super bowl", "olympics", "technology", "apple",
                    "google", "meta", "tesla", "space", "nasa", "health", "covid", "weather",
                    "hurricane", "earthquake", "wildfire"],
        "score": 5
    }
}

# US-Related Keywords (for filtering)
US_KEYWORDS = [
    "usa", "u.s.", "united states", "america", "american", "washington", "new york",
    "california", "texas", "florida", "biden", "trump", "congress", "senate", "house",
    "governor", "mayor", "state", "federal", "fbi", "cia", "pentagon", "white house"
]

# Exclusion Keywords (spam/gossip)
EXCLUSION_KEYWORDS = [
    "kardashian", "celebrity", "hollywood", "gossip", "dating", "relationship",
    "instagram model", "tiktok", "viral video", "meme", "horoscope", "zodiac",
    "quiz", "sponsored", "advertisement"
]

# Category Mapping
CATEGORY_KEYWORDS = {
    "Politics": ["president", "congress", "senate", "election", "vote", "bill", "law", 
                 "politics", "biden", "trump", "governor", "democrat", "republican"],
    "Economy": ["economy", "inflation", "stock", "market", "fed", "federal reserve", 
                "unemployment", "jobs", "gdp", "recession", "trade"],
    "Technology": ["tech", "technology", "ai", "artificial intelligence", "apple", "google",
                   "meta", "tesla", "space", "nasa", "innovation"],
    "Sports": ["nfl", "nba", "mlb", "nhl", "super bowl", "world series", "olympics", 
               "sports", "game", "championship"],
    "Justice": ["crime", "shooting", "court", "supreme court", "justice", "police", 
                "trial", "verdict", "fbi", "investigation"],
    "International": ["war", "russia", "china", "ukraine", "nato", "military", "conflict",
                     "foreign policy", "diplomacy"],
    "Health": ["health", "covid", "pandemic", "vaccine", "hospital", "medical"],
    "Environment": ["climate", "weather", "hurricane", "wildfire", "earthquake", "flood",
                    "environment", "epa"]
}

# Instagram Settings
CHANNEL_NAME = "Modern_USA_News"
CHANNEL_HANDLE = "@modern_usa_news"

# Database Settings
DB_PATH = "news_database.db"

# Collection Settings
COLLECTION_INTERVAL_HOURS = 2
MAX_STORIES_PER_DAY = 5
ARCHIVE_DAYS = 7  # Keep articles for 7 days

# Output Settings
OUTPUT_DIR = "ModernUSANews"
TODAY_DIR = "Today"
ARCHIVE_DIR = "Archive"

# Free LLM Settings (we'll use Ollama locally + HuggingFace API as fallback)
OLLAMA_MODELS = ["llama3.2:1b", "qwen2.5:1.5b", "phi3:mini", "llama3.2:latest"]  # CPU-optimized models
OLLAMA_TIMEOUT = 120  # Increased timeout for CPU rendering
OLLAMA_DELAY = 2      # Delay between batch requests
MAX_PROMPT_CHARS = 700 # Truncate article content to reduce payload

HUGGINGFACE_API_KEY = ""  # Optional: HF free tier
HUGGINGFACE_MODELS = [
    "meta-llama/Llama-3.2-3B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "HuggingFaceH4/zephyr-7b-beta"
]

# Hashtag Pools
CATEGORY_HASHTAGS = {
    "Politics": ["#USPolitics", "#Politics", "#Congress", "#WhiteHouse", "#Election2024"],
    "Economy": ["#Economy", "#StockMarket", "#Finance", "#Business", "#EconomicNews"],
    "Technology": ["#Tech", "#Technology", "#Innovation", "#AI", "#TechNews"],
    "Sports": ["#Sports", "#NFL", "#NBA", "#SportNews", "#USASports"],
    "Justice": ["#Justice", "#Crime", "#Law", "#SupremeCourt", "#LegalNews"],
    "International": ["#WorldNews", "#ForeignPolicy", "#GlobalNews", "#InternationalNews"],
    "Health": ["#Health", "#Healthcare", "#PublicHealth", "#Medical"],
    "Environment": ["#Climate", "#Weather", "#Environment", "#ClimateChange"]
}

COMMON_HASHTAGS = [
    "#USA", "#AmericaNews", "#BreakingNews", "#News", "#USANews",
    "#ModernUSANews", "#NewsToday", "#CurrentEvents", "#Trending", "#Newsworthy"
]
