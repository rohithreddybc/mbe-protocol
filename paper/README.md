# Paper: Breaking the Memory Wall (KV cache survey)

This folder holds the survey manuscript that introduces the **MBE protocol** in the
parent repository.

**Title:** Breaking the Memory Wall: A Survey of Key-Value (KV) Cache Compression for
Efficient Large Language Model (LLM) Inference
**Target venue:** Artificial Intelligence Review (Springer) — under preparation/review.
**Author:** Rohith Reddy B. C.

## Contents
- `KV Cache Compression_paper_revised.docx` / `.pdf` — the manuscript (~15k words, 11
  sections, 209 references, 6 tables, 4 figures).
- `build_manuscript.py`, `references.py` — regenerate the manuscript: `python build_manuscript.py`.
- `make_*.py` — figure generators (taxonomy, PRISMA flow, literature trends, Pareto,
  graphical abstract).
- `figures/` — rendered figures (PNG; export EPS/TIFF for production).
- `submission/` — cover letter, highlights, submission checklist, suggested reviewers,
  response-to-anticipated-reviewers.
- `REVISION_NOTES.md` — full revision history, acceptance scoring, and remaining tasks.

## Reproduce (one command, cross-platform, deterministic)
```bash
pip install -r requirements.txt
python build.py     # regenerates all figures -> .docx -> PDF (if Word/LibreOffice present)
```
`build.py` runs the figure generators (`make_*.py`) **then** `build_manuscript.py` in the
correct order. Running `build_manuscript.py` alone produces a figure-less draft, since it
embeds the PNGs the figure scripts create. PDF export uses `docx2pdf` (needs Word) or
LibreOffice headless; without either, open the `.docx` and "Save as PDF".

The figure data is itself reproducible: `make_trends.py` computes Fig. 3 directly from
`references.py`, and `make_pareto.py` plots the author-reported points of Table 5. The
reference list (`references.py`) is the single source of truth for all citations.

## Reproduce the empirical results
The MBE seed numbers come from `../eval/run_seed.py` (deterministic: `torch.manual_seed(0)`).
The 0.5B CPU run reproduces on any machine with `torch` + `transformers`; the 7-8B run is a
one-click Colab (see the repository root README). Results can vary slightly with the
`transformers` version due to attention/tokenizer changes; pin versions for exact numbers.

## Status / remaining work
See `REVISION_NOTES.md` and `submission/SUBMISSION_CHECKLIST.md`. The main open item is
running the MBE seed leaderboard (parent repo) and adding the controlled numbers.
