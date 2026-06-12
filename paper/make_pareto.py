# -*- coding: utf-8 -*-
"""Memory-accuracy frontier plotted from author-reported literature points (Table 5).
Heterogeneous settings -> indicative, not a controlled comparison; the controlled
version is produced by the MBE harness (Section 10)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# (KV budget retained %, reported accuracy retention %, label, colour, (dx,dy) label offset)
pts = [
    (50, 99.5, "8-bit/FP8", "#2563eb", (4, 6)),
    (25, 99.2, "DMC", "#14b8a6", (4, 7)),
    (25, 98.0, "4-bit", "#2563eb", (4, -13)),
    (20, 97.8, "H2O", "#0e9f6e", (-26, -13)),
    (12.5, 99.0, "Act. Beacon", "#14b8a6", (-62, 4)),
    (12, 100.2, "PyramidKV", "#0e9f6e", (-2, 6)),
    (10, 99.7, "R-KV", "#14b8a6", (-30, -13)),
    (3.2, 99.0, "CAKE", "#0e9f6e", (-6, 7)),
    (1.7, 85.0, "DynamicKV", "#0e9f6e", (5, 5)),
    (0.25, 97.0, "RocketKV", "#0e9f6e", (6, 7)),
]

fig, ax = plt.subplots(figsize=(6.4, 4.3))
# crude upper-envelope frontier through the better points
env = sorted([(b, a) for (b, a, _, _, _) in pts])
fx = [b for b, _ in env]
fy = []
best = 0
for b, a in env:
    best = max(best, a)
    fy.append(best)
ax.plot(fx, fy, color="#1f2a44", lw=1.4, ls="--", alpha=0.6, label="reported envelope")

for (b, a, lab, col, off) in pts:
    ax.scatter([b], [a], s=55, color=col, edgecolor="white", zorder=5)
    ax.annotate(lab, (b, a), textcoords="offset points", xytext=off, fontsize=7.3,
                color="#1f2a44")

ax.set_xscale("log")
ax.set_xlabel("KV cache budget retained (%, log scale)", fontsize=9)
ax.set_ylabel("Reported accuracy retention (%)", fontsize=9)
ax.set_xlim(0.15, 70)
ax.set_ylim(80, 101)
ax.set_xticks([0.25, 1, 3, 10, 25, 50])
ax.set_xticklabels(["0.25", "1", "3", "10", "25", "50"])
ax.tick_params(labelsize=8)
ax.grid(True, ls=":", alpha=0.5)
ax.legend(fontsize=8, loc="lower right")
# colour legend
from matplotlib.lines import Line2D
fam = [Line2D([0],[0],marker='o',color='w',markerfacecolor=c,markersize=7,label=l)
       for c,l in [("#2563eb","Quantization"),("#0e9f6e","Eviction"),("#14b8a6","Learned")]]
ax.legend(handles=fam + [Line2D([0],[0],ls="--",color="#1f2a44",alpha=0.6,label="envelope")],
          fontsize=7.5, loc="lower left")
plt.tight_layout()
fig.savefig("pareto_figure.png", dpi=220, bbox_inches="tight")
print("Saved pareto_figure.png (data-derived from Table 5 literature points)")
