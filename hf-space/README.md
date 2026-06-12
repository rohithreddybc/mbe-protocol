---
title: MBE Leaderboard
emoji: 📊
colorFrom: indigo
colorTo: red
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
python_version: "3.12"
pinned: false
license: cc-by-4.0
---

# MBE Leaderboard

A live leaderboard for **Matched-Budget Evaluation (MBE)** of KV cache compression
methods. It renders the KV Compression Cards from the dataset
[`Rohithreddybc/mbe-kv-cache`](https://huggingface.co/datasets/Rohithreddybc/mbe-kv-cache),
updating as new cards are submitted.

## Deploy
1. Create a Space at huggingface.co/new-space (SDK: **Gradio**), named e.g.
   `Rohithreddybc/mbe-leaderboard`.
2. Push this folder (`app.py`, `README.md`, `requirements.txt`):
   ```bash
   huggingface-cli upload Rohithreddybc/mbe-leaderboard . . --repo-type=space
   ```
3. The Space builds automatically and pulls cards live from the dataset.

## Links
- Protocol + harness: https://github.com/rohithreddybc/mbe-protocol
- Dataset: https://huggingface.co/datasets/Rohithreddybc/mbe-kv-cache
