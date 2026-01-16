# Modern_USA_News - FREE Automation System
## Complete Setup Guide

---

## 🎯 Overview

This is a **100% FREE** automated news content system for Instagram. It uses:
- ✅ RSS feeds (no API costs)
- ✅ Local LLM with Ollama (free)
- ✅ HuggingFace API fallback (free tier)
- ✅ SQLite database (free)
- ✅ Flask dashboard (free)

**No paid APIs. No subscriptions. Fully automated.**

---

## 📋 Prerequisites

### Required:
1. **Python 3.8+**
2. **Ollama** (for local, free AI) - OPTIONAL but recommended

### Internet connection for:
- RSS feeds
- HuggingFace API (fallback only)

---

## 🚀 Installation

### Step 1: Install Python Dependencies

```powershell
cd d:\Ig-automation
pip install -r requirements_free.txt
```

### Step 2: Install Ollama (Optional but Recommended)

**Why Ollama?**
- 100% FREE
- Runs locally (no internet needed for AI)
- Fast & private
- Better than HuggingFace free tier

**Install:**
1. Download from: https://ollama.com/download
2. Install for Windows
3. Open terminal and run:

```powershell
ollama pull llama3.2
```

This downloads the Llama 3.2 model (~2GB). It's FREE and works offline!

**Alternative models:** (`ollama pull mistral` or `ollama pull phi3`)

### Step 3: (Optional) HuggingFace API as Fallback

If Ollama is not installed, the system will automatically use HuggingFace's free API.

**No setup needed!** The free tier works without an API key.

If you want better rate limits:
1. Sign up at https://huggingface.co (FREE)
2. Get your API token
3. Edit `rss_config.py` and set:
   ```python
   HUGGINGFACE_API_KEY = "your_token_here"
   ```

---

## 📖 Usage

### Option 1: Run Full Automation (Recommended)

Start the automation system that runs 24/7:

```powershell
python free_automation.py
```

This will:
- Collect news every 2 hours
- Generate 5 daily posts at 6:00 AM
- Save everything to `ModernUSANews/Today/` folder

**Leave it running!** Press Ctrl+C to stop.

---

### Option 2: Run Once (Manual Mode)

Just generate today's content once:

```powershell
python free_automation.py
```

The first run always generates content immediately, then waits for schedule.

---

### Option 3: Dashboard Only

Start the web dashboard to view existing posts:

```powershell
python free_dashboard.py
```

Then open: **http://localhost:5000**

---

## 📁 Output Structure

After running, you'll have:

```
ModernUSANews/
├── Today/
│   ├── Post1_Politics_[title]_ImageText.txt    ← Put this text on your image
│   ├── Post1_Politics_[title]_Caption.txt      ← Copy this for Instagram caption
│   ├── Post1_Politics_[title]_Hashtags.txt     ← Copy hashtags
│   ├── Post1_Politics_[title]_Info.txt         ← Full article info
│   ├── Post2_Economy_[title]_ImageText.txt
│   ├── ...
│   └── Post5_[...].txt
└── Archive/
    └── 2026-01-12/                             ← Previous days archived here
```

---

## 🎨 How to Post to Instagram

### Method 1: Manual Posting (Simple)

1. **Run automation:**
   ```powershell
   python free_automation.py
   ```

2. **Open dashboard:**
   ```powershell
   python free_dashboard.py
   ```
   Go to http://localhost:5000

3. **For each post:**
   - Click "📋 Copy Caption" → Paste in Instagram
   - Click "🖼️ Download Image Text" → Use text for your graphic
   - Click "#️⃣ Copy Hashtags" → Paste as first comment

4. **Create image:**
   - Use your Modern_USA_News background template
   - Add the headline and summary from `ImageText.txt`
   - Post!

---

### Method 2: Dashboard Workflow

1. Open dashboard: http://localhost:5000
2. You'll see 5 posts ready
3. Click any post to:
   - Copy caption (one click!)
   - Copy hashtags (one click!)
   - Download image text file
4. Use Canva/Photoshop to add text to your background
5. Post to Instagram

---

## 🤖 About the AI Models

### If Ollama is installed (Recommended):
- Uses **Llama 3.2** (FREE, local, fast)
- No internet needed
- Private & secure
- High quality captions

### If Ollama is NOT installed:
- Falls back to **HuggingFace API** (FREE tier)
- Requires internet
- Still produces great captions
- May have rate limits (but high enough for daily use)

### If both fail:
- Uses **template-based fallback**
- Still works!
- Captions are basic but functional

---

## 📊 System Features

### ✅ News Collection
- **7 major sources**: CNN, NBC, Fox, AP, Reuters, NYT, Politico
- **Automatic deduplication**: No repeats
- **US news filtering**: Only relevant stories
- **Smart ranking**: Prioritizes important news
- **Spam filtering**: Excludes gossip & clickbait

### ✅ Content Generation
- **Headlines**: Max 12 words, punchy
- **Image summaries**: Max 22 words, clear
- **Captions**: 4 paragraphs, professional
- **Hashtags**: 10 relevant tags
- **Keywords**: 3 trending keywords
- **Categories**: Auto-detected (Politics, Economy, etc.)

### ✅ Automation
- **Collects news**: Every 2 hours
- **Generates posts**: Daily at 6:00 AM (customizable)
- **Saves everything**: Organized folders
- **Archives old content**: Automatic

---

## ⚙️ Customization

### Change Schedule

Edit `free_automation.py`:

```python
# Collection frequency (default: 2 hours)
schedule.every(2).hours.do(bot.run_collection_only)

# Daily generation time (default: 6:00 AM)
schedule.every().day.at("06:00").do(bot.run_daily_cycle)
```

Change to your preferred times!

### Change Number of Posts

Edit `rss_config.py`:

```python
MAX_STORIES_PER_DAY = 5  # Change to 3, 7, 10, etc.
```

### Add More News Sources

Edit `rss_config.py` and add to `RSS_FEEDS`:

```python
"newsource": {
    "name": "Source Name",
    "feeds": {
        "top": "https://example.com/rss"
    }
}
```

---

## 🔧 Troubleshooting

### "No posts generated"
- Wait for news collection (2 hours initially)
- Or manually test: `python rss_collector.py`
- Check database: `news_database.db` should exist

### "Ollama not found"
- System will automatically use HuggingFace
- Install Ollama for better results (see Step 2 above)

### "Port 5000 already in use"
- Change port in `free_dashboard.py`:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)
  ```

### "HuggingFace rate limit"
- Install Ollama (no rate limits!)
- Or wait 1 hour and retry
- Or sign up for HF API token (free)

---

## 📝 Workflow Example

**Your Daily Routine (5 minutes total):**

1. **Morning**: Open dashboard → http://localhost:5000
2. **Review**: See 5 auto-generated posts
3. **Copy**: Click "Copy Caption" for Post #1
4. **Create**: Add headline to your Modern_USA_News background
5. **Post**: Upload to Instagram, paste caption
6. **Repeat**: For other 4 posts throughout the day

**System handles:**
- News collection ✅
- Content writing ✅
- Hashtag generation ✅
- File organization ✅

**You handle:**
- Creating the image (5 min per post)
- Posting to Instagram (1 min per post)

---

## 🎯 Next Steps

### After Installation:

1. **Test RSS Collection:**
   ```powershell
   python rss_collector.py
   ```
   Should collect 50-100+ articles

2. **Test Content Generation:**
   ```powershell
   python free_llm_writer.py
   ```
   Should generate sample content

3. **Generate First Batch:**
   ```powershell
   python free_automation.py
   ```
   Wait 1-2 minutes, check `ModernUSANews/Today/`

4. **Start Dashboard:**
   ```powershell
   python free_dashboard.py
   ```
   Open http://localhost:5000 and review!

---

## 💡 Pro Tips

### Improve Content Quality:
1. **Use Ollama** (local LLM) instead of HuggingFace
2. **Run multiple times** daily for more variety
3. **Edit captions** yourself for perfection
4. **Customize keywords** in `rss_config.py` for your audience

### Automate Completely:
1. **Keep script running** 24/7
2. Posts generate automatically at 6 AM
3. Just check dashboard daily and post!

### Scale Up:
- Increase `MAX_STORIES_PER_DAY` to 10-15
- Add more RSS sources
- Use better Ollama models (`ollama pull llama3.1:70b`)

---

## 📞 Support

### Files to check:
- `news_database.db` - All collected articles
- `ModernUSANews/Today/` - Today's posts
- Console output - Shows what's happening

### Test individual components:
```powershell
python rss_collector.py    # Test news collection
python news_ranker.py       # Test ranking
python free_llm_writer.py   # Test AI generation
python output_manager.py    # Test file output
```

---

## 🎉 You're All Set!

Run `python free_automation.py` and let it work for you!

Open the dashboard, copy content, create images, and post.

**Everything is FREE. Everything is automated. Everything is yours!** 🚀
