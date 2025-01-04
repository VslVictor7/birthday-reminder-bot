FROM python:3.12.8-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk update && \
    pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/cache/apk/*

COPY . .

CMD ["python", "bot/main.py"]