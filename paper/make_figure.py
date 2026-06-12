# -*- coding: utf-8 -*-
"""Generate a clean four-layer taxonomy overview figure for the survey."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(8.2, 5.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

# Central problem box
ax.add_patch(FancyBboxPatch((3.4, 8.5), 3.2, 0.9, boxstyle="round,pad=0.06",
                            fc="#1f2a44", ec="#1f2a44"))
ax.text(5.0, 8.95, "KV Cache Memory Wall\n(memory-bandwidth-bound decoding)",
        ha="center", va="center", color="white", fontsize=9.5, fontweight="bold")

layers = [
    ("Algorithmic\ncompression (§4)",
     "Quantization  ·  Eviction / sparsity  ·  Token & cross-layer merging",
     "#2563eb"),
    ("Architectural\nredesign (§5)",
     "MQA / GQA  ·  Multi-head latent attention  ·  SSM & hybrid models",
     "#0e9f6e"),
    ("System-level\nmanagement (§6)",
     "Paged attention  ·  Prefix sharing (+ security)  ·  Tiered offloading",
     "#b45309"),
    ("Hardware\nacceleration (§7)",
     "Decode kernels & fusion  ·  Processing-in-memory  ·  ASIC / FPGA",
     "#9333ea"),
]

y = 6.7
for i, (title, items, color) in enumerate(layers):
    yy = y - i * 1.55
    # connector
    ax.plot([5.0, 1.9], [8.45, yy + 0.45], color="#b8c0cc", lw=1.0, zorder=0)
    ax.add_patch(FancyBboxPatch((0.4, yy), 3.0, 0.9, boxstyle="round,pad=0.05",
                                fc=color, ec=color))
    ax.text(1.9, yy + 0.45, title, ha="center", va="center", color="white",
            fontsize=9, fontweight="bold")
    ax.add_patch(FancyBboxPatch((3.7, yy), 6.0, 0.9, boxstyle="round,pad=0.05",
                                fc="#f1f4f9", ec=color, lw=1.3))
    ax.text(6.7, yy + 0.45, items, ha="center", va="center", color="#1f2a44",
            fontsize=8.4)

# cross-cutting concern bar
ax.add_patch(FancyBboxPatch((0.4, 0.25), 9.3, 0.7, boxstyle="round,pad=0.05",
                            fc="#fde8e8", ec="#c81e1e", lw=1.3))
ax.text(5.05, 0.6,
        "Cross-cutting (§8–§9): co-design & Pareto trade-offs  ·  "
        "infinite context  ·  agentic degradation  ·  benchmarking  ·  multi-tenant security",
        ha="center", va="center", color="#7a1010", fontsize=8.0)

plt.tight_layout()
fig.savefig("taxonomy_figure.png", dpi=220, bbox_inches="tight")
print("Saved taxonomy_figure.png")
