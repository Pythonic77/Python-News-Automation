"""
News Fetcher Module for Modern_USA_News
Fetches latest US news from NewsAPI
"""

import requests
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import hashlib
from config import NEWS_API_KEY, CATEGORIES, CACHE_DIR

class NewsFetcher:
    """Fetches and processes news from NewsAPI"""
    
    BASE_URL = "https://newsapi.org/v2"
    
    def __init__(self):
        self.api_key = NEWS_API_KEY
        self.cache_file = os.path.join(CACHE_DIR, "used_articles.json")
        self._ensure_cache_dir()
        self.used_articles = self._load_used_articles()
    
    def _ensure_cache_dir(self):
        """Create cache directory if it doesn't exist"""
        os.makedirs(CACHE_DIR, exist_ok=True)
    
    def _load_used_articles(self) -> set:
        """Load previously used article IDs to avoid duplicates"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get("articles", []))
            except:
                return set()
        return set()
    
    def _save_used_articles(self):
        """Save used article IDs"""
        with open(self.cache_file, 'w') as f:
            json.dump({"articles": list(self.used_articles)}, f)
    
    def _generate_article_id(self, article: Dict) -> str:
        """Generate unique ID for an article"""
        content = f"{article.get('title', '')}{article.get('url', '')}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _determine_category(self, article: Dict, requested_category: str = "general") -> str:
        """
        Determine the category of an article.
        If fetched via a specific category query, prioritize that.
        Otherwise try to infer from content.
        """
        if requested_category != "general":
            return requested_category
            
        title = article.get("title", "").lower()
        description = article.get("description", "") or ""
        content = f"{title} {description.lower()}"
        
        for cat_id, cat_data in CATEGORIES.items():
            if cat_id == "general":
                continue
            for keyword in cat_data["keywords"]:
                if keyword in content:
                    return cat_id
        
        return "general"
    
    def fetch_top_headlines(self, count: int = 10) -> List[Dict]:
        """Fetch general top headlines"""
        params = {
            "apiKey": self.api_key,
            "country": "us",
            "pageSize": count * 2
        }
        return self._fetch_and_process(params, count=count)

    def fetch_by_category(self, category_key: str, count: int = 5) -> List[Dict]:
        """Fetch news for a specific internal category"""
        if category_key not in CATEGORIES:
            return []
            
        # Map our internal categories to NewsAPI categories or search queries
        # NewsAPI categories: business, entertainment, general, health, science, sports, technology
        newsapi_cat_map = {
            "business": "business",
            "technology": "technology",
            "sports": "sports",
            "entertainment": "entertainment",
            "health": "health",
            "science": "science"
        }
        
        params = {
            "apiKey": self.api_key,
            "country": "us",
            "pageSize": count * 3
        }

        if category_key in newsapi_cat_map:
            params["category"] = newsapi_cat_map[category_key]
        else:
            # Fallback for 'politics' etc which isn't a standard category, use q (search)
            # Use specific keywords for better relevance if it's not a standard category
            search_query = CATEGORIES[category_key].get("search_term", "")
            if search_query:
                params["q"] = search_query
        
        return self._fetch_and_process(params, count=count, category_override=category_key)

    def _fetch_and_process(self, params: Dict, count: int, category_override: str = None) -> List[Dict]:
        try:
            response = requests.get(f"{self.BASE_URL}/top-headlines", params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "ok":
                print(f"⚠️  API Error: {data.get('message', 'Unknown error')}")
                return []
            
            articles = []
            for article in data.get("articles", []):
                article_id = self._generate_article_id(article)
                
                # Skip if already used
                if article_id in self.used_articles:
                    continue
                
                # Skip articles with missing essential data or removed content
                if not article.get("title") or article.get("title") == "[Removed]":
                    continue
                
                cat = category_override if category_override else self._determine_category(article)
                
                processed = {
                    "id": article_id,
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "source": article.get("source", {}).get("name", "Unknown"),
                    "url": article.get("url", ""),
                    "image_url": article.get("urlToImage", ""),
                    "published_at": article.get("publishedAt", ""),
                    "category": cat
                }
                
                articles.append(processed)
                if len(articles) >= count:
                    break
            
            return articles
            
        except requests.RequestException as e:
            print(f"⚠️  Request error: {e}")
            return []

    def mark_as_used(self, article_ids: List[str]):
        """Mark articles as used"""
        self.used_articles.update(article_ids)
        self._save_used_articles()
