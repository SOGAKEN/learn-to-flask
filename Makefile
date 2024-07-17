# 変数定義
PROJECT_ID := docker-cloudran-works
REGION := asia-northeast1
REPOSITORY := llm
IMAGE_NAME := llm-comparison-app
VERSION := $(shell git rev-parse --short HEAD)
FULL_IMAGE_NAME := $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(REPOSITORY)/$(IMAGE_NAME):$(VERSION)

# デフォルトのターゲット
.PHONY: all
all: build push

# 依存関係のインストール
.PHONY: install
install:
	pip install -r requirements.txt

# テストの実行
.PHONY: test
test:
	python -m pytest tests/

# Docker イメージのビルド
.PHONY: build
build:
	docker build --platform linux/amd64 -t $(FULL_IMAGE_NAME) .

# Artifact Registry への Docker イメージのプッシュ
.PHONY: push
push:
	docker push $(FULL_IMAGE_NAME)

# Cloud Run へのデプロイ
.PHONY: deploy
deploy:
	gcloud run deploy $(IMAGE_NAME) \
		--image $(FULL_IMAGE_NAME) \
		--platform managed \
		--region $(REGION) \
		--allow-unauthenticated

# ローカルでの実行
.PHONY: run
run:
	python run.py

# クリーンアップ
.PHONY: clean
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

# BigQuery テーブルの作成
.PHONY: create-table
create-table:
	python migrations/create_llm_performance_table.py

# Artifact Registry リポジトリの作成
.PHONY: create-repo
create-repo:
	gcloud artifacts repositories create $(REPOSITORY) \
		--repository-format=docker \
		--location=$(REGION) \
		--description="Repository for LLM Comparison App"

# gcloud の認証設定
.PHONY: gcloud-auth
gcloud-auth:
	gcloud auth configure-docker $(REGION)-docker.pkg.dev

# ヘルプ
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  install        Install dependencies"
	@echo "  test           Run tests"
	@echo "  build          Build Docker image"
	@echo "  push           Push Docker image to Artifact Registry"
	@echo "  deploy         Deploy to Cloud Run"
	@echo "  run            Run locally"
	@echo "  clean          Clean up generated files"
	@echo "  create-table   Create BigQuery table"
	@echo "  create-repo    Create Artifact Registry repository"
	@echo "  gcloud-auth    Configure gcloud authentication"
