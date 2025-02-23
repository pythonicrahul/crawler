import redis
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

REDIS_QUEUE_NAME = "url_queue"

def push_urls_to_redis():
    """Push URLs into Redis List using RPUSH."""
    # Connect to Redis
    redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

    # Read URLs from the file
    with open("urls.txt", "r") as file:
        urls = [line.strip() for line in file.readlines()]

    # Push URLs into Redis list
    for url in urls:
        redis_client.rpush(REDIS_QUEUE_NAME, url)  # Use RPUSH to add at the end of the list
        logging.info(f"Pushed: {url}")
        time.sleep(0.1)  # Throttle to avoid overwhelming Redis

if __name__ == "__main__":
    push_urls_to_redis()
