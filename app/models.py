from google.cloud import bigquery

schema = [
    bigquery.SchemaField("request_time", "TIMESTAMP"),
    bigquery.SchemaField("provider", "STRING"),
    bigquery.SchemaField("model_id", "STRING"),
    bigquery.SchemaField("response_time", "FLOAT"),
    bigquery.SchemaField("request", "STRING"),
    bigquery.SchemaField("response", "STRING"),
]


def create_table(client, table_id):
    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)
    print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")
