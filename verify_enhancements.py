import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from free_llm_writer import FreeContentGenerator
from image_generator_pil import FreeImageGenerator
from output_manager import OutputManager

def test_enhancements():
    print("\n🚀 STARTING ENHANCEMENT VERIFICATION\n" + "="*40)
    
    # 1. Initialize Modules
    writer = FreeContentGenerator()
    image_gen = FreeImageGenerator()
    output = OutputManager()
    
    test_article = {
        "title": "US Economy Shows Robust Growth in Latest Report",
        "description": "New data released by the Department of Commerce indicates that the US economy grew by 3.2% in the last quarter, exceeding expectations despite inflation concerns.",
        "source": "NBC News",
        "category": "Economy"
    }
    
    # 2. Test Content Generation
    print("\n📝 [1/3] Testing Content Generation...")
    content = writer.generate_content(test_article)
    
    print(f"   ✅ Headline: {content['headline']}")
    print(f"   ✅ Number of Slides: {len(content.get('slides', []))}")
    print(f"   ✅ First Comment: {content.get('first_comment', 'MISSING')[:50]}...")
    print(f"   ✅ Image Prompt: {content.get('image_prompt', 'MISSING')[:50]}...")
    
    # 3. Test Visual Carousel
    print("\n🎨 [2/3] Testing Carousel Generation...")
    image_paths = image_gen.generate_carousel(
        slides=content['slides'],
        category=content['category'],
        post_number=99,
        sentiment="Positive"
    )
    
    for i, path in enumerate(image_paths, 1):
        if os.path.exists(path):
            print(f"   ✅ Slide {i} generated: {os.path.basename(path)}")
        else:
            print(f"   ❌ Slide {i} FAILED")
            
    # 4. Test Output Manager
    print("\n💾 [3/3] Testing Output Manager...")
    files = output.save_post(test_article, content, 99)
    
    required_files = ['caption', 'first_comment', 'image_prompt', 'hashtags', 'meta']
    for req in required_files:
        if req in files and os.path.exists(files[req]):
            print(f"   ✅ {req.replace('_', ' ').title()} file saved")
        else:
            print(f"   ❌ {req.replace('_', ' ').title()} file MISSING")
            
    print("\n" + "="*40 + "\n✅ VERIFICATION COMPLETE")

if __name__ == "__main__":
    test_enhancements()
