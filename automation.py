"""
Main Automation Script for Modern_USA_News
Orchestrates news fetching, content generation, and file saving.
"""

import os
import time
import argparse
import schedule
from datetime import datetime
from news_fetcher import NewsFetcher
from image_generator import ImageGenerator
from caption_generator import CaptionGenerator
from config import OUTPUT_DIR, LOGS_DIR

class InstagramAutomation:
    def __init__(self):
        self.news_fetcher = NewsFetcher()
        self.image_generator = ImageGenerator()
        self.caption_generator = CaptionGenerator()
        
        self._ensure_dirs()
        print("🚀 Instagram Automation System Initialized")

    def _ensure_dirs(self):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(LOGS_DIR, exist_ok=True)

    def _get_output_path(self, date_str):
        path = os.path.join(OUTPUT_DIR, date_str)
        os.makedirs(path, exist_ok=True)
        return path

    def run_cycle(self):
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Starting generation cycle...")
        date_str = datetime.now().strftime("%Y-%m-%d")
        output_path = self._get_output_path(date_str)
        
        generated_count = 0
        targets = ["politics", "technology", "business", "sports", "entertainment"]
        
        for category in targets:
            print(f"   Searching for {category} news...")
            # Fetch 1 fresh article
            articles = self.news_fetcher.fetch_by_category(category, count=1)
            
            for article in articles:
                try:
                    print(f"   ✨ Processing: {article['title'][:50]}...")
                    
                    # 1. Generate Content (Hook + Caption) FIRST
                    content = self.caption_generator.generate_content(article)
                    hook_text = content['hook']
                    caption_text = content['caption']
                    
                    # Generate filename
                    safe_title = "".join([c for c in article['title'] if c.isalnum() or c in (' ', '-', '_')]).rstrip()
                    safe_title = safe_title.replace(' ', '_')[:50]
                    base_filename = f"{category}_{safe_title}"
                    
                    image_path = os.path.join(output_path, f"{base_filename}.jpg")
                    caption_path = os.path.join(output_path, f"{base_filename}.txt")
                    
                    # 2. Generate Image using the Hook
                    self.image_generator.generate_post(article, hook_text, image_path)
                    
                    # 3. Save Caption
                    with open(caption_path, "w", encoding="utf-8") as f:
                        f.write(caption_text)
                    
                    # 4. Mark as used
                    self.news_fetcher.mark_as_used([article['id']])
                    
                    print(f"      ✅ Generated: {base_filename}")
                    print(f"         Hook: {hook_text}")
                    generated_count += 1
                    
                except Exception as e:
                    print(f"      ❌ Error processing article: {str(e)}")
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Cycle complete. Generated {generated_count} posts.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    args = parser.parse_args()
    
    bot = InstagramAutomation()
    
    if args.once:
        bot.run_cycle()
    else:
        print("⏰ Scheduling active. Running every 4 hours.")
        bot.run_cycle()
        schedule.every(4).hours.do(bot.run_cycle)
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    main()
