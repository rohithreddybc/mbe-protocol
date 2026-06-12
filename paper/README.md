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

## Reproduce
```bash
pip install python-docx matplotlib
python build_manuscript.py   # writes the .docx; convert to PDF with Word/LibreOffice
```

## Status / remaining work
See `REVISION_NOTES.md` and `submission/SUBMISSION_CHECKLIST.md`. The main open item is
running the MBE seed leaderboard (parent repo) and adding the controlled numbers.
