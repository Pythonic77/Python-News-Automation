"""
FREE AI Content Generator for Modern_USA_News
Uses Ollama (local, free) with HuggingFace API fallback
"""

import requests
import time
from typing import Dict, Optional
from rss_config import (
    OLLAMA_MODELS, HUGGINGFACE_MODELS, HUGGINGFACE_API_KEY,
    CHANNEL_HANDLE, CATEGORY_HASHTAGS, COMMON_HASHTAGS,
    OLLAMA_TIMEOUT, OLLAMA_DELAY, MAX_PROMPT_CHARS
)

class FreeContentGenerator:
    def __init__(self):
        self.ollama_available = self._check_ollama()
        print(f"🤖 Content Generator initialized (Ollama: {'✅' if self.ollama_available else '❌'})")
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is running locally"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def generate_content(self, article: Dict) -> Dict[str, str]:
        """Generate content for an article with hardening"""
        title = article['title']
        description = article.get('description', '') or ''
        source = article['source']
        category = article.get('category', 'General')
        
        # Truncate content to reduce Ollama payload
        safe_desc = self._truncate_context(description)
        
        # Try Ollama first (local, free, fast)
        if self.ollama_available:
            try:
                # Add delay between requests to prevent CPU overload
                time.sleep(OLLAMA_DELAY)
                return self._generate_with_ollama(title, safe_desc, source, category)
            except Exception as e:
                print(f"   ⚠️  Ollama failed: {e}, trying HuggingFace...")
        
        # Fallback to HuggingFace
        try:
            return self._generate_with_huggingface(title, description, source, category)
        except Exception as e:
            print(f"   ⚠️  HuggingFace failed: {e}, using template fallback...")
        
        # Final fallback
        return self._generate_fallback(title, description, source, category)

    def _truncate_context(self, text: str) -> str:
        """Truncate context for Ollama payload efficiency"""
        if not text: return ""
        # Strip quotes and basic HTML tags
        clean_text = re.sub(r'<[^>]+>', '', text)
        clean_text = clean_text.replace('"', "'").strip()
        if len(clean_text) > MAX_PROMPT_CHARS:
            return clean_text[:MAX_PROMPT_CHARS] + "..."
        return clean_text

    def warmup_ollama(self):
        """Send a lightweight prompt to pre-load Ollama models"""
        if not self.ollama_available: return
        print(f"   🔥 Warming up Ollama models...")
        for model in OLLAMA_MODELS:
            try:
                requests.post(
                    "http://localhost:11434/api/generate",
                    json={"model": model, "prompt": "ready?", "stream": False},
                    timeout=10 # Short timeout for warmup
                )
            except:
                continue
    
    def _generate_with_ollama(self, title: str, desc: str, source: str, category: str) -> Dict[str, str]:
        """Generate content using local Ollama"""
        
        prompt = self._build_prompt(title, desc, source, category)
        
        # Try each Ollama model
        for model in OLLAMA_MODELS:
            try:
                print(f"   🤖 Trying Ollama model: {model}...")
                
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9
                        }
                    },
                    timeout=OLLAMA_TIMEOUT
                )
                
                if response.status_code == 200:
                    result = response.json()
                    text = result['response']
                    parsed = self._parse_response(text, title, desc, category)
                    print(f"      ✅ Generated with {model}")
                    return parsed
                    
            except Exception as e:
                print(f"      ⚠️  {model} failed: {e}")
                continue
        
        raise Exception("All Ollama models failed")
    
    def _generate_with_huggingface(self, title: str, desc: str, source: str, category: str) -> Dict[str, str]:
        """Generate content using HuggingFace Inference API (FREE)"""
        
        prompt = self._build_prompt(title, desc, source, category)
        
        # Try HuggingFace models
        for model in HUGGINGFACE_MODELS:
            try:
                print(f"   🤖 Trying HuggingFace model: {model}...")
                
                headers = {}
                if HUGGINGFACE_API_KEY:
                    headers["Authorization"] = f"Bearer {HUGGINGFACE_API_KEY}"
                
                response = requests.post(
                    f"https://api-inference.huggingface.co/models/{model}",
                    headers=headers,
                    json={"inputs": prompt, "parameters": {"max_new_tokens": 500}},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        text = result[0].get('generated_text', '')
                        parsed = self._parse_response(text, title, desc, category)
                        print(f"      ✅ Generated with {model}")
                        return parsed
                
            except Exception as e:
                print(f"      ⚠️  {model} failed: {e}")
                continue
        
        raise Exception("All HuggingFace models failed")
    
    def _build_prompt(self, title: str, desc: str, source: str, category: str) -> str:
        """Build prompt for LLM"""
        return f"""You are a professional news writer for the Instagram account "{CHANNEL_HANDLE}".

Article:
Title: {title}
Details: {desc}
Source: {source}
Category: {category}

Create content for Instagram:

1. CAROUSEL_SLIDE_1: Hook headline (max 12 words)
2. CAROUSEL_SLIDE_2: Core summary (max 40 words)
3. CAROUSEL_SLIDE_3: Why it matters (max 35 words)
4. CAROUSEL_SLIDE_4: Engaging question for audience + "Follow Modern_USA_News"
5. IMAGE_PROMPT: A detailed image generation prompt.
   Style: realistic editorial news photography, professional, neutral, no text, no logos, symbolic imagery.
6. FIRST_COMMENT: A neutral, open-ended first comment to encourage discussion. No bias, no strong opinions.
7. CAPTION: Write a 4-paragraph Instagram caption summarizing the story.

Tone: Professional, neutral, modern news anchor. Clear and concise.

Format your response as:
SLIDE_1: [content]
SLIDE_2: [content]
SLIDE_3: [content]
SLIDE_4: [content]
IMAGE_PROMPT: [your detailed image prompt]
FIRST_COMMENT: [first comment]
CAPTION: [your full caption]
"""
    
    def _parse_response(self, text: str, title: str, desc: str, category: str) -> Dict[str, str]:
        """Parse LLM response"""
        
        # Extract sections
        slide1_match = re.search(r'SLIDE_1[:\s]+(.+?)(?=\nSLIDE_2|$)', text, re.IGNORECASE | re.DOTALL)
        slide2_match = re.search(r'SLIDE_2[:\s]+(.+?)(?=\nSLIDE_3|$)', text, re.IGNORECASE | re.DOTALL)
        slide3_match = re.search(r'SLIDE_3[:\s]+(.+?)(?=\nSLIDE_4|$)', text, re.IGNORECASE | re.DOTALL)
        slide4_match = re.search(r'SLIDE_4[:\s]+(.+?)(?=\nIMAGE_PROMPT|$)', text, re.IGNORECASE | re.DOTALL)
        prompt_match = re.search(r'IMAGE_PROMPT[:\s]+(.+?)(?=\nFIRST_COMMENT|$)', text, re.IGNORECASE | re.DOTALL)
        comment_match = re.search(r'FIRST_COMMENT[:\s]+(.+?)(?=\nCAPTION|$)', text, re.IGNORECASE | re.DOTALL)
        caption_match = re.search(r'CAPTION[:\s]+(.+)', text, re.IGNORECASE | re.DOTALL)
        
        slide1 = self._enforce_limit(slide1_match.group(1).strip() if slide1_match else title, 12)
        slide2 = self._enforce_limit(slide2_match.group(1).strip() if slide2_match else desc, 40)
        slide3 = self._enforce_limit(slide3_match.group(1).strip() if slide3_match else "Developing story...", 35)
        slide4 = slide4_match.group(1).strip() if slide4_match else "What are your thoughts? Follow Modern_USA_News"
        
        image_prompt = prompt_match.group(1).strip() if prompt_match else f"realistic editorial news photography of {title}, professional, neutral, no text"
        first_comment = comment_match.group(1).strip() if comment_match else "What do you think about this development?"
        caption = caption_match.group(1).strip() if caption_match else desc
        
        # Add signature and hashtags to caption
        hashtags = self._generate_hashtags(category)
        full_caption = f"{caption}\n\n📰 Follow {CHANNEL_HANDLE} for daily U.S. news\n\n{hashtags}"
        
        keywords = self._extract_keywords(title, desc)
        
        return {
            "headline": slide1,
            "slides": [slide1, slide2, slide3, slide4],
            "image_prompt": image_prompt,
            "first_comment": first_comment,
            "caption": full_caption,
            "hashtags": hashtags,
            "keywords": keywords,
            "category": category
        }

    def _enforce_limit(self, text: str, word_limit: int) -> str:
        """Truncate text to word limit and add ellipsis if needed"""
        words = text.split()
        if len(words) > word_limit:
            return ' '.join(words[:word_limit]) + "..."
        return text
    
    def _generate_fallback(self, title: str, desc: str, source: str, category: str) -> Dict[str, str]:
        """Template-based fallback when AI fails"""
        
        # Create slides
        slide1 = self._enforce_limit(title, 12)
        slide2 = self._enforce_limit(desc or "Important update on " + title, 40)
        slide3 = "Key details emerging as this story develops from " + source
        slide4 = "What are your thoughts? Follow " + CHANNEL_HANDLE
        
        # Create fallback image prompt
        image_prompt = f"realistic editorial news photography of {title}, professional, neutral, no text, symbolic imagery"
        
        # Create first comment
        first_comment = "Stay informed on this developing story. What's your take?"
        
        # Create caption
        caption = f"""📰 BREAKING: {title}

{desc or 'Stay tuned for more details as this story develops.'}

This story comes from {source}. We're monitoring the situation and will bring you updates.

What are your thoughts on this development? Let us know in the comments! 👇

📰 Follow {CHANNEL_HANDLE} for daily U.S. news"""
        
        hashtags = self._generate_hashtags(category)
        full_caption = f"{caption}\n\n{hashtags}"
        
        keywords = self._extract_keywords(title, desc)
        
        return {
            "headline": slide1,
            "slides": [slide1, slide2, slide3, slide4],
            "image_prompt": image_prompt,
            "first_comment": first_comment,
            "caption": full_caption,
            "hashtags": hashtags,
            "keywords": keywords,
            "category": category
        }
    
    def _generate_hashtags(self, category: str) -> str:
        """Generate hashtags"""
        category_tags = CATEGORY_HASHTAGS.get(category, [])
        all_tags = category_tags[:5] + COMMON_HASHTAGS[:5]
        return ' '.join(all_tags[:10])
    
    def _extract_keywords(self, title: str, desc: str) -> str:
        """Extract top 3 keywords"""
        text = f"{title} {desc}".lower()
        
        # Simple keyword extraction (can be improved)
        words = re.findall(r'\b[a-z]{4,}\b', text)
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Filter common words
        common_words = {'this', 'that', 'with', 'from', 'have', 'been', 'were', 'said', 'will', 'their'}
        filtered = {w: c for w, c in word_freq.items() if w not in common_words}
        
        top_words = sorted(filtered.items(), key=lambda x: x[1], reverse=True)[:3]
        keywords = ', '.join([w[0].title() for w in top_words])
        
        return keywords


if __name__ == "__main__":
    # Test generator
    generator = FreeContentGenerator()
    
    test_article = {
        "title": "Biden Announces New Economic Plan to Combat Inflation",
        "description": "President Biden unveiled a comprehensive economic plan aimed at reducing inflation and lowering costs for American families.",
        "source": "CNN",
        "category": "Politics"
    }
    
    print("\n🤖 Testing content generation...")
    content = generator.generate_content(test_article)
    
    print(f"\n📰 HEADLINE:\n{content['headline']}")
    print(f"\n🖼️  IMAGE SUMMARY:\n{content['image_summary']}")
    print(f"\n📝 CAPTION:\n{content['caption']}")
    print(f"\n#️⃣ HASHTAGS:\n{content['hashtags']}")
    print(f"\n🔑 KEYWORDS:\n{content['keywords']}")
