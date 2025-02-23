FROM python:3.12

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    fonts-liberation \
    libappindicator3-1 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxrandr2 \
    xdg-utils

# Install Google Chrome (stable version)
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# Install ChromeDriver using WebDriver Manager
RUN pip install redis pymongo requests beautifulsoup4 selenium webdriver-manager

# Copy worker code
COPY worker.py .

CMD ["python", "worker.py"]
