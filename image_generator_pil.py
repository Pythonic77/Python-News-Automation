"""
FREE Image Generator for Modern_USA_News
Uses PIL/Pillow for text overlay on reusable backgrounds
NO API Keys Required - 100% Local & Free
"""

import os
from datetime import datetime
from typing import Dict, Optional, Tuple, List
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from textwrap import wrap

# Configuration
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
BACKGROUND_FILE = os.path.join(ASSETS_DIR, "background.png")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

# Image Settings
IMAGE_SIZE = (1080, 1080)  # Instagram square format
BACKGROUND_COLOR = (20, 25, 35)  # Dark blue fallback

# Text Styling
HEADLINE_AREA = (60, 350, 1020, 550)  # Left, Top, Right, Bottom
SUMMARY_AREA = (60, 560, 1020, 750)
CATEGORY_AREA = (60, 180, 1020, 240)
DATE_AREA = (60, 920, 1020, 970)
BRAND_AREA = (60, 80, 1020, 140)

# Colors
TEXT_WHITE = (255, 255, 255)
TEXT_ACCENT = (255, 200, 100)  # Gold/Amber for highlights

# Smart Palettes
PALETTES = {
    "Neutral": {
        "bg": (20, 25, 35),
        "panel": (255, 255, 255, 40), # Semi-transparent white
        "accent": (255, 200, 100),
        "text": (255, 255, 255),
        "border": (255, 255, 255, 80)
    },
    "Serious": {
        "bg": (20, 10, 10), # Dark Red/Black
        "panel": (255, 255, 255, 30),
        "accent": (220, 50, 50),
        "text": (240, 240, 240),
        "border": (220, 50, 50, 100)
    },
    "Positive": {
        "bg": (10, 25, 20), # Dark Green/Teal
        "panel": (255, 255, 255, 50),
        "accent": (100, 220, 150),
        "text": (255, 255, 255),
        "border": (100, 220, 150, 120)
    }
}

CATEGORY_COLORS = {
    "Politics": (220, 100, 100),    # Red
    "Economy": (100, 180, 100),     # Green
    "Technology": (100, 150, 220),  # Blue
    "Sports": (220, 140, 60),       # Orange
    "Justice": (180, 100, 200),     # Purple
    "International": (100, 200, 200), # Cyan
    "Health": (200, 100, 150),      # Pink
    "Environment": (100, 200, 100), # Light Green
    "General": (180, 180, 180)      # Gray
}


class FreeImageGenerator:
    """
    Image generator that creates Instagram-ready news graphics
    Uses PIL for rendering text on a reusable background template
    """
    
    def __init__(self, output_dir: str = "ModernUSANews"):
        self.output_dir = output_dir
        self.background = self._load_background()
        self.fonts = self._load_fonts()
        print("🖼️ Image Generator initialized (PIL-based, 100% FREE)")
    
    def _load_background(self) -> Image.Image:
        """Load or create background image"""
        try:
            if os.path.exists(BACKGROUND_FILE):
                bg = Image.open(BACKGROUND_FILE)
                bg = bg.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
                bg = bg.convert("RGBA")
                print("   ✅ Background loaded from assets")
                return bg
        except Exception as e:
            print(f"   ⚠️ Could not load background: {e}")
        
        # Create a gradient background as fallback
        return self._create_gradient_background()
    
    def _create_gradient_background(self) -> Image.Image:
        """Create a modern gradient background"""
        img = Image.new("RGBA", IMAGE_SIZE, BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)
        
        # Create subtle gradient overlay
        for y in range(IMAGE_SIZE[1]):
            # Dark at top, slightly lighter in middle, dark at bottom
            if y < IMAGE_SIZE[1] // 2:
                alpha = int(30 * (1 - y / (IMAGE_SIZE[1] // 2)))
            else:
                alpha = int(30 * ((y - IMAGE_SIZE[1] // 2) / (IMAGE_SIZE[1] // 2)))
            
            overlay_color = (255, 255, 255, alpha)
            draw.line([(0, y), (IMAGE_SIZE[0], y)], fill=overlay_color[:3])
        
        # Add border accent
        border_color = (60, 80, 120)
        draw.rectangle([0, 0, IMAGE_SIZE[0]-1, 8], fill=(255, 200, 100))  # Top gold bar
        draw.rectangle([0, IMAGE_SIZE[1]-8, IMAGE_SIZE[0]-1, IMAGE_SIZE[1]-1], fill=(255, 200, 100))  # Bottom gold bar
        
        # Add side accents
        draw.rectangle([0, 0, 4, IMAGE_SIZE[1]-1], fill=border_color)
        draw.rectangle([IMAGE_SIZE[0]-5, 0, IMAGE_SIZE[0]-1, IMAGE_SIZE[1]-1], fill=border_color)
        
        print("   ✅ Generated gradient background")
        return img
    
    def _load_fonts(self) -> Dict[str, ImageFont.FreeTypeFont]:
        """Load fonts with fallbacks"""
        fonts = {}
        
        # Common system font paths
        system_fonts = [
            # Windows
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
            "C:/Windows/Fonts/georgia.ttf",
            # Linux
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            # Mac
            "/System/Library/Fonts/Helvetica.ttc",
        ]
        
        # Try to find available fonts
        headline_font = None
        body_font = None
        
        for font_path in system_fonts:
            if os.path.exists(font_path):
                try:
                    if "bold" in font_path.lower() or "bd" in font_path.lower() or "b." in font_path.lower():
                        if not headline_font:
                            headline_font = font_path
                    else:
                        if not body_font:
                            body_font = font_path
                except:
                    continue
        
        # Default font path
        default_font = body_font or headline_font or system_fonts[0]
        bold_font = headline_font or default_font
        
        try:
            fonts['brand'] = ImageFont.truetype(bold_font, 48)
            fonts['headline'] = ImageFont.truetype(bold_font, 52)
            fonts['summary'] = ImageFont.truetype(default_font, 36)
            fonts['category'] = ImageFont.truetype(bold_font, 32)
            fonts['date'] = ImageFont.truetype(default_font, 26)
            fonts['source'] = ImageFont.truetype(default_font, 22)
            print("   ✅ Fonts loaded successfully")
        except Exception as e:
            print(f"   ⚠️ Font loading error: {e}, using defaults")
            # Use PIL default font
            fonts['brand'] = ImageFont.load_default()
            fonts['headline'] = ImageFont.load_default()
            fonts['summary'] = ImageFont.load_default()
            fonts['category'] = ImageFont.load_default()
            fonts['date'] = ImageFont.load_default()
            fonts['source'] = ImageFont.load_default()
        
        return fonts
    
    def _get_palette(self, category: str, sentiment: str = "Neutral") -> Dict:
        """Determine palette based on category and sentiment"""
        # Override rules
        if category in ["Politics"]:
            return PALETTES["Neutral"]
        if category in ["Justice", "Crime", "Tragedy"]:
            return PALETTES["Serious"]
        
        # Fallback to sentiment hint
        return PALETTES.get(sentiment.title(), PALETTES["Neutral"])

    def generate_carousel(self, slides: List[str], category: str, 
                         post_number: int, sentiment: str = "Neutral") -> List[str]:
        """Generate 4 carousel slides with Glassmorphism style"""
        output_paths = []
        palette = self._get_palette(category, sentiment)
        
        try:
            for i, text in enumerate(slides, 1):
                filename = f"Slide_{i}.png"
                today_dir = os.path.join(self.output_dir, "Today", f"Story_{post_number}")
                os.makedirs(today_dir, exist_ok=True)
                path = os.path.join(today_dir, filename)
                
                # Create Glassmorphism slide
                self._create_glass_slide(text, category, i, palette, path)
                output_paths.append(path)
                
            return output_paths
        except Exception as e:
            print(f"   ❌ Carousel generation failed: {e}")
            # Fallback to single image
            fallback = self.generate_image(slides[0], slides[1] if len(slides)>1 else "", 
                                          category, post_number)
            return [fallback]

    def _create_glass_slide(self, text: str, category: str, slide_num: int, 
                            palette: Dict, output_path: str):
        """Create a single slide with glassmorphism effect"""
        # 1. Base background
        img = self.background.copy()
        
        # 2. Apply Gaussian Blur ONCE to background
        img = img.filter(ImageFilter.GaussianBlur(radius=15))
        
        # 3. Create panel layer
        overlay = Image.new("RGBA", IMAGE_SIZE, (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)
        
        # Panel dimensions
        panel_rect = [100, 200, 980, 880] # [L, T, R, B]
        
        # Draw shadow (soft drop shadow)
        shadow_rect = [panel_rect[0]+10, panel_rect[1]+10, panel_rect[2]+10, panel_rect[3]+10]
        draw_ov.rounded_rectangle(shadow_rect, radius=40, fill=(0, 0, 0, 60))
        
        # Draw Frosted Glass Panel
        draw_ov.rounded_rectangle(panel_rect, radius=40, fill=palette["panel"])
        
        # Draw Subtle Border
        draw_ov.rounded_rectangle(panel_rect, radius=40, outline=palette["border"], width=3)
        
        # Composite
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)
        
        # 4. Text Content
        # Header (Brand)
        self._draw_text_centered(draw, "MODERN USA NEWS", (100, 80, 980, 140), 
                                 self.fonts['brand'], palette["accent"])
        
        # Slide Number Indicator
        indicator = f"{slide_num} / 4"
        draw.text((900, 160), indicator, font=self.fonts['date'], fill=palette["text"])
        
        # Main Body Text
        # Adjust font size/area based on slide type (Hook is bigger)
        if slide_num == 1:
            font = self.fonts['headline']
            max_lines = 4
        else:
            font = self.fonts['summary']
            max_lines = 6
            
        self._draw_multiline_text(draw, text, (150, 250, 930, 830), 
                                  font, palette["text"], max_lines=max_lines)
                                  
        # Category Badge
        cat_color = CATEGORY_COLORS.get(category, CATEGORY_COLORS["General"])
        self._draw_category_badge_small(draw, category, cat_color)
        
        # Footer Date
        date_str = datetime.now().strftime("%B %d, %Y")
        draw.text((150, 950), date_str, font=self.fonts['date'], fill=(200, 200, 200))
        
        # 5. Save
        img_rgb = Image.new("RGB", img.size, palette["bg"])
        img_rgb.paste(img, mask=img.split()[3])
        img_rgb.save(output_path, "PNG", quality=95)

    def _draw_category_badge_small(self, draw: ImageDraw.Draw, category: str, color: Tuple):
        """Draw a smaller category badge for carousels"""
        text = category.upper()
        bbox = draw.textbbox((0, 0), text, font=self.fonts['category'])
        text_w = bbox[2] - bbox[0]
        
        draw.rounded_rectangle([150, 180, 150 + text_w + 30, 230], radius=15, fill=color)
        draw.text((165, 190), text, font=self.fonts['category'], fill=(255, 255, 255))

    def generate_image(self, headline: str, summary: str, category: str,
                       post_number: int, output_path: Optional[str] = None,
                       source: str = "") -> str:
        """
        Generate Instagram-ready image
        
        Args:
            headline: Main headline (max 12 words)
            summary: Image summary text (max 22 words)
            category: News category
            post_number: Post number for filename
            output_path: Optional custom output path
            source: Source attribution (optional)
            
        Returns:
            Path to generated image
        """
        try:
            # Create a copy of background
            img = self.background.copy()
            draw = ImageDraw.Draw(img)
            
            # Draw overlay for text readability
            overlay = Image.new("RGBA", IMAGE_SIZE, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            
            # Semi-transparent box behind text
            overlay_draw.rectangle(
                [40, 160, 1040, 800],
                fill=(15, 20, 30, 200)
            )
            
            # Blend overlay
            img = Image.alpha_composite(img, overlay)
            draw = ImageDraw.Draw(img)
            
            # Draw brand name
            self._draw_text_centered(
                draw, "MODERN USA NEWS", 
                BRAND_AREA, self.fonts['brand'], TEXT_ACCENT
            )
            
            # Draw category badge
            category_color = CATEGORY_COLORS.get(category, CATEGORY_COLORS["General"])
            self._draw_category_badge(draw, category, category_color)
            
            # Draw headline
            self._draw_multiline_text(
                draw, headline, HEADLINE_AREA, 
                self.fonts['headline'], TEXT_WHITE, max_lines=3
            )
            
            # Draw summary
            self._draw_multiline_text(
                draw, summary, SUMMARY_AREA,
                self.fonts['summary'], (220, 220, 220), max_lines=4
            )
            
            # Draw date
            date_str = datetime.now().strftime("%B %d, %Y")
            self._draw_text_centered(
                draw, date_str, DATE_AREA, 
                self.fonts['date'], (180, 180, 180)
            )
            
            # Draw decorative line
            draw.line([(100, 530), (980, 530)], fill=TEXT_ACCENT, width=2)
            
            # Draw source if provided
            if source:
                source_text = f"Source: {source}"
                draw.text((60, 850), source_text, font=self.fonts['source'], fill=(140, 140, 140))
            
            # Add watermark
            self._add_watermark(draw, img)
            
            # Determine output path
            if not output_path:
                today_dir = os.path.join(self.output_dir, "Today")
                os.makedirs(today_dir, exist_ok=True)
                
                safe_headline = ''.join(c if c.isalnum() or c == ' ' else '' for c in headline)
                safe_headline = safe_headline.replace(' ', '_')[:30]
                filename = f"Post{post_number}_{category}_{safe_headline}_Image.png"
                output_path = os.path.join(today_dir, filename)
            
            # Save as RGB (PNG doesn't need RGBA conversion but removes transparency)
            img_rgb = Image.new("RGB", img.size, (20, 25, 35))
            img_rgb.paste(img, mask=img.split()[3])
            img_rgb.save(output_path, "PNG", quality=95)
            
            print(f"   🖼️ Image generated: {os.path.basename(output_path)}")
            return output_path
            
        except Exception as e:
            print(f"   ❌ Image generation failed: {e}")
            # Return placeholder path
            return self._create_placeholder_image(post_number, category)
    
    def _draw_text_centered(self, draw: ImageDraw.Draw, text: str, 
                            area: Tuple[int, int, int, int],
                            font: ImageFont.FreeTypeFont, color: Tuple[int, int, int]):
        """Draw text centered in an area"""
        left, top, right, bottom = area
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = left + (right - left - text_width) // 2
        y = top + (bottom - top - text_height) // 2
        
        draw.text((x, y), text, font=font, fill=color)
    
    def _draw_multiline_text(self, draw: ImageDraw.Draw, text: str,
                             area: Tuple[int, int, int, int],
                             font: ImageFont.FreeTypeFont, 
                             color: Tuple[int, int, int],
                             max_lines: int = 3):
        """Draw multiline text with wrapping"""
        left, top, right, bottom = area
        max_width = right - left
        
        # Calculate approximate characters per line
        test_text = "A" * 20
        bbox = draw.textbbox((0, 0), test_text, font=font)
        char_width = (bbox[2] - bbox[0]) / 20
        chars_per_line = int(max_width / char_width)
        
        # Wrap text
        lines = wrap(text, width=chars_per_line)[:max_lines]
        
        # Get line height
        bbox = draw.textbbox((0, 0), "Ay", font=font)
        line_height = bbox[3] - bbox[1] + 8
        
        # Calculate starting Y to center vertically
        total_height = len(lines) * line_height
        y = top + (bottom - top - total_height) // 2
        
        for line in lines:
            # Center each line
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = left + (max_width - text_width) // 2
            
            draw.text((x, y), line, font=font, fill=color)
            y += line_height
    
    def _draw_category_badge(self, draw: ImageDraw.Draw, category: str,
                             color: Tuple[int, int, int]):
        """Draw category badge"""
        text = category.upper()
        bbox = draw.textbbox((0, 0), text, font=self.fonts['category'])
        text_width = bbox[2] - bbox[0]
        
        # Badge position (centered under brand)
        badge_x = (IMAGE_SIZE[0] - text_width - 40) // 2
        badge_y = 185
        
        # Draw badge background
        draw.rounded_rectangle(
            [badge_x, badge_y, badge_x + text_width + 40, badge_y + 50],
            radius=25, fill=color
        )
        
        # Draw badge text
        draw.text((badge_x + 20, badge_y + 10), text, 
                  font=self.fonts['category'], fill=TEXT_WHITE)
    
    def _add_watermark(self, draw: ImageDraw.Draw, img: Image.Image):
        """Add Modern_USA_News watermark to bottom-right corner"""
        watermark_text = "Modern_USA_News"
        
        try:
            # Get text size
            bbox = draw.textbbox((0, 0), watermark_text, font=self.fonts['source'])
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Position at bottom-right with padding
            padding = 20
            x = IMAGE_SIZE[0] - text_width - padding
            y = IMAGE_SIZE[1] - text_height - padding
            
            # Draw shadow for visibility
            shadow_color = (0, 0, 0, 180)
            draw.text((x + 2, y + 2), watermark_text, font=self.fonts['source'], 
                      fill=(0, 0, 0))
            
            # Draw watermark text with semi-transparency effect (white with slight transparency)
            watermark_color = (255, 255, 255)  # White for visibility
            draw.text((x, y), watermark_text, font=self.fonts['source'], 
                      fill=watermark_color)
            
            # Also draw a small "©" symbol
            draw.text((x - 20, y), "©", font=self.fonts['source'], fill=watermark_color)
            
        except Exception as e:
            # Watermark is non-critical, continue if it fails
            pass
    
    def _create_placeholder_image(self, post_number: int, category: str) -> str:
        """Create a simple placeholder when main generation fails"""
        try:
            img = Image.new("RGB", IMAGE_SIZE, BACKGROUND_COLOR)
            draw = ImageDraw.Draw(img)
            
            # Simple text
            message = f"Post #{post_number}\n\nNews Image\n\n{category}"
            draw.text((IMAGE_SIZE[0]//2 - 100, IMAGE_SIZE[1]//2 - 50), 
                      message, fill=TEXT_WHITE)
            
            # Save
            today_dir = os.path.join(self.output_dir, "Today")
            os.makedirs(today_dir, exist_ok=True)
            path = os.path.join(today_dir, f"Post{post_number}_placeholder.png")
            img.save(path, "PNG")
            
            return path
        except:
            return ""
    
    def batch_generate(self, posts: list) -> int:
        """
        Generate images for multiple posts
        
        Args:
            posts: List of dicts with 'headline', 'summary', 'category', etc.
            
        Returns:
            Number of successfully generated images
        """
        success_count = 0
        
        for i, post in enumerate(posts, 1):
            try:
                self.generate_image(
                    headline=post.get('headline', 'Breaking News'),
                    summary=post.get('summary', post.get('image_summary', '')),
                    category=post.get('category', 'General'),
                    post_number=i,
                    source=post.get('source', '')
                )
                success_count += 1
            except Exception as e:
                print(f"   ⚠️ Failed to generate image {i}: {e}")
                continue
        
        return success_count


if __name__ == "__main__":
    # Test image generation
    generator = FreeImageGenerator()
    
    test_posts = [
        {
            "headline": "Biden Announces Major Economic Policy Changes",
            "summary": "The administration unveiled sweeping reforms targeting inflation and job growth across key sectors.",
            "category": "Politics",
            "source": "CNN"
        },
        {
            "headline": "Stock Market Reaches Record High Amid Tech Rally",
            "summary": "Wall Street sees unprecedented gains as technology stocks surge following strong earnings reports.",
            "category": "Economy",
            "source": "Reuters"
        }
    ]
    
    print("\n🖼️ Testing image generation...")
    count = generator.batch_generate(test_posts)
    print(f"\n✅ Generated {count} images successfully")
