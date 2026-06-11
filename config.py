# Configuration file for RSS Aggregator

# ===== RSS FEEDS =====
# Financial news sources in RSS format
RSS_FEEDS = {
    'Reuters': [
        'https://www.reuters.com/finance',
        'https://feeds.reuters.com/reuters/businessNews',
    ],
    'Bloomberg': [
        'https://feeds.bloomberg.com/markets/news.rss',
        'https://feeds.bloomberg.com/top/news.rss',
    ],
    'Financial Times': [
        'https://feeds.ft.com/markets',
        'https://feeds.ft.com/world',
    ],
    'General': [
        'https://feeds.cnbc.com/cnbc/world/',
    ]
}

# ===== EMAIL SETTINGS =====
# How often to check for news (in hours)
CHECK_INTERVAL = 24

# Time to send daily summary (24-hour format)
SUMMARY_TIME = '09:00'

# Email configuration
EMAIL_SENDER = 'your-outlook-email@outlook.com'
EMAIL_PASSWORD = 'your-outlook-password'  # For app password, see: https://support.microsoft.com/en-us/account-billing/using-app-passwords-with-two-step-verification
EMAIL_SERVER = 'smtp-mail.outlook.com'
EMAIL_PORT = 587

# Who receives the summary
EMAIL_RECIPIENT = 'your-email@outlook.com'

# Email subject line
EMAIL_SUBJECT_TEMPLATE = 'Daily Customer News Summary - {date}'

# ===== NEWS MATCHING SETTINGS =====
# How many characters to keep from article description
DESCRIPTION_LENGTH = 200

# Minimum similarity score to match (0-1, where 1 is exact match)
MATCH_THRESHOLD = 0.3

# ===== LOGGING =====
LOG_FILE = 'rss_aggregator.log'
DEBUG_MODE = True
