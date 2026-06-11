"""
Send email summary of matched articles
"""

import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import (
    EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_SERVER, EMAIL_PORT,
    EMAIL_RECIPIENT, EMAIL_SUBJECT_TEMPLATE, DESCRIPTION_LENGTH,
    LOG_FILE, DEBUG_MODE
)

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


def create_email_body(matches_by_customer):
    """
    Create HTML email body from matched articles
    
    Args:
        matches_by_customer (dict): Results from find_matching_articles()
    
    Returns:
        str: HTML formatted email body
    """
    
    # Start with email header
    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .customer { background-color: #f0f0f0; padding: 15px; margin: 15px 0; border-radius: 5px; }
            .customer-name { font-size: 18px; font-weight: bold; color: #333; margin-bottom: 10px; }
            .article { background-color: white; padding: 10px; margin: 10px 0; border-left: 3px solid #0066cc; }
            .article-title { font-weight: bold; color: #0066cc; text-decoration: none; }
            .article-title:hover { text-decoration: underline; }
            .article-meta { color: #666; font-size: 12px; margin-top: 5px; }
            .article-desc { color: #333; margin-top: 5px; font-size: 13px; }
            .source { display: inline-block; background-color: #e0e0e0; padding: 2px 6px; border-radius: 3px; font-size: 11px; }
            .no-articles { color: #999; font-style: italic; }
            .summary { font-size: 12px; color: #666; margin-top: 20px; }
        </style>
    </head>
    <body>
    """
    
    html += f"<h1>Daily Customer News Summary</h1>\n"
    html += f"<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>\n"
    html += "<hr>\n"
    
    # Count total articles
    total_articles = sum(len(articles) for articles in matches_by_customer.values())
    
    # Add articles for each customer
    for customer_name, matched_articles in matches_by_customer.items():
        html += f'<div class="customer">\n'
        html += f'<div class="customer-name">📊 {customer_name}</div>\n'
        
        if matched_articles:
            html += f'<p style="margin: 0; color: #666;">{len(matched_articles)} relevant articles found</p>\n'
            
            for match in matched_articles:
                article = match['article']
                score = match['match_score']
                
                html += f'<div class="article">\n'
                html += f'<a href="{article["link"]}" class="article-title" target="_blank">{article["title"]}</a>\n'
                html += f'<div class="article-meta">\n'
                html += f'<span class="source">{article["source"]}</span>\n'
                html += f'📅 {article["published"]}\n'
                html += f'(Match: {score*100:.0f}%)\n'
                html += f'</div>\n'
                
                # Add truncated description
                desc = article['description'].strip()
                if len(desc) > DESCRIPTION_LENGTH:
                    desc = desc[:DESCRIPTION_LENGTH] + '...'
                
                html += f'<div class="article-desc">{desc}</div>\n'
                html += f'</div>\n'
        else:
            html += f'<p class="no-articles">No relevant articles found today</p>\n'
        
        html += f'</div>\n'
    
    # Add footer
    html += "<hr>\n"
    html += f'<div class="summary">\n'
    html += f'<p>Total articles found: <strong>{total_articles}</strong></p>\n'
    html += f'<p>This is an automated report. Do not reply to this email.</p>\n'
    html += f'</div>\n'
    html += "</body></html>\n"
    
    return html


def send_email(matches_by_customer):
    """
    Send email summary using Outlook/SMTP
    
    Args:
        matches_by_customer (dict): Results from find_matching_articles()
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    try:
        logger.info("Preparing to send email...")
        
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = EMAIL_SUBJECT_TEMPLATE.format(
            date=datetime.now().strftime('%Y-%m-%d')
        )
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECIPIENT
        
        # Create email body
        html_body = create_email_body(matches_by_customer)
        
        # Attach HTML content
        part = MIMEText(html_body, 'html')
        msg.attach(part)
        
        # Connect to Outlook SMTP server
        logger.info(f"Connecting to {EMAIL_SERVER}:{EMAIL_PORT}...")
        server = smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT)
        server.starttls()  # Secure connection
        
        # Login with credentials
        logger.info("Logging in to Outlook...")
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        
        # Send email
        logger.info(f"Sending email to {EMAIL_RECIPIENT}...")
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
        server.quit()
        
        logger.info("✓ Email sent successfully!")
        return True
        
    except smtplib.SMTPAuthenticationError:
        logger.error("❌ Email authentication failed. Check your email and password.")
        logger.error("Note: For Outlook, you may need to use an 'App Password' instead of your regular password.")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"❌ SMTP error: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Error sending email: {e}")
        return False


if __name__ == '__main__':
    # Test: create a sample email preview
    sample_matches = {
        'Apple Inc.': [
            {
                'article': {
                    'title': 'Apple announces new iPhone features',
                    'link': 'https://example.com/article1',
                    'source': 'Reuters',
                    'published': '2024-01-15',
                    'description': 'Apple unveiled new features for the upcoming iPhone...'
                },
                'match_score': 0.95
            }
        ],
        'Tesla Inc.': []
    }
    
    html = create_email_body(sample_matches)
    
    # Save preview to file
    with open('email_preview.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✓ Email preview saved to email_preview.html")
    print("\nTo send real email, call send_email() with your matched articles.")
