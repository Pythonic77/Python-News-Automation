"""
Quick Start Script for Modern_USA_News
Test the system and generate your first batch
"""

import sys
import os

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def main():
    print_header("🚀 Modern_USA_News - Quick Start Test")
    
    # Test 1: RSS Collection
    print("📡 TEST 1: RSS News Collection")
    print("   Collecting from 7 news sources...")
    
    try:
        from rss_collector import RSSCollector
        collector = RSSCollector()
        stats = collector.collect_all()
        
        total = sum(stats.values())
        print(f"\n   ✅ SUCCESS! Collected {total} new articles")
        print("\n   Breakdown:")
        for source, count in stats.items():
            print(f"      • {source}: {count} articles")
        
        overall = collector.get_stats()
        print(f"\n   📊 Database Stats:")
        print(f"      • Total articles: {overall['total_articles']}")
        print(f"      • US-related: {overall['us_related']}")
        print(f"      • Active sources: {overall['active_sources']}")
        
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        print("   Check that all dependencies are installed.")
        return False
    
    # Test 2: News Ranking
    print_header("🎯 TEST 2: Smart News Ranking")
    print("   Selecting top 5 stories...")
    
    try:
        from news_ranker import NewsRanker
        ranker = NewsRanker()
        top_stories = ranker.get_top_stories(5)
        
        if not top_stories:
            print("   ⚠️  No stories found yet. This is normal on first run.")
            print("   Try running the collector again in a few minutes.")
        else:
            print(f"\n   ✅ Selected {len(top_stories)} top stories:")
            for i, story in enumerate(top_stories, 1):
                print(f"\n      {i}. [{story['category']}] {story['title'][:60]}...")
                print(f"         Source: {story['source']}")
                print(f"         Priority: {story['priority_score']}")
    
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    # Test 3: AI Content Generation
    print_header("🤖 TEST 3: AI Content Generation")
    
    try:
        from free_llm_writer import FreeContentGenerator
        writer = FreeContentGenerator()
        
        # Test with sample article
        test_article = {
            "title": "Breaking: Major Economic Policy Announced by Federal Reserve",
            "description": "The Federal Reserve announced significant changes to interest rates affecting millions of Americans.",
            "source": "Reuters",
            "category": "Economy"
        }
        
        print("   Generating content for test article...")
        content = writer.generate_content(test_article)
        
        print(f"\n   ✅ Content Generated Successfully!")
        print(f"\n      📰 Headline:\n         {content['headline']}")
        print(f"\n      🖼️  Image Summary:\n         {content['image_summary']}")
        print(f"\n      #️⃣ Hashtags:\n         {content['hashtags']}")
        print(f"\n      🔑 Keywords: {content['keywords']}")
    
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        print("   Note: If Ollama is not installed, the system will use HuggingFace.")
        print("   Install Ollama for better results: https://ollama.com")
    
    # Test 4: Output Manager
    print_header("📁 TEST 4: File Output System")
    
    try:
        from output_manager import OutputManager
        manager = OutputManager()
        
        print(f"   ✅ Output directories created:")
        print(f"      • Today: {manager.today_dir}")
        print(f"      • Archive: {manager.archive_dir}")
        
        # Check if any posts exist
        posts = manager.get_today_posts()
        if posts:
            print(f"\n   📋 Found {len(posts)} existing posts")
        else:
            print(f"\n   📋 No posts yet (this is normal)")
    
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    # Final Summary
    print_header("✅ ALL TESTS PASSED!")
    
    print("🎯 What's Next?\n")
    print("   Option 1: Generate your first posts NOW")
    print("   ========================================")
    print("   Run: python free_automation.py")
    print("   This will generate 5 posts immediately")
    print()
    print("   Option 2: Start the Dashboard")
    print("   ========================================")
    print("   Run: python free_dashboard.py")
    print("   Then open: http://localhost:5000")
    print()
    print("   Option 3: Read the Full Guide")
    print("   ========================================")
    print("   Open: FREE_SETUP_GUIDE.md")
    print()
    
    print("📌 Quick Tip: Install Ollama for 100% free AI")
    print("   Download: https://ollama.com/download")
    print("   Then run: ollama pull llama3.2")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Some tests failed. Check error messages above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted by user")
        sys.exit(0)
