import logging
import os

from google.auth import default
from google.cloud import bigquery

logging.basicConfig(level=logging.INFO)

schema = [
    bigquery.SchemaField("request_time", "TIMESTAMP"),
    bigquery.SchemaField("provider", "STRING"),
    bigquery.SchemaField("model_id", "STRING"),
    bigquery.SchemaField("response_time", "FLOAT"),
    bigquery.SchemaField("request", "STRING"),
    bigquery.SchemaField("response", "STRING"),
]


def create_llm_performance_table():
    # デフォルトの認証情報を使用してプロジェクトIDを取得
    _, project_id = default()

    # 環境変数からプロジェクトIDを取得し、デフォルト値がない場合は自動取得したIDを使用
    project_id = os.getenv("GCP_PROJECT_ID", project_id)
    dataset_id = os.getenv("BIGQUERY_DATASET_ID")
    table_id = "llm_performance"

    if not project_id:
        raise ValueError("Unable to determine GCP_PROJECT_ID")
    if not dataset_id:
        raise ValueError("BIGQUERY_DATASET_ID must be set")

    # データセットIDからプロジェクトIDを削除（もし含まれていれば）
    dataset_id = dataset_id.split(".")[-1]

    logging.info(f"Project ID: {project_id}")
    logging.info(f"Dataset ID: {dataset_id}")
    logging.info(f"Table ID: {table_id}")

    client = bigquery.Client(project=project_id)

    # テーブル参照を正しく構築
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    logging.info(f"Full table reference: {table_ref}")

    table = bigquery.Table(table_ref, schema=schema)

    try:
        table = client.create_table(table, exists_ok=True)
        logging.info(
            f"Created table {table.project}.{table.dataset_id}.{table.table_id}"
        )
    except Exception as e:
        logging.error(f"Error creating BigQuery table: {e}")
        raise


if __name__ == "__main__":
    create_llm_performance_table()
