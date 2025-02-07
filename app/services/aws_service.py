import json
import logging
import os
import time
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

aws_client = boto3.client(
    "bedrock",
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


async def get_aws_models():
    try:
        response = aws_client.list_foundation_models()
        return [model["modelId"] for model in response.get("modelSummaries", [])]
    except ClientError as e:
        logging.error(f"Error fetching AWS models: {e}")
        return []


async def query_aws(model_id, input_text):
    try:
        runtime_client = boto3.client(
            "bedrock-runtime",
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

        response = runtime_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({"prompt": input_text}),
        )
        return json.loads(response["body"].read())
    except ClientError as e:
        logging.error(f"Error querying AWS model {model_id}: {e}")
        return {"error": str(e)}


async def run_query(provider, model_id, input_text):
    start_time = time.time()
    request_time = datetime.utcnow()

    response = await query_aws(model_id, input_text)

    end_time = time.time()

    return {
        "request_time": request_time.isoformat(),
        "provider": provider,
        "model_id": model_id,
        "response_time": end_time - start_time,
        "request": input_text,
        "response": json.dumps(response),
    }
