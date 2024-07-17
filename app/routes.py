import asyncio
import logging

from flask import jsonify
from google.cloud import bigquery

from app import create_app
from app.services import aws_service, azure_service, gcp_service

app = create_app()
logging.basicConfig(level=logging.INFO)

bigquery_client = bigquery.Client()


@app.route("/", methods=["GET", "POST"])
def run_llm_comparison():
    input_prompt = "Hello, LLM!"

    results = asyncio.run(run_comparison(input_prompt))

    # BigQueryにデータを挿入
    table_id = f"{app.config['GCP_PROJECT_ID']}.{app.config['BIGQUERY_DATASET_ID']}.llm_performance"
    errors = bigquery_client.insert_rows_json(table_id, results)
    if errors:
        logging.error(f"Errors inserting rows: {errors}")

    return jsonify(
        {
            "message": "Comparison completed and data inserted successfully",
            "results": results,
        }
    )


async def run_comparison(input_prompt):
    aws_models = await aws_service.get_aws_models()
    gcp_models = await gcp_service.get_gcp_models()
    azure_models = azure_service.get_azure_models()

    tasks = []
    for provider, models, service in [
        ("AWS", aws_models, aws_service),
        ("GCP", gcp_models, gcp_service),
        ("Azure", azure_models, azure_service),
    ]:
        for model_id in models:
            tasks.append(service.run_query(provider, model_id, input_prompt))

    results = await asyncio.gather(*tasks)
    logging.info(f"Completed {len(results)} queries")
    return results
