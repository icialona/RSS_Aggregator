# QUICK START GUIDE 🚀

## What You Have

I've created a complete RSS Aggregator system with 8 Python files. Here's what each does:

### 📄 Core Files

| File | Purpose |
|------|---------|
| **main.py** | Master control - runs everything |
| **fetch_rss.py** | Downloads news articles from RSS feeds |
| **match_news.py** | Compares articles to your customer list |
| **send_email.py** | Sends the summary email via Outlook |
| **config.py** | Settings (email, feeds, times, customers path) |
| **customers.csv** | Your customer list (EDIT THIS!) |
| **requirements.txt** | Python packages needed |
| **README.md** | Full documentation |

---

## 3 Simple Steps to Get Started

### STEP 1: Install Python Packages
```bash
pip install -r requirements.txt
```
*This takes ~2 minutes*

### STEP 2: Edit config.py
Open `config.py` and fill in:
```python
EMAIL_SENDER = 'your-outlook@outlook.com'
EMAIL_PASSWORD = 'your-app-password'     # Use App Password from: https://support.microsoft.com/en-us/account-billing/using-app-passwords-with-two-step-verification
EMAIL_RECIPIENT = 'your-email@outlook.com'
```

### STEP 3: Customize customers.csv
Replace the sample customers with YOUR customers:
```
Customer Name,Industry,Ticker,Keywords,Country
Acme Corp,Manufacturing,ACM,supply chain;production,USA
Global Bank,Finance,GB,lending;mortgage,UK
```

---

## Test It (5 minutes)

Run this to test everything works:
```bash
python main.py --once
```

**What it does:**
1. Loads your customers ✓
2. Fetches latest news ✓
3. Matches to your customers ✓
4. Sends test email ✓

**Check your inbox!** You should get an email like:

```
📊 Daily Customer News Summary
Generated: 2024-01-15 10:30:00

📊 Acme Corp
- 3 relevant articles found
  • Article Title Here
    📅 2024-01-15
    (Match: 85%)

📊 Global Bank
- 1 relevant articles found
  • Article Title Here
    📅 2024-01-15
    (Match: 72%)
```

---

## Schedule It (Auto Daily Reports)

### Option A: Run Daily (easiest)
```bash
python main.py
```
This runs forever and sends emails at 9:00 AM every day.

### Option B: Windows Task Scheduler
1. Open Task Scheduler (search in Windows Start menu)
2. Create Basic Task
3. Name: "RSS Aggregator"
4. Trigger: Daily at 9:00 AM
5. Action: Start program
   - Program: `C:\Python39\python.exe` (or your Python path)
   - Arguments: `C:\path\to\main.py --once`

### Option C: Mac/Linux Cron
```bash
crontab -e
# Add this line (runs at 9 AM daily):
0 9 * * * cd /path/to/RSS_Aggregator && python main.py --once
```

---

## How It Actually Works 🔍

```
Every Day at 9:00 AM:

1️⃣  FETCH
    ↓ fetch_rss.py downloads latest news
    ↓ from Reuters, Bloomberg, Financial Times
    ↓ from the last 24 hours
    ↓ (300+ articles)

2️⃣  MATCH
    ↓ match_news.py reads customers.csv
    ↓ checks each article against each customer
    ↓ looks for: name, industry, ticker, keywords
    ↓ scores each match (0-100%)
    ↓ keeps articles above score threshold

3️⃣  EMAIL
    ↓ send_email.py formats nice HTML email
    ↓ shows article title, source, date, link
    ↓ sends via Outlook SMTP
    ↓ lands in your inbox!
```

---

## Customization Examples 🎨

### Add more RSS feeds
Edit `config.py`:
```python
RSS_FEEDS = {
    'Reuters': [...],
    'Bloomberg': [...],
    'My Custom Source': [
        'https://feeds.example.com/news',
        'https://feeds.example.com/finance',
    ]
}
```

### Make matching stricter/looser
Edit `config.py`:
```python
MATCH_THRESHOLD = 0.5  
# 0.3 = very loose (more articles)
# 0.5 = medium (default)
# 0.7 = very strict (fewer articles)
```

### Change email time
Edit `config.py`:
```python
SUMMARY_TIME = '14:30'  # Changes from 9:00 AM to 2:30 PM
```

### Add article details
Edit `config.py`:
```python
DESCRIPTION_LENGTH = 200  # Show first 200 chars of description
```

---

## Troubleshooting 🔧

### "Email not sending"
1. Check `config.py` - email and password correct?
2. Using Outlook? Did you create an **App Password**? (NOT your regular password)
3. Check `rss_aggregator.log` for error details
4. Try: `python main.py --once` to see error messages

### "No articles found"
- RSS feeds might be down
- Check internet connection
- Try: `python fetch_rss.py` to test RSS feeds alone

### "Not matching any customers"
1. Check `customers.csv` - names spelled correctly?
2. Try lowering `MATCH_THRESHOLD` to 0.3
3. Try: `python match_news.py` to test matching alone

### See what's happening
All activity is logged to `rss_aggregator.log`:
```bash
# Mac/Linux
tail -f rss_aggregator.log

# Windows - open the file in Notepad
```

---

## Pro Tips 💡

1. **Stock Tickers** - Add ticker symbols (AAPL, MSFT) to keywords for better matches
2. **Test First** - Always test with `python main.py --once` before scheduling
3. **Debug Mode** - Set `DEBUG_MODE = True` in `config.py` to see detailed logs
4. **Multiple Names** - Add customers with slight name variations to catch more articles
5. **RSS Feeds** - Can add industry-specific feeds to match better

---

## File-by-File Explanation 📚

### main.py
- Brain of the system
- Controls the flow: Fetch → Match → Email
- Can run once (`--once`) or continuously (daily at 9 AM)

### fetch_rss.py
- Downloads RSS feeds
- Extracts: title, link, source, date, description
- Returns list of articles

### match_news.py
- Loads customers.csv
- Compares each article to each customer
- Uses: name matching, industry, ticker, keywords
- Returns which articles match which customers

### send_email.py
- Creates nice HTML email format
- Connects to Outlook SMTP server
- Sends email with all matched articles

### config.py
- All settings in one place
- Email credentials (EDIT THIS!)
- RSS feeds list
- Matching sensitivity
- Send time

### customers.csv
- Your customer data
- Columns: Name, Industry, Ticker, Keywords, Country
- Keywords separated by semicolon (;)

---

## What's Next?

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Edit `config.py` (add your email)
3. ✅ Edit `customers.csv` (add your customers)
4. ✅ Test: `python main.py --once`
5. ✅ Schedule (Task Scheduler or cron)
6. ✅ Done! Emails arrive daily at 9 AM 🎉

---

## Questions?

All code is **heavily commented** - open any .py file and read the explanations!

Each function has a docstring explaining what it does.

Good luck! 📊
