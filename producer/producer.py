import redis
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

REDIS_STREAM_NAME = "url_stream"

def push_urls_to_redis():
    # Connect to Redis
    redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

    # Read URLs from the file
    with open("urls.txt", "r") as file:
        urls = [line.strip() for line in file.readlines()]

    # Push URLs into Redis Stream
    for url in urls:
        redis_client.xadd(REDIS_STREAM_NAME, {"url": url})
        logging.info(f"Pushed: {url}")
        time.sleep(0.1)  # Throttle to avoid overwhelming Redis

if __name__ == "__main__":
    push_urls_to_redis()
