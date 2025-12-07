# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# requirements.txt を先にコピーしてインストール
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体をコピー
COPY app ./app

# 起動コマンド
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
