import asyncio
import warnings
import httpx
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import time
from db.db_connection import connect_to_db, close_db_connection
import os
from bs4 import MarkupResemblesLocatorWarning

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

# Define the directory for scraping logs
scrapping_log_dir = os.path.join('logs', 'Investing_scrapping_logs')
os.makedirs(scrapping_log_dir, exist_ok=True)  # Ensure the directory exists

# Generate a timestamp-based filename for scraping logs
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
scrapping_log_file = os.path.join(scrapping_log_dir, f"{timestamp}.log")

# Configure logging for scraping logs
logging.basicConfig(
    filename=scrapping_log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

data = []
 
# Function to clean text
def clean_text(text):
    if isinstance(text, str):
        text = text.replace('\n', ' ').replace('\r', '')
        text = ' '.join(text.split())
        return text
    else:
        return ''

# Async function to fetch the page using httpx
async def fetch_page(url, headers):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.encoding = 'utf-8'
        return response.text

# Async function to scrape article details
async def scrape_article_details(title_text, title_link, header, data):
    try:
        # Fetch the full article page asynchronously
        article_html_content = await fetch_page(title_link, header)
        article_soup = BeautifulSoup(article_html_content, 'html.parser')

        # Extract author, publish date, and full text
        author_name = article_soup.select_one('span.flex.flex-row.text-xs').get_text(strip=True) if article_soup.select_one('span.flex.flex-row.text-xs') else "Investing.com"
        published_text = article_soup.select_one('div.flex.flex-row.items-center > span').get_text(strip=True)
        if "Published" in published_text:
            published_text = published_text.replace("Published", "").strip()
            publish_date, publish_time = published_text.split(", ")
        else:
            publish_date, publish_time = None, None

        # Full article text
        paragraph = article_soup.select('div#article p')
        para_lines = [p.text for p in paragraph]
        full_text = ' '.join(para_lines)
        cleaned_full_text = clean_text(full_text)

        data.append({
            'Title': title_text,
            'Title_Link': title_link,
            'Author': author_name,
            'Publish_Date': publish_date,
            'Publish_Time': publish_time,
            'Full_Text': cleaned_full_text
        })

    except Exception as e:
        logging.error(f"Error processing article {title_text}: {e}")

# Async function to scrape the news data from the website
async def scrape_news():
    start_time = time.time()
    try:
        for page in range(1,3):
            url = f"https://www.investing.com/news/stock-market-news/{page}"
            header = {
                'user-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            }
            html_content = await fetch_page(url, header)
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find all the news items
            news_content_divs = soup.select('div.news-analysis-v2_content__z0iLP')

            # Create tasks for each article to scrape asynchronously
            tasks = []
            for div in news_content_divs:
                anchor = div.select_one('a')
                title_text = anchor.get_text(strip=True) if anchor else None
                title_link = anchor.get('href') if anchor else None
                if title_text and title_link:
                    tasks.append(scrape_article_details(title_text, title_link, header, data))

            # Run the tasks concurrently
            await asyncio.gather(*tasks)

        elapsed_time = time.time() - start_time
        logging.info(f"Scraping completed in {elapsed_time:.2f} seconds")
        return data

    except Exception as e:
        logging.error(f"Error occurred while scraping: {e}")
        return []

# Insert the scraped data into the PostgreSQL database
def insert_data_to_db(data):
    connection, cursor = connect_to_db()
    if not connection:
        logging.error("Failed to connect to the database.")
        return
    start_time = time.time()  # Start timing the data insertion process

    inserted_count = 0  # Track inserted records
    skipped_count = 0  # Track skipped records due to conflict
    
    try:
        for record in data:
            cursor.execute("""
                INSERT INTO public.investing_news(title, title_link, author, publish_date, publish_time, full_text, scrapedata_inserted_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (title_link) DO NOTHING;
            """, (
                record['Title'],
                record['Title_Link'],
                record['Author'],
                record['Publish_Date'],
                record['Publish_Time'],
                record['Full_Text'],
                datetime.now()
            ))

            # Check how many rows were actually inserted
            if cursor.rowcount > 0:  # Means data was inserted
                inserted_count += 1
            else:
                skipped_count += 1  # Means data was skipped due to conflict

        connection.commit()
        elapsed_time = time.time() - start_time  # Calculate time taken for insertion
        logging.info(f"Data insertion completed. {inserted_count} new records inserted, {skipped_count} records skipped due to conflict. Total time: {elapsed_time:.2f} seconds.")
    except Exception as e:
        logging.error(f"Failed to insert data: {e}")
        connection.rollback()
    finally:
        close_db_connection(connection, cursor)

# Main function to run scraping and database insertion
async def investing_main():
    scraped_data = await scrape_news()
    if scraped_data:
        logging.info(f"Scraped {len(scraped_data)} articles.")
        # Insert the scraped data into the database after scraping is complete
        insert_data_to_db(scraped_data)

# Run the main function
if __name__ == "__main__":
    asyncio.run(investing_main())
