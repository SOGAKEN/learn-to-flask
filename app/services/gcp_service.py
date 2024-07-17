import json
import logging
import os
import time
from datetime import datetime

from google.cloud import aiplatform

from app import PROMPTS

gcp_client = aiplatform.gapic.PredictionServiceClient(
    client_options={
        "api_endpoint": f"{os.getenv('GCP_REGION', 'us-central1')}-aiplatform.googleapis.com"
    }
)
gcp_project_id = os.getenv("GCP_PROJECT_ID")


async def get_gcp_models():
    try:
        parent = f"projects/{gcp_project_id}/locations/{os.getenv('GCP_REGION', 'us-central1')}"
        models = aiplatform.Model.list(parent=parent)
        return [model.display_name for model in models]
    except Exception as e:
        logging.error(f"Error fetching GCP models: {e}")
        return []


async def query_gcp(model_id, input_text):
    try:
        model_config = next(
            (
                config
                for provider_model, config in PROMPTS.items()
                if config["model_id"] == model_id and provider_model.startswith("gcp.")
            ),
            None,
        )
        if not model_config:
            raise ValueError(f"Model configuration not found for {model_id}")

        endpoint = gcp_client.endpoint_path(
            project=gcp_project_id,
            location=os.getenv("GCP_REGION", "us-central1"),
            endpoint=model_id,
        )
        instance = {
            "prompt": model_config["prompt_template"].format(input_text=input_text),
            "max_output_tokens": model_config.get("max_output_tokens", 256),
            "temperature": model_config.get("temperature", 0.2),
        }
        response = gcp_client.predict(endpoint=endpoint, instances=[instance])
        return {"predictions": [pred.to_dict() for pred in response.predictions]}
    except Exception as e:
        logging.error(f"Error querying GCP model {model_id}: {e}")
        return {"error": str(e)}


async def run_query(provider, model_id, input_text):
    start_time = time.time()
    request_time = datetime.utcnow()

    response = await query_gcp(model_id, input_text)

    end_time = time.time()

    return {
        "request_time": request_time.isoformat(),
        "provider": provider,
        "model_id": model_id,
        "response_time": end_time - start_time,
        "request": input_text,
        "response": json.dumps(response),
    }
