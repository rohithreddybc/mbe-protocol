# Publishing MBE to the Hugging Face Hub

Two artifacts are worth publishing on the Hub. Do this *after* you have at least the
seed leaderboard so the dataset is non-empty.

## 1. Dataset: `rohithreddybc/kv-cache-compression-mbe`
The evaluation manifest + result cards (this folder).

```bash
pip install -U huggingface_hub
huggingface-cli login                 # paste an HF write token
huggingface-cli upload rohithreddybc/kv-cache-compression-mbe . . --repo-type=dataset
```
The `README.md` here is the dataset card (YAML frontmatter already set: CC-BY-4.0,
tags, configs). After upload, the dataset is citable and its downloads/likes are
third-party-adoption evidence.

## 2. (Optional) Space: `rohithreddybc/kv-cache-compression-leaderboard`
A small Gradio/Streamlit app that renders `cards/*.json` as a sortable leaderboard. A
live leaderboard is the strongest adoption driver.

## What NOT to upload
- Do **not** re-upload LongBench / RULER / SCBench / GSM8K / IFEval — they already exist
  on the Hub under their own licenses. MBE *references* them in the manifest.
- Do **not** upload model weights or raw training data — MBE is an evaluation protocol.

## Link back
Put the dataset URL in the paper's Data Availability statement and in the GitHub README
so the paper, repo, and dataset cross-reference each other.
