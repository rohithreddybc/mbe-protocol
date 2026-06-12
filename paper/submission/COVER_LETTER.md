# Cover Letter — Artificial Intelligence Review

[Date]

To the Editors-in-Chief,
*Artificial Intelligence Review* (Springer)

Dear Editors,

I am pleased to submit our manuscript, **"Breaking the Memory Wall: A Survey of
Key-Value (KV) Cache Compression for Efficient Large Language Model (LLM)
Inference,"** for consideration as a review article in *Artificial Intelligence
Review*.

The key-value cache has become the dominant memory and cost bottleneck of
large-language-model inference: it grows linearly with context length and batch
size and must be streamed in full for every generated token, turning decoding into
a memory-bandwidth-bound problem. The literature mitigating this bottleneck is large
but fragmented across the machine-learning, systems, and computer-architecture
communities. Our survey unifies it.

**What the manuscript contributes, and how it differs from existing reviews.**
Several recent surveys address KV cache optimisation (e.g., Li et al., TMLR 2025;
Shi et al., 2024; Xu et al., 2026; Jiang et al., ACL 2026). We position our work
explicitly against all of them in Table 1 and Section 1.4. Four features are, to our
knowledge, unique to this survey:

1. A **hardware-first, four-layer framework** (algorithmic, architectural,
   system, hardware) in which every technique is tied back to a roofline and
   memory-traffic analysis, with an explicit co-design / Pareto treatment of how
   stacked methods interfere.
2. A **consolidated treatment of multi-tenant KV cache security** (prefix-sharing
   side channels, prompt-leakage and timing attacks) — absent from all prior
   KV-cache surveys.
3. An analysis of **cache degradation in long-horizon agentic loops** — likewise
   absent elsewhere.
4. **Matched-Budget Evaluation (MBE)** — a standardised, fixed-budget reporting
   protocol released with an open evaluation harness (Section 10). No prior survey
   in this area proposes an evaluation protocol; we convert the field's
   benchmarking critique into an adoptable artifact.

The manuscript is ~15,500 words with 198 references (current through June 2026),
six tables, and three figures, and includes a survey methodology with a PRISMA-style
flow, a limitations section, and full declarations.

**Originality and ethics.** This work is original, has not been published elsewhere,
and is not under consideration by another journal. A preprint will be posted to
arXiv; the companion MBE protocol and harness are openly available
(github.com/rohithreddybc/mbe-protocol). Any use of generative-AI tools was limited
to language editing and reference organisation; all technical content and conclusions
are the author's own and were verified against primary sources, as stated in the
declarations.

We believe the survey fits the scope of *Artificial Intelligence Review* as a timely,
comprehensive, and genuinely differentiated reference for a rapidly growing field,
with a reusable artifact that should benefit the community well beyond the article
itself.

Thank you for your consideration.

Sincerely,
Rohith Reddy B. C. (corresponding author), on behalf of all authors
[Affiliation] · rohithreddybc98@gmail.com
