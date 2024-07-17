import asyncio
import logging

from flask import Blueprint, jsonify, request

from app.services import aws_service, azure_service, gcp_service

bp = Blueprint("main", __name__)

logging.basicConfig(level=logging.INFO)


@bp.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200


@bp.route("/app", methods=["POST"])
def run_llm_comparison():
    input_prompt = request.json.get("prompt", "Hello, LLM!")
    results = asyncio.run(run_comparison(input_prompt))
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


@bp.errorhandler(404)
def not_found_error(error):
    return (
        jsonify(
            {
                "error": "Not Found",
                "message": "The requested URL was not found on the server.",
            }
        ),
        404,
    )


@bp.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error", "message": str(error)}), 500
