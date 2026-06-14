# -*- coding: utf-8 -*-
"""PRISMA-style identification/screening/inclusion flow figure for the survey.
Counts are approximate (the field moves fast; preprints and archival versions overlap)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(6.8, 5.8))
ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.axis("off")

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


def box(x, y, w, h, text, fc="#eef2f8", ec="#1f2a44", fs=8.3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                                fc=fc, ec=ec, lw=1.3, zorder=2))
    t = ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs,
                color="#1f2a44", zorder=3)
    _fit(t, w * 0.90, h * 0.84)

def down(x, y0, y1, color="#1f2a44"):
    ax.annotate("", xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.3))

stages = [
    (10.3, "Records identified via search\n(Consensus / Semantic Scholar / arXiv / Scopus\n+ citation tracing), cut-off June 2026:  n ≈ 612", "#eef2f8", "#1f2a44"),
    (8.4,  "Records after de-duplication and\ntitle screening:  n ≈ 318", "#eef2f8", "#1f2a44"),
    (6.5,  "Full-text assessed for eligibility\nand venue quality:  n ≈ 206", "#eef2f8", "#1f2a44"),
    (4.6,  "Studies included and discussed\nin this survey:  n = 177", "#e6f4ea", "#0e7a3b"),
]
for (y, txt, fc, ec) in stages:
    box(1.7, y, 5.6, 1.15, txt, fc=fc, ec=ec)
for i in range(len(stages) - 1):
    down(4.5, stages[i][0], stages[i+1][0] + 1.15)

# exclusion notes on the right
exclusions = [
    (9.35, "Excluded ≈ 294:\nduplicates, off-topic"),
    (7.45, "Excluded ≈ 112:\ntraining-only,\nno KV-cache focus"),
    (5.55, "Excluded ≈ 29:\nweak venue / superseded"),
]
for (y, txt) in exclusions:
    box(7.7, y, 2.1, 0.95, txt, fc="#fdecec", ec="#b42318", fs=7.0)
    ax.annotate("", xy=(7.65, y + 0.48), xytext=(7.32, y + 0.48),
                arrowprops=dict(arrowstyle="-|>", color="#b42318", lw=1.0))

for y, lab in [(10.9, "Identification"), (7.5, "Screening"), (4.6, "Included")]:
    ax.text(0.45, y, lab, ha="left", va="center", fontsize=8.5, rotation=90,
            color="#5a6473", fontweight="bold")

plt.tight_layout()
fig.savefig("prisma_figure.png", dpi=220, bbox_inches="tight")
fig.savefig("prisma_figure.pdf", bbox_inches="tight")  # vector for production
fig.savefig("prisma_figure.eps", bbox_inches="tight")
print("Saved prisma_figure.png")
