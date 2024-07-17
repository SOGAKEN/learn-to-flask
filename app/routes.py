import asyncio
import logging
import sys
import traceback

from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request

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
        prompts = app.config["PROMPTS"]
        logging.info(f"Received prompt: {input_prompt}")
        logging.info(f"PROMPTS content: {prompts}")
        results = asyncio.run(run_comparison(input_prompt, prompts))
        return jsonify(
            {"message": "Comparison completed successfully", "results": results}
        )
    except Exception as e:
        logging.error(f"Error in LLM comparison: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


async def run_comparison(input_prompt, prompts):
    try:
        tasks = []
        for provider_model, config in prompts.items():
            provider = provider_model.split(".")[0]
            service = getattr(sys.modules[__name__], f"{provider}_service")
            model_id = config.get("model_id")
            if not model_id:
                raise ValueError(f"No model_id found for {provider_model}")
            tasks.append(service.run_query(provider, model_id, input_prompt))

        results = await asyncio.gather(*tasks)
        logging.info(f"Completed {len(results)} queries")
        return results
    except Exception as e:
        logging.error(f"Error in run_comparison: {str(e)}")
        logging.error(traceback.format_exc())
        raise
