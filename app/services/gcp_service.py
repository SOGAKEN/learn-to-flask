import json
import logging
import os
import time
from datetime import datetime

from google.cloud import aiplatform

gcp_client = aiplatform.gapic.PredictionServiceClient(
    client_options={
        "api_endpoint": f"{os.getenv('GCP_REGION', 'asia-northeast1')}-aiplatform.googleapis.com"
    }
)
gcp_project_id = os.getenv("GCP_PROJECT_ID")


async def get_gcp_models():
    try:
        parent = f"projects/{gcp_project_id}/locations/{os.getenv('GCP_REGION', 'asia-northeast1')}"
        models = aiplatform.Model.list(parent=parent)
        return [model.display_name for model in models]
    except Exception as e:
        logging.error(f"Error fetching GCP models: {e}")
        return []


async def query_gcp(model_id, input_text):
    try:
        endpoint = gcp_client.endpoint_path(
            project=gcp_project_id,
            location=os.getenv("GCP_REGION", "asia-northeast1"),
            endpoint=model_id,
        )
        instance = aiplatform.gapic.PredictRequest(
            endpoint=endpoint,
            instances=[{"content": input_text}],
            parameters={"temperature": 0.2, "maxOutputTokens": 256},
        )
        response = gcp_client.predict(request=instance)
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
