#!/bin/sh
set -e

echo "Starting entrypoint script..."

echo "GCP_PROJECT_ID: $GCP_PROJECT_ID"
echo "BIGQUERY_DATASET_ID: $BIGQUERY_DATASET_ID"

# BigQuery テーブルの作成
python migrations/create_llm_performance_table.py
echo "BigQuery table creation completed."

# アプリケーションの起動
python run.py
