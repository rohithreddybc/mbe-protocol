---
title: "KV Cache Compression Leaderboard (MBE)"
emoji: 📊
colorFrom: indigo
colorTo: red
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
python_version: "3.12"
pinned: false
license: cc-by-4.0
tags:
  - kv-cache
  - kv-cache-compression
  - llm-inference
  - inference-efficiency
  - long-context
  - quantization
  - benchmark
  - leaderboard
---

# MBE Leaderboard

A live leaderboard for **Matched-Budget Evaluation (MBE)** of KV cache compression
methods. It renders the KV Compression Cards from the dataset
[`Rohithreddybc/kv-cache-compression-mbe`](https://huggingface.co/datasets/Rohithreddybc/kv-cache-compression-mbe),
updating as new cards are submitted.

## Deploy
1. Create a Space at huggingface.co/new-space (SDK: **Gradio**), named e.g.
   `Rohithreddybc/kv-cache-compression-leaderboard`.
2. Push this folder (`app.py`, `README.md`, `requirements.txt`):
   ```bash
   huggingface-cli upload Rohithreddybc/kv-cache-compression-leaderboard . . --repo-type=space
   ```
3. The Space builds automatically and pulls cards live from the dataset.

## Links
- Protocol + harness: https://github.com/rohithreddybc/mbe-protocol
- Dataset: https://huggingface.co/datasets/Rohithreddybc/kv-cache-compression-mbe
