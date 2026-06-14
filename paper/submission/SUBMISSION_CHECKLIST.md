# Submission checklist — Artificial Intelligence Review (Springer, journal 10462)

## Review model
AI Review is **single-blind**: authors are named on the title page; reviewers are
anonymous. No manuscript anonymisation is required, so the repository URL and author
name may remain in the PDF. (If the handling editor requests double-blind, swap the
title block for "Author(s) withheld" and replace the repo URL with an
anonymous.4open.science mirror.)

## Done (in the manuscript build)
- [x] Title with primary search keywords ("KV cache", "LLM inference", "survey").
- [x] Abstract **248 words** (within the 150–250 limit), no undefined abbreviations.
- [x] Keywords (7) provided.
- [x] Springer **SPBASIC author–year** citations; alphabetical reference list; 208 refs.
- [x] Numbered sections 1–11; Review Methodology (§2) with PRISMA-style flow (Fig. 1).
- [x] Limitations / threats-to-validity subsection (§10.5).
- [x] Declarations: funding, competing interests, data availability (with repo URL),
      ethics approval, author contributions, generative-AI-use statement.
- [x] 6 tables, 3 figures, all cross-referenced and in order.

## To complete before/at submission (author actions)
- [ ] Fill title page: full name, department, institution, city, country, **ORCID**.
- [ ] Add **CRediT** roles (single author: Conceptualization, Investigation, Writing –
      original draft, Writing – review & editing, Visualization).
- [ ] Cover letter (see COVER_LETTER.md) and Highlights (HIGHLIGHTS.md).
- [ ] Optional but recommended: graphical abstract (graphical_abstract.png).
- [ ] **Verify every reference's arXiv ID / DOI / full author list** in a reference
      manager (Zotero/Mendeley + Springer SPBASIC style). Some preprint IDs were left
      as "arXiv preprint" pending verification — attach exact IDs.
- [ ] Supply figures as **vector EPS/PDF or 300+ dpi TIFF** (regenerate from the
      make_*.py scripts; current PNGs are 220–240 dpi — bump dpi or export EPS).
- [ ] Post the **arXiv preprint** (cs.CL, cross-list cs.LG) the same week.
- [ ] Run the **MBE seed leaderboard** and add the controlled numbers (see notes).
- [ ] Suggest reviewers (SUGGESTED_REVIEWERS.md); declare conflicts.
- [ ] Confirm: not under consideration elsewhere; ICMJE/COPE compliance.

## Figure export note
The manuscript currently embeds PNGs. For production, re-export each figure as EPS:
`fig.savefig("name.eps")` in each make_*.py, or increase dpi to 600 for TIFF.
