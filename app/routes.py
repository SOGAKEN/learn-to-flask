import asyncio
import logging
from flask import Flask, jsonify

from app import create_app
from app.services import aws_service, azure_service, gcp_service

app = create_app()
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET", "POST"])
async def run_llm_comparison():
    input_prompt = "Hello, LLM!"

    results = await run_comparison(input_prompt)

    return jsonify({"message": "Comparison completed successfully", "results": results})


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
