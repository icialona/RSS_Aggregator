# RSS Aggregator for Credit Analysts 📰

A simple Python tool that automatically fetches news from financial RSS feeds (Reuters, Bloomberg, Financial Times) and emails you a daily summary of articles relevant to your customers.

## Features ✨

- 📡 Fetches news from multiple financial RSS feeds
- 🎯 Intelligently matches articles to your customers (by name, industry, keywords, ticker)
- 📧 Sends daily email summaries via Outlook
- ⏰ Automatic scheduling (runs daily at 9:00 AM)
- 📊 Shows match scores for relevance
- 🔍 Debug logging for troubleshooting

## Setup Guide 🚀

### 1. Install Python (if needed)
- Download from: https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### 2. Install Dependencies

Open a terminal/command prompt and run:
```bash
pip install -r requirements.txt
```

### 3. Configure Your Settings

**Edit `config.py`:**

#### Step A: Add your email credentials
```python
EMAIL_SENDER = 'your-outlook-email@outlook.com'
EMAIL_PASSWORD = 'your-outlook-password'
EMAIL_RECIPIENT = 'where-to-send@outlook.com'
```

**Important for Outlook:**
- If you have 2-factor authentication enabled, you need to create an **App Password**
- Instructions: https://support.microsoft.com/en-us/account-billing/using-app-passwords-with-two-step-verification

#### Step B: Customize your customer list
Edit `customers.csv` with your actual customers:
```
Customer Name,Industry,Ticker,Keywords,Country
Your Company,Technology,TICKER,keyword1;keyword2,USA
```

### 4. Test It Works!

Run the aggregation once to test:
```bash
python main.py --once
```

This will:
- Load your customers
- Fetch latest news
- Match articles
- Send a test email

**Check your inbox!** 📬

### 5. Set Up Daily Scheduling

**Option A: Run as scheduled task (Recommended)**

Edit `main.py` and change:
```python
SUMMARY_TIME = '09:00'  # Change to your preferred time
```

Then run:
```bash
python main.py
```

This will run forever and send emails daily at 9:00 AM.

**Option B: Windows Task Scheduler**

1. Open Task Scheduler
2. Create a new task
3. Trigger: Daily at 9:00 AM
4. Action: Run `python C:\path\to\main.py`

**Option C: Mac/Linux Cron**

Run `crontab -e` and add:
```
0 9 * * * cd /path/to/RSS_Aggregator && python main.py --once
```

## Project Structure 📁

```
RSS_Aggregator/
├── config.py          ← Your settings (email, RSS feeds, customers)
├── customers.csv      ← Your customer list (edit this!)
├── fetch_rss.py       ← Fetches articles from RSS feeds
├── match_news.py      ← Matches articles to customers
├── send_email.py      ← Sends email summaries
├── main.py            ← Main orchestration script
├── requirements.txt   ← Python dependencies
├── rss_aggregator.log ← Debug log file (created automatically)
└── README.md          ← This file
```

## How It Works 🔄

1. **Fetch** → Downloads latest articles from financial news sources
2. **Match** → Checks each article against your customer list:
   - Looks for customer names
   - Checks industry keywords
   - Searches for stock tickers
   - Finds custom keywords
3. **Score** → Gives each match a relevance score (0-100%)
4. **Email** → Sends formatted HTML email with all matches

## Customization 🎨

### Add more RSS feeds

Edit `config.py`:
```python
RSS_FEEDS = {
    'Your Source': [
        'https://feeds.example.com/news',
        'https://feeds.example.com/finance',
    ]
}
```

### Adjust matching sensitivity

In `config.py`, change:
```python
MATCH_THRESHOLD = 0.5  # 0.3 = more matches, 0.7 = stricter
```

### Change email send time

In `config.py`:
```python
SUMMARY_TIME = '09:00'  # Change to '14:30' for 2:30 PM, etc.
```

## Troubleshooting 🔧

### Email not sending?

1. **Check email/password** in `config.py`
2. **If using Outlook**, make sure to use an **App Password**, not your regular password
3. Check `rss_aggregator.log` for errors
4. Try running: `python main.py --once` to see error messages

### No articles found?

- The RSS feeds might be down
- Check your internet connection
- Try running: `python fetch_rss.py` to test RSS fetching

### Not matching any articles?

1. Check `customers.csv` - make sure customer names/keywords are correct
2. Lower `MATCH_THRESHOLD` in `config.py` (try 0.3 instead of 0.5)
3. Run: `python match_news.py` to test matching logic

### Check logs

All activities are logged to `rss_aggregator.log`. Open it to see what's happening:
```bash
tail -f rss_aggregator.log  # Mac/Linux
type rss_aggregator.log     # Windows
```

## Advanced Usage 💻

### Run in background (Windows)

Create a file called `run_background.bat`:
```batch
@echo off
python main.py
pause
```

Double-click it to run.

### Send test email manually

```python
from fetch_rss import fetch_all_articles
from match_news import load_customers, find_matching_articles
from send_email import send_email

customers = load_customers()
articles = fetch_all_articles()
matches = find_matching_articles(articles, customers)
send_email(matches)
```

## Tips 💡

- **Keywords**: Add stock ticker symbols (AAPL, MSFT) to keywords for better matching
- **Multiple sources**: Add the same customer with slight name variations to catch more articles
- **Testing**: Always test with `python main.py --once` before scheduling
- **Email size**: Very old RSS feeds might return large results. Adjust `hours_back` in `fetch_rss.py`

## Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Edit `config.py` with your email
3. ✅ Edit `customers.csv` with your customers
4. ✅ Test: `python main.py --once`
5. ✅ Set up scheduling (Task Scheduler or cron)

## Questions? 🤔

The code is heavily commented. Check the `.py` files to understand how each part works.

Happy reporting! 📊
