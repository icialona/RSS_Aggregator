"""
Match articles to customers based on name, industry, and keywords
"""

import csv
import logging
from difflib import SequenceMatcher
from config import LOG_FILE, DEBUG_MODE

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


def load_customers(csv_file='customers.csv'):
    """
    Load customer list from CSV file
    
    Args:
        csv_file (str): Path to customers CSV file
    
    Returns:
        list: List of customer dictionaries with keys:
              - name: Customer name
              - industry: Industry sector
              - ticker: Stock ticker
              - keywords: Comma-separated keywords
    """
    customers = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                customer = {
                    'name': row['Customer Name'].strip(),
                    'industry': row['Industry'].strip(),
                    'ticker': row['Ticker'].strip(),
                    'keywords': [k.strip() for k in row['Keywords'].split(';')],
                }
                customers.append(customer)
                logger.info(f"Loaded customer: {customer['name']}")
        
        logger.info(f"✓ Successfully loaded {len(customers)} customers")
        return customers
        
    except FileNotFoundError:
        logger.error(f"Customer file not found: {csv_file}")
        return []
    except Exception as e:
        logger.error(f"Error loading customers: {e}")
        return []


def text_similarity(text1, text2):
    """
    Calculate similarity between two texts (0 to 1)
    0 = completely different
    1 = identical
    """
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def match_article_to_customer(article, customer):
    """
    Check if an article is relevant to a customer
    Returns a similarity score (0 to 1)
    """
    
    article_text = f"{article['title']} {article['description']}".lower()
    match_score = 0
    
    # 1. Check for customer name (highest priority)
    if text_similarity(article_text, customer['name']) > 0.5:
        match_score = max(match_score, 0.9)
        logger.debug(f"Match: Found customer name in article")
    
    # 2. Check for industry keywords (medium priority)
    if text_similarity(article_text, customer['industry']) > 0.6:
        match_score = max(match_score, 0.6)
        logger.debug(f"Match: Found industry '{customer['industry']}' in article")
    
    # 3. Check for ticker (high priority if found)
    if customer['ticker'] in article_text:
        match_score = max(match_score, 0.8)
        logger.debug(f"Match: Found ticker '{customer['ticker']}' in article")
    
    # 4. Check for keywords (medium-high priority)
    for keyword in customer['keywords']:
        if len(keyword) > 2:  # Ignore very short keywords
            if text_similarity(keyword.lower(), article_text) > 0.7:
                match_score = max(match_score, 0.7)
                logger.debug(f"Match: Found keyword '{keyword}' in article")
            elif keyword.lower() in article_text:
                match_score = max(match_score, 0.65)
                logger.debug(f"Match: Found keyword '{keyword}' in article")
    
    return match_score


def find_matching_articles(articles, customers, threshold=0.5):
    """
    Find which articles are relevant to which customers
    
    Args:
        articles (list): List of article dictionaries
        customers (list): List of customer dictionaries
        threshold (float): Minimum match score to include (0 to 1)
    
    Returns:
        dict: Dictionary with structure:
              {
                'Customer Name': [
                    {
                        'article': {...},
                        'match_score': 0.85
                    }
                ]
              }
    """
    
    results = {}
    
    for customer in customers:
        results[customer['name']] = []
    
    # Check each article against each customer
    for article in articles:
        for customer in customers:
            match_score = match_article_to_customer(article, customer)
            
            # If match score is high enough, add to results
            if match_score >= threshold:
                results[customer['name']].append({
                    'article': article,
                    'match_score': match_score
                })
                logger.info(f"✓ Match found: {customer['name']} - {article['title'][:50]}...")
    
    return results


if __name__ == '__main__':
    # Test: load customers and match (you need to run fetch_rss.py first)
    from fetch_rss import fetch_all_articles
    
    customers = load_customers()
    articles = fetch_all_articles()
    matches = find_matching_articles(articles, customers, threshold=0.5)
    
    print("\n=== Matching Results ===\n")
    for customer_name, matched_articles in matches.items():
        if matched_articles:
            print(f"📰 {customer_name}: {len(matched_articles)} matching articles")
            for match in matched_articles[:2]:  # Show first 2
                print(f"   - {match['article']['title'][:60]}...")
                print(f"     Score: {match['match_score']:.2f}\n")
