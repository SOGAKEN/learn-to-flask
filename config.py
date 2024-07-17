import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")
    GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
    GCP_REGION = os.environ.get("GCP_REGION", "asia-northeast1")
    AZURE_ENDPOINT = os.environ.get("AZURE_ENDPOINT")
    AZURE_KEY = os.environ.get("AZURE_KEY")
    AZURE_MODEL_ID = os.environ.get("AZURE_MODEL_ID")
    BIGQUERY_DATASET_ID = os.environ.get("BIGQUERY_DATASET_ID")
