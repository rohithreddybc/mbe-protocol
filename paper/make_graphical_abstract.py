# -*- coding: utf-8 -*-
"""Graphical abstract: problem -> four-layer mitigation -> MBE protocol -> comparable results.

Text labels are auto-fitted to their boxes so they can never overflow (which made
white-on-dark labels spill onto the page and look truncated)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(9.2, 4.4))
ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")


def _fit(t, max_w, max_h=None, min_fs=4.5):
    inv = ax.transData.inverted()
    for _ in range(60):
        fig.canvas.draw()
        bb = t.get_window_extent()
        (x0, y0) = inv.transform((bb.x0, bb.y0))
        (x1, y1) = inv.transform((bb.x1, bb.y1))
        w, h = abs(x1 - x0), abs(y1 - y0)
        fs = t.get_fontsize()
        if (w <= max_w and (max_h is None or h <= max_h)) or fs <= min_fs:
            return
        t.set_fontsize(fs - 0.3)


def box(x, y, w, h, text, fc, ec, fs=9, bold=False, tc="white"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                                fc=fc, ec=ec, lw=1.4, zorder=2))
    t = ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
                color=tc, fontweight="bold" if bold else "normal", zorder=3)
    _fit(t, w * 0.88, h * 0.86)


def arrow(x0, x1, y):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="-|>", color="#1f2a44", lw=2.0))


# Problem
box(0.2, 2.3, 2.3, 1.5, "The Memory Wall\nKV cache dominates\nlong-context LLM\ninference",
    "#1f2a44", "#1f2a44", fs=9.2, bold=True)
arrow(2.55, 3.15, 3.0)

# Four layers
layers = [
    ("Algorithmic\n(quant · evict ·\nmerge · low-rank)", "#2563eb"),
    ("Architectural\n(GQA · MLA ·\nSSM / hybrid)", "#0e9f6e"),
    ("System\n(paging · transport ·\noffload)", "#b45309"),
    ("Hardware\n(kernels · PIM ·\nASIC / FPGA)", "#9333ea"),
]
for i, (txt, col) in enumerate(layers):
    box(3.2, 4.55 - i * 1.18, 3.1, 1.02, txt, col, col, fs=7.8)
arrow(6.45, 7.0, 3.05)

# MBE protocol
box(7.05, 1.95, 2.4, 2.2,
    "MBE\nMatched-Budget\nEvaluation\n(fixed-budget protocol\n+ open harness)",
    "#7a1010", "#7a1010", fs=8.6, bold=True)
arrow(9.5, 10.0, 3.05)

# Outcome
box(10.05, 2.3, 1.85, 1.5,
    "Comparable,\nreproducible\nresults\n+ leaderboard",
    "#0e7a3b", "#0e7a3b", fs=8.2, bold=True)

# unique-contribution ribbon (kept clear of the stacked layer boxes above)
ax.add_patch(FancyBboxPatch((3.2, 0.05), 6.25, 0.72, boxstyle="round,pad=0.05",
                            fc="#fff4e5", ec="#b45309", lw=1.2, zorder=2))
rt = ax.text(6.32, 0.41,
             "First survey to jointly cover multi-tenant security + agentic degradation "
             "and to ship a standardised evaluation protocol",
             ha="center", va="center", fontsize=8.0, color="#7a1010", style="italic", zorder=3)
_fit(rt, 6.25 * 0.92, 0.72 * 0.86)

fig.savefig("graphical_abstract.png", dpi=240, bbox_inches="tight")
fig.savefig("graphical_abstract.pdf", bbox_inches="tight")  # vector for production
fig.savefig("graphical_abstract.eps", bbox_inches="tight")
print("Saved graphical_abstract.png")
