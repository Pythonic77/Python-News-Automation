"""
RSS News Collector for Modern_USA_News
Collects news from multiple RSS feeds and stores in SQLite
"""

import feedparser
import sqlite3
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict
import time
from rss_config import (
    RSS_FEEDS, DB_PATH, US_KEYWORDS, EXCLUSION_KEYWORDS,
    PRIORITY_KEYWORDS, CATEGORY_KEYWORDS, ARCHIVE_DAYS
)

class RSSCollector:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_database()
        print("📡 RSS Collector initialized")
    
    def _init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_hash TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                link TEXT NOT NULL,
                source TEXT NOT NULL,
                category TEXT,
                published_time TEXT,
                collected_time TEXT,
                priority_score INTEGER DEFAULT 0,
                is_us_related INTEGER DEFAULT 0,
                is_excluded INTEGER DEFAULT 0,
                selected_for_post INTEGER DEFAULT 0,
                posted INTEGER DEFAULT 0
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_article_hash ON articles(article_hash)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_priority ON articles(priority_score DESC)
        """)
        
        conn.commit()
        conn.close()
        print("✅ Database initialized")
    
    def _generate_hash(self, title: str, link: str) -> str:
        """Generate unique hash for article"""
        combined = f"{title}|{link}".lower()
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _is_us_related(self, text: str) -> bool:
        """Check if article is US-related"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in US_KEYWORDS)
    
    def _should_exclude(self, text: str) -> bool:
        """Check if article should be excluded"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in EXCLUSION_KEYWORDS)
    
    def _calculate_priority(self, title: str, description: str) -> int:
        """Calculate priority score based on keywords"""
        text = f"{title} {description}".lower()
        score = 0
        
        for level, data in PRIORITY_KEYWORDS.items():
            for keyword in data["keywords"]:
                if keyword in text:
                    score += data["score"]
        
        return score
    
    def _detect_category(self, title: str, description: str) -> str:
        """Detect article category"""
        text = f"{title} {description}".lower()
        
        category_scores = {}
        for category, keywords in CATEGORY_KEYWORDS.items():
            count = sum(1 for keyword in keywords if keyword in text)
            if count > 0:
                category_scores[category] = count
        
        if category_scores:
            return max(category_scores, key=category_scores.get)
        return "General"
    
    def collect_feed(self, feed_url: str, source_name: str) -> int:
        """Collect articles from a single RSS feed"""
        try:
            feed = feedparser.parse(feed_url)
            added_count = 0
            
            for entry in feed.entries:
                try:
                    # Extract data
                    title = entry.get('title', '').strip()
                    description = entry.get('description', '') or entry.get('summary', '')
                    link = entry.get('link', '').strip()
                    
                    if not title or not link:
                        continue
                    
                    # Generate hash
                    article_hash = self._generate_hash(title, link)
                    
                    # Check filters
                    full_text = f"{title} {description}"
                    is_us = self._is_us_related(full_text)
                    is_excluded = self._should_exclude(full_text)
                    priority_score = self._calculate_priority(title, description)
                    category = self._detect_category(title, description)
                    
                    # Get published time
                    published_time = entry.get('published', '') or entry.get('updated', '')
                    if not published_time:
                        published_time = datetime.now().isoformat()
                    
                    # Insert into database
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    
                    cursor.execute("""
                        INSERT OR IGNORE INTO articles 
                        (article_hash, title, description, link, source, category, 
                         published_time, collected_time, priority_score, is_us_related, is_excluded)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        article_hash, title, description, link, source_name, category,
                        published_time, datetime.now().isoformat(), priority_score, 
                        int(is_us), int(is_excluded)
                    ))
                    
                    if cursor.rowcount > 0:
                        added_count += 1
                    
                    conn.commit()
                    conn.close()
                    
                except Exception as e:
                    print(f"   ⚠️  Error processing entry: {e}")
                    continue
            
            return added_count
            
        except Exception as e:
            print(f"   ❌ Error fetching feed {feed_url}: {e}")
            return 0
    
    def collect_all(self) -> Dict[str, int]:
        """Collect from all RSS feeds"""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🔄 Starting RSS collection...")
        
        stats = {}
        total_added = 0
        
        for source_id, source_data in RSS_FEEDS.items():
            source_name = source_data["name"]
            print(f"   📰 Collecting from {source_name}...")
            
            source_total = 0
            for feed_type, feed_url in source_data["feeds"].items():
                added = self.collect_feed(feed_url, source_name)
                source_total += added
            
            stats[source_name] = source_total
            total_added += source_total
            print(f"      ✅ Added {source_total} new articles")
            time.sleep(1)  # Be nice to servers
        
        # Clean old articles
        self._clean_old_articles()
        
        print(f"\n   📊 Total new articles collected: {total_added}")
        return stats
    
    def _clean_old_articles(self):
        """Remove articles older than ARCHIVE_DAYS"""
        cutoff_date = (datetime.now() - timedelta(days=ARCHIVE_DAYS)).isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM articles 
            WHERE collected_time < ? AND posted = 0
        """, (cutoff_date,))
        
        deleted = cursor.rowcount
        if deleted > 0:
            print(f"   🗑️  Cleaned {deleted} old articles")
        
        conn.commit()
        conn.close()
    
    def get_article_count(self) -> int:
        """Get total article count"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM articles WHERE is_excluded = 0")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_stats(self) -> Dict:
        """Get collection statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM articles")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM articles WHERE is_us_related = 1")
        us_related = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM articles WHERE is_excluded = 1")
        excluded = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT source) FROM articles")
        sources = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_articles": total,
            "us_related": us_related,
            "excluded": excluded,
            "active_sources": sources
        }


if __name__ == "__main__":
    # Test collection
    collector = RSSCollector()
    stats = collector.collect_all()
    
    print("\n📊 Collection Stats:")
    for source, count in stats.items():
        print(f"   {source}: {count} articles")
    
    print(f"\n   Overall Stats: {collector.get_stats()}")
