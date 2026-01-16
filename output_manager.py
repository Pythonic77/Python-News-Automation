"""
Enhanced Output Manager for Modern_USA_News
Manages file generation with date-based folders and images
"""

import os
import json
import shutil
from datetime import datetime
from typing import Dict, List, Optional
from rss_config import OUTPUT_DIR


class OutputManager:
    """
    Manages all output files for the automation system
    Features:
    - Date-based folder structure: ModernUSANews/2026-01-14/
    - Image integration
    - Meta JSON files
    - Archiving
    """
    
    def __init__(self, output_dir: str = OUTPUT_DIR):
        self.base_dir = output_dir
        self.date_str = datetime.now().strftime('%Y-%m-%d')
        self.today_dir = os.path.join(output_dir, self.date_str)
        self.archive_dir = os.path.join(output_dir, "archive")
        self._init_directories()
        print(f"📁 Output Manager initialized: {self.today_dir}")
    
    def _init_directories(self):
        """Create output directory structure"""
        os.makedirs(self.today_dir, exist_ok=True)
        os.makedirs(self.archive_dir, exist_ok=True)
    
    def save_post(self, article: Dict, content: Dict, post_number: int) -> Dict[str, str]:
        """
        Save all technical files for a single post
        """
        files = {}
        base_name = f"post_{post_number}"
        
        # 1. Caption File
        caption_path = os.path.join(self.today_dir, f"{base_name}_caption.txt")
        with open(caption_path, 'w', encoding='utf-8') as f:
            f.write(content['caption'])
        files['caption'] = caption_path
        
        # 2. First Comment File
        comment_path = os.path.join(self.today_dir, f"{base_name}_first_comment.txt")
        with open(comment_path, 'w', encoding='utf-8') as f:
            f.write(content.get('first_comment', 'What do you think?'))
        files['first_comment'] = comment_path
        
        # 3. Image Prompt (Ollama generated)
        prompt_path = os.path.join(self.today_dir, f"{base_name}_image_prompt.txt")
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write(content.get('image_prompt', ''))
        files['image_prompt'] = prompt_path
        
        # 4. Hashtags
        hashtags_path = os.path.join(self.today_dir, f"{base_name}_hashtags.txt")
        with open(hashtags_path, 'w', encoding='utf-8') as f:
            f.write(content.get('hashtags', ''))
        files['hashtags'] = hashtags_path
        
        # 5. Meta JSON
        meta_path = os.path.join(self.today_dir, f"{base_name}_meta.json")
        meta_data = {
            "post_number": post_number,
            "generated_at": datetime.now().isoformat(),
            "headline": content.get('headline', ''),
            "category": content.get('category', 'General'),
            "source": article.get('source', 'Unknown'),
            "slides": content.get('slides', [])
        }
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta_data, f, indent=2, ensure_ascii=False)
        files['meta'] = meta_path
        
        print(f"   💾 Saved Post #{post_number} core data files")
        return files

    def save_carousel_images(self, post_number: int, image_paths: List[str]):
        """Copy carousel images to the post directory (already handled by generator usually)"""
        # Just a reference point for the controller
        print(f"   🖼️ Carousel images confirmed for Post #{post_number}: {len(image_paths)} slides")
    
    def _get_posting_time(self, post_number: int) -> str:
        """Generate suggested posting time based on engagement patterns"""
        # Best times for US news content (EST)
        posting_slots = [
            "07:00 AM EST",  # Morning commute
            "12:00 PM EST",  # Lunch break
            "05:00 PM EST",  # After work
            "08:00 PM EST",  # Evening
            "10:00 PM EST",  # Late night
            "09:00 AM EST",  # Mid-morning
            "03:00 PM EST"   # Afternoon
        ]
        
        index = (post_number - 1) % len(posting_slots)
        return posting_slots[index]
    
    def save_image(self, post_number: int, image_path: str) -> Optional[str]:
        """
        Copy generated image to output folder with correct naming
        """
        try:
            dest_path = os.path.join(self.today_dir, f"post_{post_number}_image.png")
            
            if os.path.exists(image_path) and image_path != dest_path:
                shutil.copy2(image_path, dest_path)
                print(f"   🖼️ Image saved: post_{post_number}_image.png")
                return dest_path
            elif os.path.exists(image_path):
                return image_path
            else:
                print(f"   ⚠️ Image file not found: {image_path}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error saving image: {e}")
            return None
    
    def clear_today(self):
        """Clear today's folder"""
        if os.path.exists(self.today_dir):
            for file in os.listdir(self.today_dir):
                file_path = os.path.join(self.today_dir, file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f"   ⚠️ Could not remove {file}: {e}")
        print("   🗑️ Cleared today's folder")
    
    def archive_old_folders(self, keep_days: int = 7):
        """Move old date folders to archive"""
        try:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=keep_days)
            
            for folder in os.listdir(self.base_dir):
                folder_path = os.path.join(self.base_dir, folder)
                
                # Check if it's a date folder
                if os.path.isdir(folder_path) and folder != "archive":
                    try:
                        folder_date = datetime.strptime(folder, '%Y-%m-%d')
                        if folder_date < cutoff_date:
                            # Move to archive
                            dest = os.path.join(self.archive_dir, folder)
                            shutil.move(folder_path, dest)
                            print(f"   📦 Archived: {folder}")
                    except ValueError:
                        # Not a date folder, skip
                        continue
                        
        except Exception as e:
            print(f"   ⚠️ Archive error: {e}")
    
    def get_today_posts(self) -> List[Dict]:
        """Get list of today's posts with all data"""
        posts = []
        
        if not os.path.exists(self.today_dir):
            return posts
        
        # Find all meta.json files
        for file in sorted(os.listdir(self.today_dir)):
            if file.endswith('_meta.json'):
                try:
                    meta_path = os.path.join(self.today_dir, file)
                    with open(meta_path, 'r', encoding='utf-8') as f:
                        meta = json.load(f)
                    
                    post_num = meta.get('post_number', 0)
                    base_name = f"post_{post_num}"
                    
                    post_data = {
                        'number': post_num,
                        'base_name': base_name,
                        'headline': meta.get('headline', 'N/A'),
                        'category': meta.get('category', 'General'),
                        'caption': '',
                        'hashtags': meta.get('hashtags', ''),
                        'posting_time': meta.get('posting_suggestion', ''),
                        'files': {
                            'image': os.path.join(self.today_dir, f"{base_name}_image.png"),
                            'caption': os.path.join(self.today_dir, f"{base_name}_caption.txt"),
                            'meta': meta_path,
                            'hashtags': os.path.join(self.today_dir, f"{base_name}_hashtags.txt"),
                            'image_prompt': os.path.join(self.today_dir, f"{base_name}_image_prompt.txt"),
                            'image_text': os.path.join(self.today_dir, f"{base_name}_image_text.txt")
                        },
                        'meta': meta
                    }
                    
                    # Read caption
                    caption_path = post_data['files']['caption']
                    if os.path.exists(caption_path):
                        with open(caption_path, 'r', encoding='utf-8') as f:
                            post_data['caption'] = f.read()
                    
                    posts.append(post_data)
                    
                except Exception as e:
                    print(f"   ⚠️ Error reading {file}: {e}")
                    continue
        
        # Sort by post number
        posts.sort(key=lambda x: x['number'])
        return posts
    
    def get_post_summary(self) -> Dict:
        """Get summary of today's posts"""
        posts = self.get_today_posts()
        
        summary = {
            'date': self.date_str,
            'total_posts': len(posts),
            'posts_with_images': 0,
            'categories': {},
            'posts': []
        }
        
        for post in posts:
            # Check for image
            image_path = post['files'].get('image', '')
            has_image = os.path.exists(image_path)
            if has_image:
                summary['posts_with_images'] += 1
            
            # Count categories
            cat = post.get('category', 'General')
            summary['categories'][cat] = summary['categories'].get(cat, 0) + 1
            
            # Add post info
            summary['posts'].append({
                'number': post['number'],
                'headline': post['headline'][:50] + '...' if len(post['headline']) > 50 else post['headline'],
                'category': cat,
                'has_image': has_image,
                'posting_time': post.get('posting_time', '')
            })
        
        return summary
    
    def create_daily_report(self) -> str:
        """Create a human-readable daily report"""
        summary = self.get_post_summary()
        
        report = []
        report.append("=" * 60)
        report.append(f"MODERN USA NEWS - DAILY REPORT")
        report.append(f"Date: {summary['date']}")
        report.append("=" * 60)
        report.append(f"\nTotal Posts: {summary['total_posts']}")
        report.append(f"Posts with Images: {summary['posts_with_images']}")
        report.append(f"\nCategories:")
        
        for cat, count in summary['categories'].items():
            report.append(f"  - {cat}: {count}")
        
        report.append(f"\n{'=' * 60}")
        report.append("POST DETAILS")
        report.append("=" * 60)
        
        for post in summary['posts']:
            status = "✅" if post['has_image'] else "⚠️ (no image)"
            report.append(f"\n{status} Post #{post['number']}")
            report.append(f"   Headline: {post['headline']}")
            report.append(f"   Category: {post['category']}")
            report.append(f"   Post at: {post['posting_time']}")
        
        report.append("\n" + "=" * 60)
        report.append("All files saved in: " + self.today_dir)
        report.append("=" * 60)
        
        # Save report
        report_text = '\n'.join(report)
        report_path = os.path.join(self.today_dir, "daily_report.txt")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        return report_text


if __name__ == "__main__":
    # Test output manager
    manager = OutputManager()
    
    test_article = {
        "title": "Breaking: Major Economic Policy Announced",
        "description": "The administration unveiled sweeping changes to tax policy.",
        "source": "Reuters",
        "category": "Economy",
        "link": "https://example.com",
        "priority_score": 15
    }
    
    test_content = {
        "headline": "Major Tax Policy Changes Unveiled",
        "image_summary": "Administration announces sweeping tax reform affecting millions of Americans nationwide",
        "caption": "📰 BREAKING: Major policy changes announced today...\n\nThis is a test caption.\n\nWhat do you think?",
        "hashtags": "#Economy #TaxReform #USA #News #ModernUSANews",
        "keywords": "Tax, Economy, Reform",
        "category": "Economy"
    }
    
    print("\n💾 Testing file save...")
    files = manager.save_post(test_article, test_content, 1)
    
    print("\n📂 Saved files:")
    for file_type, path in files.items():
        exists = "✅" if os.path.exists(path) else "⏳"
        print(f"   {exists} {file_type}: {os.path.basename(path)}")
    
    print("\n📋 Today's Posts:")
    posts = manager.get_today_posts()
    for post in posts:
        print(f"   Post #{post['number']}: {post['headline']}")
    
    print("\n📊 Summary:")
    summary = manager.get_post_summary()
    print(f"   Total: {summary['total_posts']} posts")
