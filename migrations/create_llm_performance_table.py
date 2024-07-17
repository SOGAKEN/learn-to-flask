import os

from google.cloud import bigquery

schema = [
    bigquery.SchemaField("request_time", "TIMESTAMP"),
    bigquery.SchemaField("provider", "STRING"),
    bigquery.SchemaField("model_id", "STRING"),
    bigquery.SchemaField("response_time", "FLOAT"),
    bigquery.SchemaField("request", "STRING"),
    bigquery.SchemaField("response", "STRING"),
]


def create_llm_performance_table():
    client = bigquery.Client()
    project_id = os.getenv("GCP_PROJECT_ID")
    dataset_id = os.getenv("BIGQUERY_DATASET_ID")
    table_id = "llm_performance"

    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    table = bigquery.Table(table_ref, schema=schema)

    try:
        table = client.create_table(table, exists_ok=True)
        print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")
    except Exception as e:
        print(f"Error creating BigQuery table: {e}")


if __name__ == "__main__":
    create_llm_performance_table()
