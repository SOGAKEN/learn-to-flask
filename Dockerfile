FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED True
ENV FLASK_APP run.py

# デバッグ用：ディレクトリ構造を表示
RUN ls -R

# Flask アプリケーションを初期化してから実行
CMD ["python", "-c", "from app import create_app; app = create_app(); app.run(host='0.0.0.0', port=8080)"]
