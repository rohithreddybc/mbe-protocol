# Running the MBE seed on Colab — instructions for coauthors

**Goal:** produce the real 7–8B "KV Compression Cards" that go into Section 10 / the
leaderboard of our survey. Right now the paper only has a 0.5B CPU proof-of-concept; this
gives us the model-scale numbers. It takes ~20–40 minutes on a **free** Colab GPU.

You need: a Google account. (Optional: a Hugging Face account — only if you use a gated
model like Llama, or want to upload the result yourself.)

---

## Step 1 — Open the notebook
Click the badge in the repo README, or open this link:

**https://colab.research.google.com/github/rohithreddybc/kv-cache-compression-mbe/blob/main/colab/MBE_seed_run.ipynb**

## Step 2 — Turn on the GPU (important)
In Colab: **Runtime → Change runtime type → Hardware accelerator → T4 GPU → Save.**
(The free T4 has 16 GB, enough — the 7–8B model is loaded in 4-bit.)

## Step 3 — Run the baseline cells
We want the built-in baselines (KIVI quantization, StreamingLLM, H2O), so use **Option B**.

1. Run **cell 1** ("Install + check GPU"). It installs packages and clones the repo
   (~2 min). You should see a line like `NVIDIA T4 ... 15360 MiB`. If it says no GPU,
   go back to Step 2.
2. **Skip the "Option A" cell** (that's for evaluating a brand-new method).
3. Run the **"Option B — baselines"** cell. Default model is `Qwen/Qwen2.5-7B-Instruct`
   (open, no access needed). This is the one to run for our numbers. It prints, per
   method and budget, a line like:
   ```
   kivi-4bit    budget=25.0%  -> passkey acc 0.950
   streaming    budget=25.0%  -> passkey acc 0.000
   ...
   ```
4. Run the **"Show your card"** cell. It prints the result JSON and saves it to
   `mbe-protocol/cards/seed_multimethod_qwen2.5-7b-instruct.json`.

## Step 4 — Send the result back
Two options, either is fine:

- **Easiest:** in Colab's left sidebar open the **Files** panel → `mbe-protocol/cards/`
  → right-click the new `seed_*.json` → **Download**, and email/Slack it to the
  corresponding author (Rohith). He'll commit it to the repo and the leaderboard.
- **Or upload it yourself** (last cell): it asks you to log in with a Hugging Face
  **write** token (https://huggingface.co/settings/tokens). It uploads to *your own*
  HF dataset namespace; then open an issue/PR on the GitHub repo with the link so it's
  added to the central leaderboard.

That's it. **Cells 1 → Option B → Show card → send the JSON.**

---

## Optional: run a second model
To strengthen the table, re-run the **Option B** cell after changing the model line to
another from the dropdown (e.g. `meta-llama/Llama-3.1-8B-Instruct`) and run "Show card"
again. **Llama is gated:** you must first request access on its HF model page and run
`from huggingface_hub import login; login()` with your token in a cell. Qwen needs none.

## Troubleshooting
- **Out-of-memory (CUDA OOM):** set `MBE_SKIP_H2O = '1'` in the Option B cell (H2O needs
  the most memory), or switch the model to `Qwen/Qwen2.5-3B-Instruct`.
- **"No GPU" / very slow:** you didn't enable the T4 (Step 2), or Colab gave you a CPU
  runtime — reconnect and retry.
- **Disconnects after idle:** Colab free tier times out if idle; keep the tab active, or
  just rerun — it's deterministic (fixed seed).
- **Want more samples (more stable numbers):** raise `MBE_N` (e.g. `'40'`); it's slower.

## What the numbers mean
Each method is evaluated at the **same KV-memory budget** (50/25/12.5%) on a passkey
retrieval task. Quantization keeps every token (usually near-lossless); eviction methods
drop tokens (and on this single-needle task can miss the needle). The point of MBE is
exactly this apples-to-apples, fixed-budget comparison — see Section 10 of the paper.

## Links
- Notebook: colab/MBE_seed_run.ipynb (in this repo)
- Repo: https://github.com/rohithreddybc/kv-cache-compression-mbe
- Dataset: https://huggingface.co/datasets/Rohithreddybc/kv-cache-compression-mbe
- Leaderboard: https://huggingface.co/spaces/Rohithreddybc/kv-cache-compression-leaderboard
