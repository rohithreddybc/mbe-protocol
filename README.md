# MBE — Matched-Budget Evaluation for KV Cache Compression

**A standardized reporting protocol and open harness for evaluating KV cache compression methods at fixed memory budgets.**

MBE is **not a new benchmark.** It is a thin reporting layer that consumes existing
task suites (LongBench, RULER, SCBench, GSM8K, and a multi-turn/agentic trace) and
fixes the axes along which their results are compared, so that numbers from different
papers can finally be placed on a single picture.

> Companion to the survey *"Breaking the Memory Wall: A Survey of Key-Value (KV) Cache
> Compression for Efficient Large Language Model (LLM) Inference"* (Artificial
> Intelligence Review, under review), which **introduces the MBE protocol in Section 10**.

---

## Why MBE

Published KV cache compression results are not comparable: method A reports
"near-lossless at a 50% budget," method B reports "8× compression" at lower quality,
on a different model and task, with no system metrics. They cannot be ranked.

**MBE's one rule:** compare every method at the **same retained-KV-memory budgets**,
report the **same task grid** and the **same system metrics**, and package the result
as one **KV Compression Card**.

## The matched-budget ladder

Budget = fraction of the full-cache footprint retained (computed from
`M_KV = 2 · B · T · L · H_kv · D_head · P`). Report at:

| Budget | Retained KV |
|-------:|:------------|
| B50    | 50%         |
| B25    | 25%         |
| B12    | 12.5%       |
| B06    | 6.25% (optional, aggressive) |

## The reporting suite

| Axis   | Required dimension        | Specified values |
|--------|---------------------------|------------------|
| Model  | scale + attention type    | 7–8B GQA model · a 7–14B model · one ≥70B model |
| Task   | retrieval                 | long-doc QA (LongBench / SCBench tasks) |
| Task   | aggregation / tracing     | multi-hop + aggregation (RULER) |
| Task   | instruction following     | multi-instruction prompts |
| Task   | reasoning                 | chain-of-thought arithmetic (GSM8K) |
| Task   | agentic / multi-turn      | ≥1 long-horizon trace |
| System | memory + latency          | peak KV memory · decode throughput · TTFT · max batch before OOM · hardware tier |
| Method | deployment prerequisite   | training-free / calibration / pre-training; composability |

## Quickstart

```bash
pip install -r requirements.txt
# 1. describe your method + run config in a YAML (see configs/example_method.yaml)
python run_mbe.py --config configs/example_method.yaml --out cards/mymethod_llama3.1-8b.json
# 2. render the standardized card
python render_card.py cards/mymethod_llama3.1-8b.json > cards/mymethod_llama3.1-8b.md
# 3. submit cards/ via pull request to appear on the LEADERBOARD
```

The harness is **adapter-based**: implement one `KVCompressor` interface
(`methods/base.py`) and MBE handles the budget sweep, task running, and metric
collection. Reference adapters for KIVI, H2O, SnapKV, StreamingLLM, and PyramidKV
ship in `methods/`.

## Contributing a result

Open a PR adding `cards/<method>_<model>.json`. CI re-renders the card and updates
[`LEADERBOARD.md`](LEADERBOARD.md). Every merged card is a reproducible, citable,
third-party data point.

## Dataset
Evaluation manifest + result cards: https://huggingface.co/datasets/Rohithreddybc/mbe-kv-cache
Live leaderboard (Space): https://huggingface.co/spaces/Rohithreddybc/mbe-leaderboard

## Cite

If you evaluate under MBE, please cite the survey (see [`CITATION.cff`](CITATION.cff)).

## License

Code: Apache-2.0. Protocol specification and cards: CC-BY-4.0.
