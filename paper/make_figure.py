# -*- coding: utf-8 -*-
"""Generate a clean four-layer taxonomy overview figure for the survey.

Every text label is auto-fitted to its box: the font is shrunk until the text
provably fits inside the box (width and height), so labels can never overflow the
box boundary (which previously made white-on-dark text spill onto the white page
and look clipped)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(8.8, 5.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")


def _fit(t, max_w, max_h=None, min_fs=5.0):
    """Shrink text object `t` until it fits within max_w (and max_h) data units."""
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
        t.set_fontsize(fs - 0.4)


def labelbox(cx, cy, w, h, text, fc, ec, fs, tc, bold=False, lw=1.3):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0.05", fc=fc, ec=ec, lw=lw, zorder=2))
    t = ax.text(cx, cy, text, ha="center", va="center", color=tc, fontsize=fs,
                fontweight="bold" if bold else "normal", zorder=3)
    _fit(t, w * 0.90, h * 0.82)


# Central problem box (wide enough for the full subtitle line)
labelbox(5.0, 8.95, 5.2, 0.95, "KV Cache Memory Wall\n(memory-bandwidth-bound decoding)",
         "#1f2a44", "#1f2a44", 9.5, "white", bold=True)

layers = [
    ("Algorithmic\ncompression (§4)",
     "Quantization  ·  Eviction / sparsity  ·  Token & cross-layer merging", "#2563eb"),
    ("Architectural\nredesign (§5)",
     "MQA / GQA  ·  Multi-head latent attention  ·  SSM & hybrid models", "#0e9f6e"),
    ("System-level\nmanagement (§6)",
     "Paged attention  ·  Prefix sharing (+ security)  ·  Tiered offloading", "#b45309"),
    ("Hardware\nacceleration (§7)",
     "Decode kernels & fusion  ·  Processing-in-memory  ·  ASIC / FPGA", "#9333ea"),
]

y = 6.7
for i, (title, items, color) in enumerate(layers):
    cy = (y - i * 1.55) + 0.45
    ax.plot([5.0, 1.9], [8.45, cy], color="#b8c0cc", lw=1.0, zorder=0)
    labelbox(1.9, cy, 3.0, 0.9, title, color, color, 9, "white", bold=True)
    labelbox(6.7, cy, 6.0, 0.9, items, "#f1f4f9", color, 8.4, "#1f2a44", lw=1.3)

# cross-cutting concern bar
labelbox(5.05, 0.6, 9.3, 0.72,
         "Cross-cutting (§8–§9): co-design & Pareto trade-offs  ·  infinite context  ·  "
         "agentic degradation  ·  benchmarking  ·  multi-tenant security",
         "#fde8e8", "#c81e1e", 8.0, "#7a1010", lw=1.3)

fig.savefig("taxonomy_figure.png", dpi=220, bbox_inches="tight")
fig.savefig("taxonomy_figure.pdf", bbox_inches="tight")  # vector for production
fig.savefig("taxonomy_figure.eps", bbox_inches="tight")
print("Saved taxonomy_figure.png")
