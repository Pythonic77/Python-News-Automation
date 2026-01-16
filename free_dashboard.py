"""
Flask Dashboard for Modern_USA_News (FREE Version)
Simple web interface to view and manage daily posts
Basic UI - Focus on functionality over design
"""

from flask import Flask, render_template, jsonify, send_file, request
import os
import json
from datetime import datetime
from output_manager import OutputManager
from rss_collector import RSSCollector
from news_ranker import NewsRanker

app = Flask(__name__)

# Initialize managers (lazy loading)
_output_manager = None
_collector = None
_ranker = None

def get_output_manager():
    global _output_manager
    if _output_manager is None:
        _output_manager = OutputManager()
    return _output_manager

def get_collector():
    global _collector
    if _collector is None:
        try:
            _collector = RSSCollector()
        except:
            pass
    return _collector

def get_ranker():
    global _ranker
    if _ranker is None:
        try:
            _ranker = NewsRanker()
        except:
            pass
    return _ranker


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/posts')
def get_posts():
    """Get today's posts"""
    try:
        output = get_output_manager()
        posts = output.get_today_posts()
        
        # Add file existence checks
        for post in posts:
            files = post.get('files', {})
            file_status = {}
            for file_type, file_path in files.items():
                file_status[file_type] = {
                    'path': file_path,
                    'exists': os.path.exists(file_path) if file_path else False
                }
            post['file_status'] = file_status
        
        return jsonify({
            'success': True,
            'date': output.date_str,
            'count': len(posts),
            'posts': posts
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'count': 0,
            'posts': []
        })


@app.route('/api/post/<int:post_num>')
def get_post_detail(post_num):
    """Get detailed info for a specific post"""
    try:
        output = get_output_manager()
        posts = output.get_today_posts()
        
        post = next((p for p in posts if p['number'] == post_num), None)
        
        if not post:
            return jsonify({'success': False, 'error': 'Post not found'}), 404
        
        return jsonify({
            'success': True,
            'post': post
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/post/<int:post_num>/content/<content_type>')
def get_post_content(post_num, content_type):
    """Get specific content for a post"""
    try:
        output = get_output_manager()
        posts = output.get_today_posts()
        
        post = next((p for p in posts if p['number'] == post_num), None)
        
        if not post:
            return jsonify({'success': False, 'error': 'Post not found'}), 404
        
        file_path = post.get('files', {}).get(content_type)
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            'success': True,
            'content': content,
            'post_number': post_num,
            'content_type': content_type
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/post/<int:post_num>/image')
def get_post_image(post_num):
    """Serve post image"""
    try:
        output = get_output_manager()
        image_path = os.path.join(output.today_dir, f"post_{post_num}_image.png")
        
        if os.path.exists(image_path):
            return send_file(image_path, mimetype='image/png')
        else:
            return "Image not found", 404
            
    except Exception as e:
        return str(e), 500


@app.route('/api/download/<int:post_num>/<content_type>')
def download_file(post_num, content_type):
    """Download a specific file"""
    try:
        output = get_output_manager()
        posts = output.get_today_posts()
        
        post = next((p for p in posts if p['number'] == post_num), None)
        
        if not post:
            return "Post not found", 404
        
        file_path = post.get('files', {}).get(content_type)
        
        if not file_path or not os.path.exists(file_path):
            return "File not found", 404
        
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        return str(e), 500


@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    try:
        output = get_output_manager()
        collector = get_collector()
        ranker = get_ranker()
        
        # Collector stats
        collector_stats = {}
        if collector:
            try:
                collector_stats = collector.get_stats()
            except:
                pass
        
        # Ranker stats
        daily_summary = {}
        if ranker:
            try:
                daily_summary = ranker.get_daily_summary()
            except:
                pass
        
        # Output stats
        posts = output.get_today_posts()
        summary = output.get_post_summary()
        
        return jsonify({
            'success': True,
            'date': output.date_str,
            'stats': {
                'total_articles': collector_stats.get('total_articles', 0),
                'us_related': collector_stats.get('us_related', 0),
                'active_sources': collector_stats.get('active_sources', 0),
                'posts_ready': len(posts),
                'posts_with_images': summary.get('posts_with_images', 0),
                'categories': summary.get('categories', {})
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'stats': {}
        })


@app.route('/api/report')
def get_report():
    """Get daily report"""
    try:
        output = get_output_manager()
        report_path = os.path.join(output.today_dir, "daily_report.txt")
        
        if os.path.exists(report_path):
            with open(report_path, 'r', encoding='utf-8') as f:
                report = f.read()
            return jsonify({'success': True, 'report': report})
        else:
            # Generate on the fly
            report = output.create_daily_report()
            return jsonify({'success': True, 'report': report})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/dates')
def get_available_dates():
    """Get list of available date folders"""
    try:
        output = get_output_manager()
        dates = []
        
        for folder in sorted(os.listdir(output.base_dir), reverse=True):
            folder_path = os.path.join(output.base_dir, folder)
            if os.path.isdir(folder_path) and folder != "archive":
                # Check if it's a date folder
                try:
                    datetime.strptime(folder, '%Y-%m-%d')
                    # Count posts
                    post_count = len([f for f in os.listdir(folder_path) if f.endswith('_meta.json')])
                    dates.append({
                        'date': folder,
                        'post_count': post_count,
                        'is_today': folder == output.date_str
                    })
                except ValueError:
                    continue
        
        return jsonify({'success': True, 'dates': dates})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'dates': []})


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print(" 🌐 Modern_USA_News Dashboard")
    print("=" * 50)
    print(" 📍 Open http://localhost:5000 in your browser")
    print(" 💡 Press Ctrl+C to stop")
    print("=" * 50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
