# MBE Leaderboard

Auto-generated from `cards/*.json`. Each row is a reproducible KV Compression Card.
**Compare within a (model, budget) group only.**

---

## Seed run (CPU, multi-method) — REAL numbers

> Produced by `eval/run_seed.py` on **Qwen2.5-0.5B-Instruct (GQA), CPU/float32**,
> passkey retrieval (single mid-context needle), N=8. A **proof-of-concept across
> compression families** at matched budgets — **not** the paper's 7-8B suite. The
> eviction adapters keep a subset of the prefill cache with correct RoPE positions;
> decode passes true position ids. These are deliberately simple reference
> implementations.

| Method (family)              | 100% | 25% | 12.5% |
|------------------------------|:----:|:---:|:-----:|
| full (baseline)              | 1.00 |  -  |   -   |
| KIVI-4bit (quantization)     |  -   | 1.00| 1.00  |
| StreamingLLM (sink+window)   |  -   | 0.00| 0.00  |
| H2O (heavy-hitter, simplified)|  -  | 0.00| 0.00  |

**Finding:** at these budgets, **quantization (which retains every token) is lossless**,
while **budget-constrained eviction drops the mid-context needle** and fails retrieval.
This reproduces, at small scale, the known weakness of accumulated-attention eviction on
needle-style retrieval that motivates query-aware methods (survey §4.2). It also confirms
the eviction + position handling is correct: a clean "needle evicted" failure, not garbage.

> Earlier single-family quantization sweep (`eval/smoke_quant.py`) additionally shows the
> 2-bit cliff: KV-8bit and KV-4bit are lossless, KV-2bit collapses (card in `cards/`).

---

## Full suite (seed) — in progress

> Status: **placeholder.** Populate by running `run_mbe.py` for the methods below on a
> 7-8B model across the 50/25/12.5% budget ladder (a single-GPU job). Cells marked `—`
> are not yet measured; **do not cite `—` cells.** Author-reported literature numbers
> live in the survey's Table 5, not here.

### Llama-3.1-8B-Instruct — LongBench (avg, ↑)

| Method        | Type           | Full | B50 | B25 | B12 | Training-free |
|---------------|----------------|:----:|:---:|:---:|:---:|:-------------:|
| Full cache    | baseline       |  —   |  —  |  —  |  —  |  —            |
| KIVI          | quantization   |  —   |  —  |  —  |  —  |  ✓            |
| H2O           | eviction       |  —   |  —  |  —  |  —  |  ✓            |
| SnapKV        | eviction       |  —   |  —  |  —  |  —  |  ✓            |
| StreamingLLM  | rolling buffer |  —   |  —  |  —  |  —  |  ✓            |
| PyramidKV     | layer-adaptive |  —   |  —  |  —  |  —  |  ✓            |

## Submit
`run_mbe.py` → `cards/<method>_<model>.json` → PR. CI re-renders this file.
