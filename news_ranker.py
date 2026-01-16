"""
Smart News Ranker for Modern_USA_News
Selects top 5 stories based on priority, recency, and diversity
"""

import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict
from rss_config import DB_PATH, MAX_STORIES_PER_DAY

class NewsRanker:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        print("🎯 News Ranker initialized")
    
    def get_top_stories(self, count: int = MAX_STORIES_PER_DAY, hours: int = 24) -> List[Dict]:
        """
        Select top stories based on:
        1. US-related
        2. Not excluded
        3. Not already selected
        4. Priority score
        5. Recency
        6. Category diversity
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.cursor()
        
        # Get cutoff time
        cutoff_time = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        # Get top candidates
        cursor.execute("""
            SELECT *
            FROM articles
            WHERE is_us_related = 1
              AND is_excluded = 0
              AND selected_for_post = 0
              AND collected_time >= ?
            ORDER BY priority_score DESC, collected_time DESC
            LIMIT 50
        """, (cutoff_time,))
        
        candidates = [dict(row) for row in cursor.fetchall()]
        
        if not candidates:
            print("   ⚠️  No new candidates found, trying last 48 hours...")
            cutoff_time = (datetime.now() - timedelta(hours=48)).isoformat()
            cursor.execute("""
                SELECT *
                FROM articles
                WHERE is_us_related = 1
                  AND is_excluded = 0
                  AND selected_for_post = 0
                  AND collected_time >= ?
                ORDER BY priority_score DESC, collected_time DESC
                LIMIT 50
            """, (cutoff_time,))
            candidates = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        # Select top stories with category diversity
        selected = self._select_diverse_stories(candidates, count)
        
        # Mark as selected
        if selected:
            self._mark_as_selected([s['id'] for s in selected])
        
        return selected
    
    def _select_diverse_stories(self, candidates: List[Dict], count: int) -> List[Dict]:
        """
        Select stories ensuring category diversity
        """
        if len(candidates) <= count:
            return candidates
        
        selected = []
        used_categories = set()
        
        # First pass: One story per category
        for article in candidates:
            category = article['category']
            if category not in used_categories:
                selected.append(article)
                used_categories.add(category)
                if len(selected) >= count:
                    return selected
        
        # Second pass: Fill remaining slots with highest priority
        remaining = [a for a in candidates if a not in selected]
        remaining.sort(key=lambda x: x['priority_score'], reverse=True)
        
        while len(selected) < count and remaining:
            selected.append(remaining.pop(0))
        
        return selected
    
    def _mark_as_selected(self, article_ids: List[int]):
        """Mark articles as selected for posting"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        placeholders = ','.join('?' * len(article_ids))
        cursor.execute(f"""
            UPDATE articles
            SET selected_for_post = 1
            WHERE id IN ({placeholders})
        """, article_ids)
        
        conn.commit()
        conn.close()
        print(f"   ✅ Marked {len(article_ids)} articles as selected")
    
    def mark_as_posted(self, article_ids: List[int]):
        """Mark articles as posted"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        placeholders = ','.join('?' * len(article_ids))
        cursor.execute(f"""
            UPDATE articles
            SET posted = 1
            WHERE id IN ({placeholders})
        """, article_ids)
        
        conn.commit()
        conn.close()
    
    def reset_selections(self):
        """Reset all selected_for_post flags (for testing)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("UPDATE articles SET selected_for_post = 0 WHERE posted = 0")
        
        conn.commit()
        conn.close()
        print("   🔄 Reset all selections")
    
    def get_daily_summary(self) -> Dict:
        """Get summary of today's selections"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().date().isoformat()
        
        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM articles
            WHERE selected_for_post = 1
              AND DATE(collected_time) = ?
            GROUP BY category
        """, (today,))
        
        categories = dict(cursor.fetchall())
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM articles
            WHERE selected_for_post = 1
              AND DATE(collected_time) = ?
        """, (today,))
        
        total = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_selected": total,
            "categories": categories
        }


if __name__ == "__main__":
    # Test ranker
    ranker = NewsRanker()
    
    print("\n🎯 Selecting top 5 stories...")
    top_stories = ranker.get_top_stories(5)
    
    print(f"\n📰 Selected {len(top_stories)} stories:")
    for i, story in enumerate(top_stories, 1):
        print(f"\n{i}. [{story['category']}] {story['title']}")
        print(f"   Source: {story['source']}")
        print(f"   Priority: {story['priority_score']}")
        print(f"   Link: {story['link']}")
    
    print(f"\n📊 Daily Summary: {ranker.get_daily_summary()}")
