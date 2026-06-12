---
license: cc-by-4.0
language:
  - en
tags:
  - kv-cache
  - kv-cache-compression
  - llm-inference
  - inference-efficiency
  - efficient-inference
  - long-context
  - quantization
  - kv-cache-quantization
  - kv-cache-eviction
  - benchmark
  - leaderboard
  - evaluation-protocol
  - large-language-models
  - transformers
task_categories:
  - text-generation
pretty_name: "KV Cache Compression Benchmark — Matched-Budget Evaluation (MBE)"
size_categories:
  - n<1K
configs:
  - config_name: manifest
    data_files: mbe_manifest.json
  - config_name: results
    data_files: cards/*.json
---

# Matched-Budget Evaluation (MBE) — KV Cache Compression

A **standardized reporting protocol** for KV cache compression in LLM inference. MBE is
not a new task benchmark; it is a thin reporting layer that fixes *which* models, tasks,
and budgets results are reported at, so that numbers from different papers become
comparable.

- **Manifest** (`mbe_manifest.json`): the frozen evaluation specification — model suite,
  task suite (consuming existing benchmarks: LongBench, RULER, SCBench, GSM8K, IFEval),
  the fixed KV-budget ladder (50 / 25 / 12.5 / 6.25 %), and the required system metrics.
  Evaluate at these exact settings so results line up.
- **Results** (`cards/*.json`): submitted **KV Compression Cards** — one method × one
  model, produced by the open harness under matched budgets.

## Why
Published KV cache compression results are not comparable (different models, budgets,
tasks, system metrics). MBE fixes the axes. See the companion survey and harness:
- Harness / protocol: https://github.com/rohithreddybc/mbe-protocol
- Survey: "Breaking the Memory Wall: A Survey of Key-Value (KV) Cache Compression for
  Efficient Large Language Model (LLM) Inference" (Artificial Intelligence Review, under
  review).

## How to contribute a result
Run the harness (`run_mbe.py`) on the manifest's model + budget ladder, then submit your
card JSON via PR to the GitHub repo or as a dataset PR here.

## Citation
See `CITATION.cff` in the GitHub repository.

## License
CC-BY-4.0. The manifest references third-party benchmarks under their own licenses.
