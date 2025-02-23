import redis
import time
import requests
import random
import logging
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Redis and MongoDB Config
REDIS_STREAM_NAME = "url_stream"
MONGO_DB_NAME = "crawler_db"
MONGO_COLLECTION_NAME = "metadata"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/117.0.0.0 Safari/537.36"
]

def fetch_with_requests(url):
    """Fetch page using requests."""
    try:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        response = requests.get(url, timeout=20, headers=headers)
        return response.content if response.status_code == 200 else None
    except Exception as e:
        logging.error(f"Requests error: {e}")
        return None

def fetch_with_selenium(url):
    """Fetch page using Selenium for CAPTCHA/JS-heavy sites."""
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(random.uniform(5, 10))  # Allow JS to load
        page_source = driver.page_source
        driver.quit()
        return page_source
    except Exception as e:
        logging.error(f"Selenium error: {e}")
        return None

def extract_metadata(url):
    """Extract metadata from the webpage."""
    try:
        html_content = fetch_with_selenium(url) if "amazon" in url.lower() else fetch_with_requests(url)
        if not html_content:
            return None

        soup = BeautifulSoup(html_content, "html.parser")
        title = soup.title.string if soup.title else "N/A"
        description = soup.find("meta", {"name": "description"})
        description = description["content"] if description else "N/A"
        body = soup.get_text(separator=" ", strip=True)[:1000]

        return {"url": url, "title": title, "description": description, "body": body}
    except Exception as e:
        logging.error(f"Extraction error: {e}")
        return None

def worker():
    logging.info("Connecting to Redis and MongoDB...")

    try:
        redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)
        redis_client.ping()
        logging.info("Redis connection successful!")
    except Exception as e:
        logging.error(f"Redis connection error: {e}")

    mongo_client = MongoClient("mongodb://mongodb:27017/")
    collection = mongo_client[MONGO_DB_NAME][MONGO_COLLECTION_NAME]

    logging.info("Worker started, waiting for URLs...")

    while True:
        try:
            messages = redis_client.xread({REDIS_STREAM_NAME: "0"}, count=1, block=1000)
            if not messages:
                continue
            for stream_name, msg_list in messages:
                for message_id, data in msg_list: 
                    url = data.get("url")
                    if url:
                        logging.info(f"Processing: {url}")
                        metadata = extract_metadata(url)
                        if metadata:
                            collection.insert_one(metadata)
                            logging.info(f"Saved to MongoDB: {url}")

                        redis_client.xdel(REDIS_STREAM_NAME, message_id)
        except Exception as e:
            logging.error(f"Worker error: {e}")
        time.sleep(1)

if __name__ == "__main__":
    logging.info("Starting worker...")
    try:
        worker()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.error(f"Worker error: {e}")
    finally:
        logging.info("Shutting down worker...")

