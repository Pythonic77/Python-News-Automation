"""
CLI Command Interface for Modern_USA_News
Provides independent commands for each automation step
"""

import argparse
import sys
import os
from datetime import datetime

# Ensure imports work from any directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def fetch_news():
    """Fetch news from all RSS sources"""
    print("\n" + "=" * 60)
    print("📡 FETCH NEWS - Modern_USA_News")
    print("=" * 60)
    
    try:
        from rss_collector import RSSCollector
        from logger import get_logger
        
        logger = get_logger()
        logger.section("RSS Collection")
        
        collector = RSSCollector()
        stats = collector.collect_all()
        
        print("\n📊 Collection Results:")
        total = 0
        for source, count in stats.items():
            print(f"   {source}: {count} new articles")
            total += count
        
        print(f"\n✅ Total new articles: {total}")
        overall = collector.get_stats()
        print(f"📚 Database now contains: {overall['total_articles']} articles")
        
        logger.update_stat('articles_added', total)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def rank_news(count: int = 5):
    """Select top stories based on ranking algorithm"""
    print("\n" + "=" * 60)
    print("🎯 RANK NEWS - Modern_USA_News")
    print("=" * 60)
    
    try:
        from news_ranker import NewsRanker
        
        ranker = NewsRanker()
        
        # Reset selections first (for testing/re-runs)
        print("\n🔄 Checking for new stories...")
        
        top_stories = ranker.get_top_stories(count)
        
        if not top_stories:
            print("⚠️ No eligible stories found.")
            print("   Try running fetch_news first or adjusting filters.")
            return []
        
        print(f"\n📰 Selected {len(top_stories)} top stories:\n")
        
        for i, story in enumerate(top_stories, 1):
            print(f"{i}. [{story['category']}] {story['title'][:70]}...")
            print(f"   Source: {story['source']} | Priority: {story['priority_score']}")
            print()
        
        return top_stories
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return []


def generate_posts(count: int = 5):
    """Generate content for top stories"""
    print("\n" + "=" * 60)
    print("📝 GENERATE POSTS - Modern_USA_News")
    print("=" * 60)
    
    try:
        from news_ranker import NewsRanker
        from free_llm_writer import FreeContentGenerator
        from output_manager import OutputManager
        from content_safety import get_safety
        from logger import get_logger
        
        logger = get_logger()
        
        # Get top stories
        ranker = NewsRanker()
        ranker.reset_selections()  # Reset for fresh selection
        top_stories = ranker.get_top_stories(count)
        
        if not top_stories:
            print("⚠️ No stories available. Run fetch_news first.")
            return False
        
        print(f"\n📰 Processing {len(top_stories)} stories...\n")
        
        # Initialize components
        writer = FreeContentGenerator()
        output = OutputManager()
        safety = get_safety()
        
        # Clear today's folder
        output.clear_today()
        
        success_count = 0
        for i, article in enumerate(top_stories, 1):
            try:
                print(f"\n[{i}/{len(top_stories)}] {article['title'][:60]}...")
                
                # Generate content
                content = writer.generate_content(article)
                
                # Apply content safety
                cleaned_content, issues = safety.validate_and_clean(content)
                
                if issues:
                    print(f"   ⚠️ Safety issues: {len(issues)}")
                
                # Save files
                files = output.save_post(article, cleaned_content, i)
                
                print(f"   ✅ Generated: {cleaned_content['headline'][:50]}...")
                success_count += 1
                
            except Exception as e:
                print(f"   ❌ Failed: {e}")
                continue
        
        print(f"\n{'=' * 60}")
        print(f"✅ Successfully generated {success_count}/{len(top_stories)} posts")
        print(f"📁 Output: {output.today_dir}")
        print(f"{'=' * 60}")
        
        logger.update_stat('posts_generated', success_count)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def generate_images():
    """Generate images for today's posts"""
    print("\n" + "=" * 60)
    print("🖼️ GENERATE IMAGES - Modern_USA_News")
    print("=" * 60)
    
    try:
        from output_manager import OutputManager
        from image_generator_pil import FreeImageGenerator
        from logger import get_logger
        
        logger = get_logger()
        
        output = OutputManager()
        image_gen = FreeImageGenerator()
        
        # Get today's posts
        posts = output.get_today_posts()
        
        if not posts:
            print("⚠️ No posts found. Run generate_posts first.")
            return False
        
        print(f"\n🎨 Generating images for {len(posts)} posts...\n")
        
        success_count = 0
        for post in posts:
            try:
                print(f"[{post['number']}] Creating image...")
                
                # Extract content from files
                headline = post.get('headline', 'Breaking News')
                
                # Read image text file for summary
                summary = ""
                image_text_path = post['files'].get('image_text', '')
                if os.path.exists(image_text_path):
                    with open(image_text_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'IMAGE SUMMARY:' in content:
                            summary = content.split('IMAGE SUMMARY:')[1].split('\n')[0].strip()
                
                # Get category
                category = post.get('category', 'General')
                
                # Generate image
                image_path = image_gen.generate_image(
                    headline=headline,
                    summary=summary,
                    category=category,
                    post_number=post['number']
                )
                
                if image_path and os.path.exists(image_path):
                    print(f"   ✅ Image saved: {os.path.basename(image_path)}")
                    success_count += 1
                else:
                    print(f"   ❌ Image generation failed")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
        
        print(f"\n{'=' * 60}")
        print(f"✅ Generated {success_count}/{len(posts)} images")
        print(f"{'=' * 60}")
        
        logger.update_stat('images_created', success_count)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def daily_run():
    """Run the complete daily automation cycle"""
    print("\n" + "=" * 60)
    print("🚀 DAILY RUN - Modern_USA_News")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        from logger import get_logger
        
        logger = get_logger()
        logger.section("Daily Automation Cycle")
        
        # Step 1: Fetch news
        print("\n📌 STEP 1: Fetching news...")
        fetch_news()
        
        # Step 2: Generate posts
        print("\n📌 STEP 2: Generating posts...")
        generate_posts()
        
        # Step 3: Generate images
        print("\n📌 STEP 3: Generating images...")
        generate_images()
        
        # Summary
        logger.print_summary()
        
        print("\n" + "=" * 60)
        print("🎉 DAILY CYCLE COMPLETE!")
        print(f"   All posts are ready in: ModernUSANews/Today/")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Daily run failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def regenerate_failed():
    """Attempt to regenerate any failed posts"""
    print("\n" + "=" * 60)
    print("🔄 REGENERATE FAILED - Modern_USA_News")
    print("=" * 60)
    
    try:
        from output_manager import OutputManager
        from news_ranker import NewsRanker
        
        output = OutputManager()
        ranker = NewsRanker()
        
        # Check for missing images
        posts = output.get_today_posts()
        
        missing_images = []
        for post in posts:
            # Check if image exists
            base_name = post.get('base_name', '')
            image_path = os.path.join(output.today_dir, f"{base_name}_Image.png")
            
            if not os.path.exists(image_path):
                missing_images.append(post)
        
        if not missing_images:
            print("✅ All posts are complete. Nothing to regenerate.")
            return True
        
        print(f"⚠️ Found {len(missing_images)} posts missing images")
        
        # Regenerate images
        from image_generator_pil import FreeImageGenerator
        image_gen = FreeImageGenerator()
        
        for post in missing_images:
            try:
                print(f"   Regenerating image for Post #{post['number']}...")
                
                headline = post.get('headline', 'Breaking News')
                category = post.get('category', 'General')
                
                image_gen.generate_image(
                    headline=headline,
                    summary="",
                    category=category,
                    post_number=post['number']
                )
                
            except Exception as e:
                print(f"   ❌ Still failed: {e}")
        
        print("\n✅ Regeneration complete")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_status():
    """Show current system status"""
    print("\n" + "=" * 60)
    print("📊 SYSTEM STATUS - Modern_USA_News")
    print("=" * 60)
    
    try:
        from rss_collector import RSSCollector
        from news_ranker import NewsRanker
        from output_manager import OutputManager
        
        collector = RSSCollector()
        ranker = NewsRanker()
        output = OutputManager()
        
        # Database stats
        stats = collector.get_stats()
        print(f"\n📚 Database:")
        print(f"   Total articles: {stats['total_articles']}")
        print(f"   US-related: {stats['us_related']}")
        print(f"   Active sources: {stats['active_sources']}")
        
        # Today's posts
        posts = output.get_today_posts()
        print(f"\n📝 Today's Posts: {len(posts)}")
        
        for post in posts:
            # Check for image
            base_name = post.get('base_name', '')
            image_exists = os.path.exists(
                os.path.join(output.today_dir, f"{base_name}_Image.png")
            )
            status = "✅" if image_exists else "⚠️ (no image)"
            print(f"   {status} Post #{post['number']}: {post.get('headline', 'N/A')[:40]}...")
        
        # Daily summary
        summary = ranker.get_daily_summary()
        print(f"\n📈 Daily Summary:")
        print(f"   Selected: {summary['total_selected']}")
        print(f"   Categories: {summary.get('categories', {})}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error getting status: {e}")


def reset_selections():
    """Reset article selections (for re-running)"""
    print("\n🔄 Resetting article selections...")
    
    try:
        from news_ranker import NewsRanker
        ranker = NewsRanker()
        ranker.reset_selections()
        print("✅ Selections reset. You can now select new stories.")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Modern_USA_News Automation CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  fetch        Fetch news from RSS feeds
  rank         Select top stories (--count N)
  generate     Generate posts for top stories (--count N)
  images       Generate images for today's posts
  daily        Run complete daily cycle
  regenerate   Regenerate any failed posts
  status       Show system status
  reset        Reset article selections

Examples:
  python cli.py fetch
  python cli.py generate --count 7
  python cli.py daily
        """
    )
    
    parser.add_argument('command', 
                        choices=['fetch', 'rank', 'generate', 'images', 
                                'daily', 'regenerate', 'status', 'reset'],
                        help='Command to run')
    
    parser.add_argument('--count', '-n', type=int, default=5,
                        help='Number of posts to generate (default: 5)')
    
    args = parser.parse_args()
    
    # Route to appropriate function
    commands = {
        'fetch': fetch_news,
        'rank': lambda: rank_news(args.count),
        'generate': lambda: generate_posts(args.count),
        'images': generate_images,
        'daily': daily_run,
        'regenerate': regenerate_failed,
        'status': show_status,
        'reset': reset_selections
    }
    
    success = commands[args.command]()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
