FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED True

# デバッグ用：ディレクトリ構造を表示
RUN ls -R

CMD ["python", "run.py"]
