from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
import json
import time
from datetime import datetime
import os

azure_client = TextAnalyticsClient(
    endpoint=os.getenv("AZURE_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("AZURE_KEY")),
)
azure_model_ids = os.getenv("AZURE_MODEL_ID", "").split(",")


def get_azure_models():
    return azure_model_ids


async def query_azure(model_id, input_text):
    try:
        response = azure_client.analyze_sentiment(documents=[input_text])
        return {
            "sentiment": response[0].sentiment,
            "confidence_scores": response[0].confidence_scores.to_dict(),
        }
    except AzureError as e:
        print(f"Error querying Azure model {model_id}: {e}")
        return {"error": str(e)}


async def run_query(provider, model_id, input_text):
    start_time = time.time()
    request_time = datetime.utcnow()

    response = await query_azure(model_id, input_text)

    end_time = time.time()

    return {
        "request_time": request_time,
        "provider": provider,
        "model_id": model_id,
        "response_time": end_time - start_time,
        "request": input_text,
        "response": json.dumps(response),
    }
