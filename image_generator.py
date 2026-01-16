"""
Image Generator for Instagram News Posts
Uses static background and typography.
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from config import CATEGORIES, FONTS, POST_WIDTH, POST_HEIGHT, CHANNEL_NAME

class ImageGenerator:
    def __init__(self):
        self.width = POST_WIDTH
        self.height = POST_HEIGHT
        self.margin = 80
        self.assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        self.bg_path = os.path.join(self.assets_dir, "background.png")
        
    def _get_font(self, font_name: str, size: int):
        try:
            return ImageFont.truetype(font_name, size)
        except OSError:
            try:
                # Windows fallback
                return ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", size)
            except OSError:
                return ImageFont.load_default()

    def generate_post(self, article: dict, hook: str, output_path: str):
        """Generate the post using static background and text hook"""
        category = article.get("category", "general")
        style = CATEGORIES.get(category, CATEGORIES["general"])
        
        # 1. Load Background
        if os.path.exists(self.bg_path):
            img = Image.open(self.bg_path).convert("RGBA")
            img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
        else:
            # Fallback
            img = Image.new('RGB', (self.width, self.height), "#111827")
            
        draw = ImageDraw.Draw(img)
        
        # 2. Draw Category Badge
        cat_text = style["name"].upper()
        cat_color = style["colors"]["primary"]
        
        # Top Left Badge
        font_cat = self._get_font("arialbd.ttf", 36)
        draw.rounded_rectangle(
            [self.margin, self.margin, self.margin + 300, self.margin + 60],
            radius=10, 
            fill=cat_color
        )
        draw.text((self.margin + 20, self.margin + 10), cat_text, font=font_cat, fill="white")
        
        # 3. Draw The Hook (Center)
        # Big bold typography
        # Calculate dynamic font size based on length
        font_size = 110
        if len(hook) > 20: font_size = 90
        if len(hook) > 40: font_size = 70
        
        font_hook = self._get_font("arialbd.ttf", font_size)
        
        # Wrap text
        max_chars = 15
        if font_size < 100: max_chars = 20
        
        lines = textwrap.wrap(hook.upper(), width=max_chars)
        
        # Calculate vertical center
        total_height = len(lines) * (font_size + 10)
        start_y = (self.height - total_height) // 2
        
        for line in lines:
            # Drop shadow for depth
            draw.text((self.margin + 4, start_y + 4), line, font=font_hook, fill="#000000")
            # Main text
            draw.text((self.margin, start_y), line, font=font_hook, fill="white")
            start_y += font_size + 15
            
        # 4. Footer CTA
        cta_text = "READ CAPTION FOR FULL STORY ⤵"
        font_cta = self._get_font("arial.ttf", 40)
        
        # Draw CTA at bottom
        text_bbox = draw.textbbox((0,0), cta_text, font=font_cta)
        text_w = text_bbox[2] - text_bbox[0]
        x_cta = (self.width - text_w) // 2
        
        draw.text((x_cta, self.height - 150), cta_text, font=font_cta, fill="#AAAAAA")
        
        # Save
        img = img.convert("RGB")
        img.save(output_path, quality=95)
