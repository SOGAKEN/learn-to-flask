#!/bin/sh

# BigQuery テーブルの作成 (必要な場合)
python migrations/create_llm_performance_table.py

# Flask アプリケーションの起動
python run.py
