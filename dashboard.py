"""
Web Dashboard for reviewing generated Instagram posts
"""

from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import os
from config import OUTPUT_DIR

app = Flask(__name__)

# Ensure output dir exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def index():
    # List all dates (folders)
    dates = sorted([d for d in os.listdir(OUTPUT_DIR) if os.path.isdir(os.path.join(OUTPUT_DIR, d))], reverse=True)
    
    selected_date = request.args.get('date')
    if not selected_date and dates:
        selected_date = dates[0]
        
    posts = []
    if selected_date:
        date_path = os.path.join(OUTPUT_DIR, selected_date)
        if os.path.exists(date_path):
            files = sorted(os.listdir(date_path))
            # Group jpg and txt files
            images = [f for f in files if f.endswith('.jpg')]
            
            for img in images:
                base_name = os.path.splitext(img)[0]
                txt_file = base_name + '.txt'
                
                caption = ""
                if txt_file in files:
                    with open(os.path.join(date_path, txt_file), 'r', encoding='utf-8') as f:
                        caption = f.read()
                
                posts.append({
                    'image': img,
                    'caption': caption,
                    'date': selected_date,
                    'base_name': base_name
                })
    
    return render_template('dashboard.html', dates=dates, selected_date=selected_date, posts=posts)

@app.route('/image/<date>/<filename>')
def serve_image(date, filename):
    return send_from_directory(os.path.join(OUTPUT_DIR, date), filename)

@app.route('/delete/<date>/<filename>')
def delete_post(date, filename):
    # filename is the base name without extension
    dir_path = os.path.join(OUTPUT_DIR, date)
    
    jpg_path = os.path.join(dir_path, filename + ".jpg")
    txt_path = os.path.join(dir_path, filename + ".txt")
    
    if os.path.exists(jpg_path):
        os.remove(jpg_path)
    if os.path.exists(txt_path):
        os.remove(txt_path)
        
    return redirect(url_for('index', date=date))

if __name__ == '__main__':
    print("Starting dashboard on http://localhost:5000")
    app.run(debug=True, port=5000)
