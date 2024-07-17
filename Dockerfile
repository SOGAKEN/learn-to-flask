FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONUNBUFFERED=1
# entrypoint.shに実行権限を付与
RUN chmod +x entrypoint.sh

EXPOSE 8080

# ENTRYPOINTを使用してentrypoint.shを実行
ENTRYPOINT ["./entrypoint.sh"]
