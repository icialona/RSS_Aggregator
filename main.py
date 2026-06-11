"""
Main orchestration script - brings everything together
Fetches RSS -> Matches articles -> Sends email
"""

import logging
import schedule
import time
from datetime import datetime
from fetch_rss import fetch_all_articles
from match_news import load_customers, find_matching_articles
from send_email import send_email
from config import LOG_FILE, DEBUG_MODE, SUMMARY_TIME, CHECK_INTERVAL, MATCH_THRESHOLD

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


def run_daily_aggregation():
    """
    Main function: fetch articles, match to customers, send email
    """
    
    logger.info("="*60)
    logger.info("🚀 Starting Daily RSS Aggregation")
    logger.info("="*60)
    
    try:
        # Step 1: Load customer list
        logger.info("\n[1/4] Loading customers...")
        customers = load_customers('customers.csv')
        
        if not customers:
            logger.error("❌ No customers loaded. Aborting.")
            return False
        
        logger.info(f"✓ Loaded {len(customers)} customers")
        
        # Step 2: Fetch articles from RSS feeds
        logger.info("\n[2/4] Fetching articles from RSS feeds...")
        articles = fetch_all_articles(hours_back=24)
        
        if not articles:
            logger.warning("⚠ No articles found. Email not sent.")
            return False
        
        logger.info(f"✓ Fetched {len(articles)} total articles")
        
        # Step 3: Match articles to customers
        logger.info(f"\n[3/4] Matching articles to customers (threshold: {MATCH_THRESHOLD})...")
        matches = find_matching_articles(articles, customers, threshold=MATCH_THRESHOLD)
        
        # Count matches
        total_matches = sum(len(m) for m in matches.values())
        logger.info(f"✓ Found {total_matches} matching articles")
        
        # Show summary
        for customer_name, matched_articles in matches.items():
            if matched_articles:
                logger.info(f"  - {customer_name}: {len(matched_articles)} articles")
        
        # Step 4: Send email
        logger.info("\n[4/4] Sending email summary...")
        success = send_email(matches)
        
        if success:
            logger.info("\n" + "="*60)
            logger.info("✓ Daily aggregation completed successfully!")
            logger.info("="*60)
            return True
        else:
            logger.error("\n" + "="*60)
            logger.error("❌ Failed to send email")
            logger.error("="*60)
            return False
            
    except Exception as e:
        logger.error(f"❌ Error in daily aggregation: {e}", exc_info=True)
        return False


def schedule_daily_task():
    """
    Schedule the aggregation to run daily at specified time
    """
    logger.info(f"📅 Scheduling daily task at {SUMMARY_TIME}")
    schedule.every().day.at(SUMMARY_TIME).do(run_daily_aggregation)
    
    logger.info("Starting scheduler. Press Ctrl+C to stop.\n")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


def run_once():
    """
    Run aggregation once (useful for testing)
    """
    logger.info("Running aggregation once for testing...")
    run_daily_aggregation()


if __name__ == '__main__':
    import sys
    
    print("""
    ╔════════════════════════════════════════╗
    ║     RSS AGGREGATOR FOR CREDIT ANALYSTS ║
    ╚════════════════════════════════════════╝
    """)
    
    # Check if running as scheduler or one-time
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # Run once for testing
        print("Mode: Run Once (Testing)\n")
        run_once()
    else:
        # Run as scheduled task
        print("Mode: Scheduled Daily Task\n")
        try:
            schedule_daily_task()
        except KeyboardInterrupt:
            logger.info("\nScheduler stopped by user")
