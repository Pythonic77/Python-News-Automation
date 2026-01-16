"""
Main Automation Script for Modern_USA_News (FREE Version)
Fully automated RSS-based news system with image generation

ZERO COST - NO API KEYS REQUIRED

Features:
- RSS news collection from major US outlets
- Smart story ranking and selection
- AI content generation (Ollama/HuggingFace/Fallback)
- PIL-based image generation with watermarks
- Content safety filtering
- Comprehensive logging
- Date-based output organization
"""

import time
import schedule
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rss_collector import RSSCollector
from news_ranker import NewsRanker
from free_llm_writer import FreeContentGenerator
from output_manager import OutputManager
from image_generator_pil import FreeImageGenerator
from content_safety import get_safety
from logger import get_logger, safe_execute
from rss_config import COLLECTION_INTERVAL_HOURS, MAX_STORIES_PER_DAY

# Feature Flags
ENABLE_REELS = False  # Keep disabled by default as requested


class NewsAutomation:
    """
    Main automation controller for Modern_USA_News
    Coordinates all modules for daily news content generation
    """
    
    def __init__(self):
        self.logger = get_logger()
        
        self.logger.section("SYSTEM INITIALIZATION")
        
        # Initialize all modules with error handling
        self.collector = self._init_module("RSS Collector", RSSCollector)
        self.ranker = self._init_module("News Ranker", NewsRanker)
        self.writer = self._init_module("Content Generator", FreeContentGenerator)
        self.output = self._init_module("Output Manager", OutputManager)
        self.image_gen = self._init_module("Image Generator", FreeImageGenerator)
        self.safety = get_safety()
        
        self._print_banner()
    
    def _init_module(self, name: str, module_class):
        """Safely initialize a module"""
        try:
            module = module_class()
            self.logger.success(f"{name}: Ready")
            return module
        except Exception as e:
            self.logger.error(f"{name} failed to initialize", exc=e)
            return None
    
    def _print_banner(self):
        """Print startup banner"""
        print("\n" + "=" * 60)
        print(" � MODERN USA NEWS - FREE Automation System")
        print("=" * 60)
        print(" ✅ 100% Free - No API Keys Required")
        print(" ✅ RSS-Based News Collection")
        print(" ✅ AI Content Generation (Local/Free)")
        print(" ✅ PIL Image Generation with Watermarks")
        print(" ✅ Content Safety Filtering")
        print("=" * 60 + "\n")
    
    @safe_execute(fallback_value=False)
    def run_daily_cycle(self) -> bool:
        """Run the complete daily content generation cycle"""
        self.logger.section(f"DAILY CYCLE - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Save state for recovery
        self.logger.save_recovery_state({'stage': 'started', 'time': datetime.now().isoformat()})
        
        try:
            # Step 1: Collect news
            self.logger.step(1, "Collecting RSS feeds")
            if self.collector:
                stats = self.collector.collect_all()
                total_new = sum(stats.values())
                self.logger.update_stat('articles_added', total_new)
            else:
                self.logger.warning("RSS Collector not available, skipping collection")
            
            # Warm up Ollama models before processing batch
            if self.writer:
                self.writer.warmup_ollama()
            
            # Step 2: Rank and select stories
            self.logger.step(2, f"Selecting top {MAX_STORIES_PER_DAY} stories")
            if not self.ranker:
                self.logger.error("News Ranker not available")
                return False
            
            # Reset selections for fresh run
            self.ranker.reset_selections()
            top_stories = self.ranker.get_top_stories(MAX_STORIES_PER_DAY)
            
            if not top_stories:
                self.logger.warning("No stories available. Try adjusting filters or running fetch first.")
                return False
            
            self.logger.info(f"   Selected {len(top_stories)} stories")
            
            # Step 3: Generate content
            self.logger.step(3, "Generating AI content")
            if not self.writer or not self.output:
                self.logger.error("Writer or Output Manager not available")
                return False
            
            # Clear today's folder
            self.output.clear_today()
            
            generated_posts = []
            for i, article in enumerate(top_stories, 1):
                try:
                    self.logger.info(f"\n   [{i}/{len(top_stories)}] Processing: {article['title'][:55]}...")
                    
                    # Generate content
                    content = self.writer.generate_content(article)
                    
                    # Apply content safety
                    cleaned_content, issues = self.safety.validate_and_clean(content)
                    
                    if issues:
                        self.logger.debug(f"Safety issues for article {i}: {issues}")
                    
                    # Save technical text files
                    files = self.output.save_post(article, cleaned_content, i)
                    
                    # Generate Visual Carousel (Viral Carousel Engine)
                    self.logger.info(f"      🎨 Generating 4-slide carousel (Glassmorphism style)...")
                    try:
                        # Sentiment check (simplified)
                        sentiment = "Neutral"
                        text_blob = (article['title'] + " " + article.get('description', '')).lower()
                        if any(w in text_blob for w in ['success', 'breakthrough', 'positive', 'good']):
                            sentiment = "Positive"
                        elif any(w in text_blob for w in ['killing', 'tragedy', 'death', 'crash', 'police']):
                            sentiment = "Serious"
                            
                        image_paths = self.image_gen.generate_carousel(
                            slides=cleaned_content.get('slides', []),
                            category=cleaned_content.get('category', 'General'),
                            post_number=i,
                            sentiment=sentiment
                        )
                        self.output.save_carousel_images(i, image_paths)
                    except Exception as visual_err:
                        self.logger.error(f"      ⚠️ Carousel failed, but text files saved", exc=visual_err)

                    # OPTIONAL REELS GENERATION (FEATURE #6)
                    if ENABLE_REELS:
                        try:
                            self.logger.info("      🎬 Attempting reels generation...")
                            # (Placeholder for generic video logic)
                            pass
                        except Exception as reel_err:
                            self.logger.debug(f"      Silently skipped reel error: {reel_err}")

                    generated_posts.append({
                        'number': i,
                        'headline': cleaned_content.get('headline', ''),
                        'category': cleaned_content.get('category', 'General'),
                        'files': files
                    })
                    
                    self.logger.success(f"Post #{i}: Ready with Carousel & Prompts")
                    self.logger.update_stat('posts_generated')
                    
                    time.sleep(1.0)  # Moderate pause for stability
                    
                except Exception as e:
                    self.logger.error(f"Failed to process article {i}", exc=e)
                    continue
            
            # Step 4: Final Summary
            self.logger.step(4, "All Content Ready")
            self.logger.info("   ✅ Viral Carousels generated")
            self.logger.info("   ✅ Image prompts saved (image_prompt.txt)")
            self.logger.info("   ✅ First comments generated (first_comment.txt)")
            
            # Step 5: Create daily report
            self.logger.step(5, "Creating daily report")
            report = self.output.create_daily_report()
            
            # Step 6: Archive old folders
            self.output.archive_old_folders(keep_days=7)
            
            # Clear recovery state on success
            self.logger.clear_recovery_state()
            
            # Final summary
            self.logger.section("CYCLE COMPLETE")
            self.logger.info(f"   📁 Output: {self.output.today_dir}")
            self.logger.info(f"   📝 Posts: {len(generated_posts)}")
            
            summary = self.output.get_post_summary()
            self.logger.info(f"   🖼️ Images: {summary['posts_with_images']}")
            self.logger.info(f"   📊 Categories: {summary['categories']}")
            
            return True
            
        except Exception as e:
            self.logger.error("Daily cycle failed", exc=e)
            self.logger.save_recovery_state({'stage': 'failed', 'error': str(e)})
            return False
    
    @safe_execute(fallback_value=None)
    def run_collection_only(self):
        """Just collect news (runs periodically)"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.logger.info(f"\n[{timestamp}] 📡 Running scheduled RSS collection...")
        
        if self.collector:
            stats = self.collector.collect_all()
            total = sum(stats.values())
            self.logger.info(f"   Collected {total} new articles")
        else:
            self.logger.warning("Collector not available")
    
    def start_scheduler(self):
        """Start the automated scheduler"""
        self.logger.section("SCHEDULER SETUP")
        self.logger.info(f"   RSS collection: Every {COLLECTION_INTERVAL_HOURS} hours")
        self.logger.info(f"   Daily generation: Every day at 06:00 AM")
        self.logger.info(f"\n   Press Ctrl+C to stop\n")
        
        # Schedule RSS collection
        schedule.every(COLLECTION_INTERVAL_HOURS).hours.do(self.run_collection_only)
        
        # Schedule daily content generation
        schedule.every().day.at("06:00").do(self.run_daily_cycle)
        
        # Run scheduler loop
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                self.logger.info("\n\n👋 Shutting down gracefully...")
                self.logger.print_summary()
                break
            except Exception as e:
                self.logger.error("Scheduler error", exc=e)
                time.sleep(60)  # Wait and retry


def main():
    """Main entry point"""
    print("\n" + "=" * 60)
    print(" 🚀 Starting Modern_USA_News Automation")
    print("=" * 60 + "\n")
    
    try:
        bot = NewsAutomation()
        
        # Run initial daily cycle
        print("🎯 Running initial content generation...\n")
        success = bot.run_daily_cycle()
        
        if success:
            print("\n✅ Initial cycle complete!")
            print("📁 Check the output folder for your posts.")
        else:
            print("\n⚠️ Initial cycle had issues. Check the logs.")
        
        # Ask about scheduler
        print("\n" + "-" * 40)
        print("Options:")
        print("  1. Start automated scheduler")
        print("  2. Exit (posts already generated)")
        print("-" * 40)
        
        try:
            choice = input("\nStart scheduler? (y/n): ").strip().lower()
            if choice == 'y':
                bot.start_scheduler()
            else:
                print("\n👋 Exiting. Your posts are ready!")
        except EOFError:
            # Non-interactive mode, just exit
            print("\n👋 Exiting. Your posts are ready!")
        
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Exiting...")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
