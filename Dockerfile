FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 8080 ポートを明示的に公開
EXPOSE 8080

CMD ["python", "run.py"]
