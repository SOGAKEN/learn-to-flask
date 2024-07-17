import asyncio
import logging
import sys
import traceback

from flask import Blueprint, jsonify, request

from app import PROMPTS
from app.services import aws_service, azure_service, gcp_service

bp = Blueprint("main", __name__)

logging.basicConfig(level=logging.INFO)


@bp.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200


@bp.route("/app", methods=["GET", "POST"])
def run_llm_comparison():
    if request.method == "GET":
        return jsonify({"message": "Please use POST method to run LLM comparison"}), 200

    try:
        input_prompt = request.json.get("prompt", "Hello, LLM!")
        logging.info(f"Received prompt: {input_prompt}")
        logging.info(f"PROMPTS content: {PROMPTS}")
        results = asyncio.run(run_comparison(input_prompt))
        return jsonify(
            {"message": "Comparison completed successfully", "results": results}
        )
    except Exception as e:
        logging.error(f"Error in LLM comparison: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


async def run_comparison(input_prompt):
    try:
        tasks = []
        for provider_model, config in PROMPTS.items():
            provider = provider_model.split(".")[0]  # 'aws.claude-v2' から 'aws' を取得
            service = getattr(sys.modules[__name__], f"{provider}_service")
            tasks.append(service.run_query(provider, config["model_id"], input_prompt))

        results = await asyncio.gather(*tasks)
        logging.info(f"Completed {len(results)} queries")
        return results
    except Exception as e:
        logging.error(f"Error in run_comparison: {str(e)}")
        logging.error(traceback.format_exc())
        raise


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


@bp.errorhandler(405)
def method_not_allowed_error(error):
    return (
        jsonify(
            {
                "error": "Method Not Allowed",
                "message": "The method is not allowed for the requested URL.",
            }
        ),
        405,
    )


@bp.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error", "message": str(error)}), 500
