"""
Fetch RSS feeds and extract article information
"""

import feedparser
import logging
from datetime import datetime, timedelta
from config import RSS_FEEDS, LOG_FILE, DEBUG_MODE

# Set up logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def fetch_all_articles(hours_back=24):
    """
    Fetch articles from all RSS feeds from the last N hours
    
    Args:
        hours_back (int): How many hours back to look for articles (default: 24)
    
    Returns:
        list: List of article dictionaries with keys:
              - title: Article title
              - link: URL to article
              - source: News source name
              - published: Publication date (string)
              - description: Brief article summary
    """
    
    articles = []
    cutoff_time = datetime.now() - timedelta(hours=hours_back)
    
    logger.info(f"Fetching articles from last {hours_back} hours...")
    
    # Go through each news source
    for source_name, feed_urls in RSS_FEEDS.items():
        for feed_url in feed_urls:
            try:
                logger.info(f"Fetching from {source_name}: {feed_url}")
                
                # Parse the RSS feed
                feed = feedparser.parse(feed_url)
                
                # Get articles from this feed
                for entry in feed.entries:
                    try:
                        # Extract article information
                        article = {
                            'title': entry.get('title', 'No title'),
                            'link': entry.get('link', ''),
                            'source': source_name,
                            'published': entry.get('published', ''),
                            'description': entry.get('summary', '')[:500],  # First 500 chars
                        }
                        
                        articles.append(article)
                        
                    except Exception as e:
                        logger.warning(f"Error processing article from {source_name}: {e}")
                        continue
                
                logger.info(f"✓ Successfully fetched {len(feed.entries)} articles from {source_name}")
                
            except Exception as e:
                logger.error(f"Error fetching RSS feed {feed_url}: {e}")
                continue
    
    logger.info(f"✓ Total articles fetched: {len(articles)}")
    return articles


if __name__ == '__main__':
    # Test: fetch articles from last 24 hours
    articles = fetch_all_articles(hours_back=24)
    
    print(f"\n=== Fetched {len(articles)} Articles ===\n")
    for i, article in enumerate(articles[:5], 1):  # Show first 5
        print(f"{i}. {article['source']}: {article['title'][:60]}...")
        print(f"   Link: {article['link']}\n")
