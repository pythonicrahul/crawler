FROM python:3.12

WORKDIR /app

COPY producer.py .
COPY urls.txt .

RUN pip install redis pymongo

CMD ["python", "producer.py"]
