import logging
import os

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError

logging.basicConfig(level=logging.INFO)

azure_key = os.getenv("AZURE_KEY")
azure_endpoint = os.getenv("AZURE_ENDPOINT")

if not azure_key:
    logging.error("AZURE_KEY environment variable is not set")
    azure_client = None
elif not azure_endpoint:
    logging.error("AZURE_ENDPOINT environment variable is not set")
    azure_client = None
else:
    try:
        azure_client = TextAnalyticsClient(
            endpoint=azure_endpoint, credential=AzureKeyCredential(azure_key)
        )
        logging.info("Azure client initialized successfully")
    except Exception as e:
        logging.error(f"Error initializing Azure client: {e}")
        azure_client = None

azure_model_ids = os.getenv("AZURE_MODEL_ID", "").split(",")


def get_azure_models():
    return azure_model_ids


async def query_azure(model_id, input_text):
    if not azure_client:
        logging.error("Azure client is not initialized")
        return {"error": "Azure client is not initialized"}

    try:
        response = azure_client.analyze_sentiment(documents=[input_text])
        return {
            "sentiment": response[0].sentiment,
            "confidence_scores": response[0].confidence_scores.to_dict(),
        }
    except AzureError as e:
        logging.error(f"Error querying Azure model {model_id}: {e}")
        return {"error": str(e)}


async def run_query(provider, model_id, input_text):
    # 既存のコード
    ...
