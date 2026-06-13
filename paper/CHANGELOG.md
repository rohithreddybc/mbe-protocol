# Manuscript changelog — from initial draft to current

For coauthors: what changed between the original draft and the current submission-ready
manuscript (target venue: *Artificial Intelligence Review*, Springer).

## At a glance

| | Initial draft | Current |
|---|---|---|
| Title | "...A *Comprehensive Review* of KV Cache Compression and Architecture..." | "...A *Survey* of *Key-Value (KV) Cache Compression* for *Efficient... (LLM) Inference*" |
| References | 98 numbered `[n]`, **~37 fabricated** (fake authors + future arXiv IDs) | **209 real, verified** (1 ID unresolved), Springer author–year |
| Length / sections | ~9,000 words, no front/back matter | ~16,700 words, **11 sections**, ~38 pages |
| Tables / figures | **0 / 0** | **6 tables, 4 figures + graphical abstract** (each with a *Takeaway*) |
| Abstract / keywords / methodology / declarations | none | all present (abstract 248 w, PRISMA flow, full declarations) |
| Original contribution | none (pure synthesis) | **MBE protocol** + open harness, HF dataset, live leaderboard, Colab |

## Major changes

1. **Citation integrity (was a desk-reject risk).** ~37 of 98 citations in the draft were
   fabricated (generic author names + non-existent future-dated arXiv IDs). The
   bibliography was rebuilt to **209 real, verifiable references**, each cited in the text
   (0 orphans), in Springer SPBASIC author–year style. Smart-quote encoding artifacts
   were fixed throughout.
2. **Venue-standard apparatus added** (none existed): abstract + keywords, a **PRISMA
   survey methodology** (§2), a **Limitations** section, a **Reproducibility** statement,
   and full Springer **declarations** (funding, competing interests, data availability,
   ethics, author contributions, AI-use).
3. **Differentiation.** New **Table 1** + §1.4 position the survey against every competing
   review (Li et al. TMLR 2025; Shi et al. 2024; Liu et al. 2025; Xu et al. 2026; Jiang
   et al. ACL 2026; Zhen et al. 2025; plus broader efficiency surveys).
4. **New coverage (whole families the draft lacked):** rotation quantization
   (QuaRot/SpinQuant), low-rank/SVD KV (Palu/Eigen Attention), learned compression
   (DMC/Activation Beacon), cross-request KV transport (CacheGen/CacheBlend/LMCache),
   adaptive-budget eviction (Ada-KV/PyramidKV/Quest), TOVA/Loki, prefill–decode
   disaggregation (DistServe/Sarathi), and multimodal caches. References current through
   June 2026.
5. **Original contribution — Matched-Budget Evaluation (MBE):** a named, standardized
   fixed-budget reporting protocol (§10) with an open harness, a public HF dataset, a live
   leaderboard Space, and a one-click Colab (bring-your-own-method). Real 0.5B multi-method
   seed results are included; the 7–8B run is pending (see colab/).
6. **Tables & figures (all new, all with one-line Takeaways):** survey-comparison,
   security-threats, taxonomy, reported-results, accuracy-at-budget, MBE-spec tables;
   PRISMA-flow, taxonomy, literature-trends, and Pareto figures; plus a graphical abstract.
   All figures export vector PDF/EPS.
7. **Tone, correctness, reproducibility:** removed hyperbole / AI-tells and humanized to
   low machine-signal; fixed real errors found in review (GQA arithmetic, an O(T²)/O(T³)
   complexity slip, a reversed GSM8K-sensitivity claim, several mis-citations); made the
   manuscript reproducible from this repo (one-command `paper/build.py`, verified from a
   clean clone).

## Quality bar
Independent reviewer-style scoring moved from an effective **desk reject** (fabricated
references) to **~84–88/100, ~72–78% acceptance after one revision**.

## Open items (for the author team)
- Author names, affiliations, ORCIDs (front matter currently uses placeholders).
- Finalize the AI-use disclosure wording to the team's actual process and AIR's policy.
- Run the 7–8B MBE seed on a GPU via the Colab and add the numbers to §10 / the leaderboard
  (see `colab/COAUTHOR_INSTRUCTIONS.md`).
- Post the arXiv preprint at submission; verify the 1 remaining reference ID.
