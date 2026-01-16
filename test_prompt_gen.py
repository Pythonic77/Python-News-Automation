
import os
import sys
from free_llm_writer import FreeContentGenerator
from output_manager import OutputManager

def test_prompt_generation():
    print("🚀 Testing Image Prompt Generation...")
    
    # 1. Test Generator
    generator = FreeContentGenerator()
    
    article = {
        "title": "NASA Launches New Satellite to Monitor Earth's Climate",
        "description": "NASA has successfully launched a new satellite designed to provide unprecedented data on Earth's climate systems and weather patterns.",
        "source": "SpaceNews",
        "category": "Science"
    }
    
    print("\n1️⃣ Generating content...")
    content = generator.generate_content(article)
    
    if 'image_prompt' in content:
        print("✅ Image Prompt Generated:")
        print(f"   {content['image_prompt'][:100]}...")
    else:
        print("❌ Image Prompt NOT found in content!")
        print(content.keys())
        return

    # 2. Test Output Manager
    print("\n2️⃣ Saving files...")
    manager = OutputManager()
    
    # Use a dummy post number 999 for testing
    files = manager.save_post(article, content, 999)
    
    prompt_path = files.get('image_prompt')
    if prompt_path and os.path.exists(prompt_path):
        print(f"✅ Image prompt file created: {prompt_path}")
        with open(prompt_path, 'r', encoding='utf-8') as f:
            saved_prompt = f.read()
        
        if saved_prompt == content['image_prompt']:
             print("✅ File content matches generated prompt")
        else:
             print("❌ File content mismatch")
    else:
        print("❌ Image prompt file NOT created")

    # Clean up
    # os.remove(prompt_path)
    print("\n✅ Verification Complete")

if __name__ == "__main__":
    test_prompt_generation()
