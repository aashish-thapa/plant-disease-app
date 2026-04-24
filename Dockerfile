FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgomp1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p database uploads

EXPOSE 8080

CMD gunicorn --bind 0.0.0.0:$PORT --timeout 120 run:app
