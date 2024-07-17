from google.cloud import bigquery
from app.models import schema
import os


def create_llm_performance_table(client, project_id, dataset_id, table_id):
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)
    print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")


if __name__ == "__main__":
    client = bigquery.Client()
    project_id = os.getenv("GCP_PROJECT_ID")
    dataset_id = os.getenv("BIGQUERY_DATASET_ID")
    table_id = "llm_performance"
    create_llm_performance_table(client, project_id, dataset_id, table_id)
