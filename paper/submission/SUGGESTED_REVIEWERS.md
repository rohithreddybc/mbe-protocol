# Suggested reviewers & conflicts

Suggest 4–6 reviewers spanning the survey's three communities (ML compression,
systems/serving, computer architecture). Provide name, affiliation, e-mail, and a
one-line rationale in the submission portal. Below are *profiles* to target — confirm
current affiliation/e-mail before submitting, and avoid anyone with a recent
co-authorship or direct competitive conflict.

## Target reviewer profiles (by expertise)
1. **KV cache quantization** — an author of KIVI / KVQuant / GEAR-class work (ML
   compression). Rationale: can assess §4.1 and the rotation/low-rank families.
2. **Eviction & sparsity** — an author of H2O / SnapKV / Scissorhands-class work.
   Rationale: §4.2 depth and the eviction-signal analysis.
3. **Serving systems** — an author of vLLM/PagedAttention / SGLang / FlexGen-class
   systems. Rationale: §6 (paging, transport, disaggregation) and MBE's system metrics.
4. **Computer architecture / PIM** — a researcher on NeuPIMs/IANUS-class
   accelerators. Rationale: §7 hardware and the roofline framing.
5. **LLM security / privacy** — a researcher on prompt-cache side channels
   (e.g., the PROMPTPEEK / timing-side-channel line). Rationale: §6.2, §9.4.
6. **Long-context evaluation** — a RULER / HELMET / LongBench author. Rationale:
   §9.3 and the MBE protocol's task suite.

## Conflicts to declare / exclude
Exclude authors of the **directly competing surveys** (they have a structural
incentive and a conflict): Li et al. (TMLR 2025), Shi et al. (2024), Liu et al.
(2025), Xu et al. (2026, arXiv:2603.20397), Jiang et al. (ACL 2026), Zhen et al.
(2025). Also exclude anyone at the corresponding author's institution and any recent
co-author.

> Note: these are *suggestions*; the editor selects reviewers. Naming 4–6 qualified,
> conflict-free reviewers speeds handling and reduces the chance of an adversarial
> competing-survey author being assigned.
