# Pre-empted reviewer concerns and prepared responses

Use this as an internal cheat-sheet for the rebuttal/revision letter. Each entry is a
likely criticism, where the manuscript already addresses it, and the response if pressed.

### 1. "Another KV-cache survey — how is this different from Li et al. 2025 / Xu et al. 2026 / Jiang et al. 2026?"
- **In paper:** Section 1.4 + Table 1 name all competitors and tabulate coverage.
- **Response:** Four differentiators no competitor has together — hardware-first
  co-design framing, multi-tenant security, agentic degradation, and a *standardised
  evaluation protocol (MBE)*. The right-most Table 1 column shows only our survey
  ships a protocol; none covers security and agentic jointly.

### 2. "MBE is a proposal, not a result — the paper ships no controlled numbers."
- **In paper:** §10.4 and §10.5 (Limitations) state this honestly; Table 5 collates
  literature numbers; the harness is open.
- **Response (revision):** include the seed leaderboard (KIVI, H2O, SnapKV,
  StreamingLLM, PyramidKV on a 7–8B model) produced by the released harness as a new
  table. This is the single highest-value revision and is already scoped in the repo.

### 3. "Synthesis is shallow — citation strings rather than comparison."
- **In paper:** Tables 3–5, the eviction-signal analysis (§4.2), and the co-design
  compatibility discussion (§8.2) provide comparison beyond enumeration.
- **Response:** point to the per-family evaluative sentences and offer to add a
  compatibility matrix (already discussed in §8.2) as a table if desired.

### 4. "Search not systematic / counts vague."
- **In paper:** §2 + PRISMA-style Fig. 1 with identification→screening→inclusion
  counts and explicit inclusion criteria (a)–(d) and a June 2026 cut-off.
- **Response:** counts are reproducible; we can attach the screening log as
  supplementary material.

### 5. "Reference count below a comprehensive survey norm."
- **Response:** 208 references, current through June 2026 (21 from 2026), covering
  quantization, eviction, merging, low-rank, learned, architectural, system,
  transport, hardware, security, agentic, and evaluation. We can extend specific
  families on request.

### 6. "Quantitative tables are not directly comparable."
- **In paper:** the captions of Tables 4 and 5 say so explicitly, and §9.3/§10 argue
  this is precisely the problem MBE solves.
- **Response:** this is the motivation for the contribution, not a flaw in it.

### 7. "Figures are schematic."
- **Response:** Fig. 1 is a PRISMA flow (data-bearing); Fig. 2 is the taxonomy; Fig. 3
  is explicitly labelled illustrative. On revision, Fig. 3 will be replaced by a
  measured Pareto plot from the MBE seed run.
