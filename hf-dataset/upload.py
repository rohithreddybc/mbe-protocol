#!/usr/bin/env python3
"""
One-shot uploader for the MBE dataset to the Hugging Face Hub.

Prereq (run once, in YOUR terminal so the token is cached locally, never pasted
into a chat):
    pip install -U huggingface_hub
    huggingface-cli login        # paste a WRITE token from https://huggingface.co/settings/tokens

Then:
    python upload.py             # creates rohithreddybc/kv-cache-compression-mbe and uploads this folder
"""
import os
from huggingface_hub import HfApi, create_repo

REPO_ID = os.environ.get("MBE_HF_REPO", "rohithreddybc/kv-cache-compression-mbe")
HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    api = HfApi()
    who = api.whoami()                       # fails loudly if not logged in
    print("Authenticated as:", who.get("name"))
    create_repo(REPO_ID, repo_type="dataset", exist_ok=True)
    print("Repo ready:", REPO_ID)
    api.upload_folder(
        folder_path=HERE,
        repo_id=REPO_ID,
        repo_type="dataset",
        ignore_patterns=["upload.py", "UPLOAD.md", "__pycache__/*"],
        commit_message="Add MBE evaluation manifest + dataset card",
    )
    print(f"Done -> https://huggingface.co/datasets/{REPO_ID}")

if __name__ == "__main__":
    main()
