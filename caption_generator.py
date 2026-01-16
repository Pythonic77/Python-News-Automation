"""
Caption Generator using OpenRouter API
"""

import requests
import json
import re
from typing import Dict, Optional
from config import OPENROUTER_API_KEY, CATEGORIES, COMMON_HASHTAGS, CHANNEL_HANDLE

class CaptionGenerator:
    """Generates engaging Instagram captions using OpenRouter/OpenAI Compatible API"""
    
    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    MODELS = [
        "google/gemini-1.5-flash",       # Paid/Limitless Tier
        "openai/gpt-4o-mini",            # Paid/Limitless Tier
        "google/gemini-2.0-flash-exp:free",
        "xiaomi/mimo-v2-flash:free", 
        "mistralai/mistral-7b-instruct:free"
    ]
    
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        if not self.api_key:
            print("⚠️  Warning: No OpenRouter API Key found. Captions will be basic.")

    def generate_content(self, article: Dict) -> Dict[str, str]:
        category = article.get("category", "general")
        title = article.get("title", "")
        description = article.get("description", "") or ""
        source = article.get("source", "")
        
        base_hook = title[:20].upper() + "..." if len(title) > 20 else title.upper()
        base_caption = f"📰 BREAKING: {title}\n\n{description}\n\nSource: {source}\n\n" + self._get_hashtags(category)
        
        if not self.api_key:
            return {'hook': base_hook, 'caption': base_caption}
            
        # Try each model
        for model in self.MODELS:
            try:
                print(f"   🤖 Trying AI model: {model}...")
                return self._generate_with_ai(title, description, source, category, model)
            except Exception as e:
                print(f"      ⚠️  Model {model} failed: {e}")
                continue
        
        print("      ❌ All models failed. Using fallback.")
        return {'hook': base_hook, 'caption': base_caption}

    def _generate_with_ai(self, title: str, description: str, source: str, category: str, model: str) -> Dict[str, str]:
        system_prompt = f"You are a social media expert for '{CHANNEL_HANDLE}'. You write engaging, professional news content."
        
        user_prompt = f"""
        I have a news article. I need two things:
        1. A VISUAL HOOK: A short, punchy (max 6-8 words) headline to put ON the image. Must be attention-grabbing but accurate. Capitalized.
        2. A CAPTION: A detailed, SEO-friendly summary.
        
        ARTICLE:
        Headline: {title}
        Details: {description}
        Source: {source}
        Category: {category}
        
        OUTPUT FORMAT (Strict JSON):
        {{
            "hook": "THE SHORT HOOK TEXT",
            "caption": "The full caption text..."
        }}
        
        CAPTION GUIDELINES:
        - Start with a strong opening line.
        - Write 3 short paragraphs summarizing the news in depth.
        - Add bullet points for key details if relevant.
        - Tone: Professional yet engaging news anchor.
        - End with: "Source: {source} | Follow {CHANNEL_HANDLE}"
        - INCLUDE 20 highly relevant, SEO-optimized hashtags at the very end.
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://modernusanews.com",
            "X-Title": "Modern USA News Bot"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "response_format": { "type": "json_object" }
        }
        
        response = requests.post(self.API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 429:
            raise Exception("Rate limit exceeded (429)")
        if response.status_code == 404:
            raise Exception("Model not found (404)")
            
        response.raise_for_status()
        result_json = response.json()
        
        if 'error' in result_json:
            raise Exception(str(result_json['error']))

        text = result_json['choices'][0]['message']['content']
        
        try:
            clean_text = re.sub(r'```json\s*|\s*```', '', text)
            parsed = json.loads(clean_text)
            return parsed
        except json.JSONDecodeError:
            return {
                'hook': title[:20].upper() + "...",
                'caption': text + "\n\n" + self._get_hashtags(category)
            }

    def _get_hashtags(self, category: str) -> str:
        cat_tags = CATEGORIES.get(category, {}).get("hashtags", [])
        all_tags = cat_tags + COMMON_HASHTAGS
        return " ".join(list(set(all_tags)))

# Test
if __name__ == "__main__":
    cg = CaptionGenerator()
    test_article = {
        "title": "NASA Launches New Mission to Mars",
        "description": "The space agency's latest rover aims to find signs of ancient life.",
        "source": "Space.com",
        "category": "technology"
    }
    print(cg.generate_content(test_article))
