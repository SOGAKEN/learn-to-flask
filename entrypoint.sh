#!/bin/sh

# BigQuery テーブルの作成
python migrations/create_llm_performance_table.py

# アプリケーションの起動
python run.py
