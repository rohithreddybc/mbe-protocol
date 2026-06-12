# -*- coding: utf-8 -*-
"""Data-bearing figure: surveyed references by year and (approximate) family,
computed directly from references.py. Substantiates currency and breadth of coverage."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import re
from collections import defaultdict
from references import REFERENCES

# priority-ordered family classifier (first match wins) over the reference string
FAMILIES = [
    ("Security/agentic", ["leak", "side channel", "side-channel", "attack", "privacy",
                           "isolation", "agent", "memory mechanism"]),
    ("Hardware", ["processing-in-memory", "pim", "compute-in-memory", "flashattention",
                  "flashdecoding", "flash-decoding", "reram", "fpga", "asic", "accelerat",
                  "roofline", "memory wall"]),
    ("System/serving", ["paged", "serving", "offload", "flexgen", "sglang", "disaggreg",
                        "cachegen", "lmcache", "cacheblend", "memserve", "prefix",
                        "vllm", "scheduling", "transport", "mooncake", "infinigen"]),
    ("Architecture", ["latent attention", "grouped-query", "multi-query", "mamba",
                      "rwkv", "retentive", "state space", "state-space", "jamba",
                      "yoco", "infini-attention", "mla", "low-rank"]),
    ("Eviction/sparsity", ["evict", "heavy", "snapkv", "scissor", "sparsit", "sparse",
                           "pyramid", "keyformer", "razor", "quest", "token pruning",
                           "selection", "budget"]),
    ("Quantization", ["quant", "bit", "kivi", "awq", "gptq", "rotat", "spinquant",
                      "quarot", "precision"]),
    ("Merging/learned", ["merg", "token merging", "distill", "beacon", "dynamic memory",
                          "learn", "compress"]),
]
COLORS = {
    "Quantization": "#2563eb", "Eviction/sparsity": "#0e9f6e",
    "Merging/learned": "#14b8a6", "Architecture": "#9333ea",
    "System/serving": "#b45309", "Hardware": "#7a1010",
    "Security/agentic": "#be185d", "Other": "#94a3b8",
}

def classify(s):
    s = s.lower()
    for name, kws in FAMILIES:
        if any(k in s for k in kws):
            return name
    return "Other"

by_year = defaultdict(lambda: defaultdict(int))
for _, full in REFERENCES.values():
    m = re.search(r"\((\d{4})", full)
    if not m:
        continue
    y = int(m.group(1))
    if y < 2022:
        y = 2021  # bucket foundational
    by_year[y][classify(full)] += 1

years = sorted(by_year)
fams = ["Quantization", "Eviction/sparsity", "Merging/learned", "Architecture",
        "System/serving", "Hardware", "Security/agentic", "Other"]

fig, ax = plt.subplots(figsize=(7.6, 4.2))
bottom = [0] * len(years)
for fam in fams:
    vals = [by_year[y].get(fam, 0) for y in years]
    ax.bar([str(y) if y != 2021 else "≤2021" for y in years], vals, bottom=bottom,
           label=fam, color=COLORS[fam], edgecolor="white", linewidth=0.4)
    bottom = [b + v for b, v in zip(bottom, vals)]

ax.set_ylabel("Number of surveyed references", fontsize=9)
ax.set_xlabel("Publication year", fontsize=9)
ax.tick_params(labelsize=8)
ax.legend(fontsize=7.2, ncol=2, loc="upper left", frameon=False)
ax.set_title("Surveyed references by year and family (approximate assignment)",
             fontsize=9.5)
ax.grid(axis="y", ls=":", alpha=0.5)
plt.tight_layout()
fig.savefig("trends_figure.png", dpi=220, bbox_inches="tight")
print("Saved trends_figure.png; total classified:", sum(sum(v.values()) for v in by_year.values()))
