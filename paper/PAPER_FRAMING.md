# TKDE Paper — Framing & Contribution Plan (reframed around the framework)

## Title (working)
**Structure for Free: Backbone-Agnostic SE-Structured Channel Mixing for Multivariate Forecasting**

## One-sentence thesis
Precomputed multi-relational *structural-entropy* (SE) masks are a **zero-parameter, drop-in replacement for channel-mixing** that improves *every* backbone we apply them to — and, under a corrected single-protocol benchmark, the channel-attention "SOTA" the field reports is largely a protocol/capacity artifact.

## Contributions (in order of strength — what the data supports)
1. **The SE-structured channel-mixing framework (PRIMARY).** Three precomputed relation graphs (partial-correlation, Pearson, lead-lag community via 2D structural-entropy minimization) used as per-head binary masks. Backbone-agnostic, zero added parameters. Demonstrated across **three backbones**:
   - iTransformer → **MultiRel** (beats iTransformer on all 4 PEMS)
   - CrossFormer → **SECrossformer** (rescues its instability; best at mid-N traffic)
   - +GRU temporal → **StructMamba** (flagship: robust across scales + non-traffic)
2. **StructMamba (flagship method).** Most robust instantiation — wins large-N (PEMS07) and generalizes to electricity (ECL), beating published iTransformer/MultiRel.
3. **A corrected PEMS/LTSF benchmark (empirical contribution).** Single-protocol re-benchmark (156+ cells, per-seed, released) showing: Mamba's long-horizon lead is mostly capacity (premium up to +81%); published configs *diverge* (S-Mamba, iTransformer, multiple cells); CrossFormer's cited rows were stale-inflated 1.3–3.1×; stability is a hidden axis (full-attention 40–77% seed spread vs SE-masked ~3%).

## What each instantiation is FOR (honest positioning — do NOT overclaim)
| Instantiation | Wins where | Honest boundary |
|---|---|---|
| StructMamba | PEMS07 (large-N), ECL; competitive all PEMS | flagship generalizer |
| SECrossformer | PEMS03/04 (mid-N traffic), big margins | NOT for ECL/Traffic (CrossFormer's off-traffic weakness); value = *fixes instability* + mid-N |
| MultiRel | all PEMS vs iTransformer | the simplest drop-in proof |

**The framework — not any single model — is the contribution.** Each model shows SE structure helps a *different* backbone; together they prove backbone-agnosticism. SECrossformer is the sharpest "structure rescues a strong-but-unstable backbone" demonstration; it is explicitly NOT claimed universal.

## The "structured-dependency" scope claim (turns weaknesses into a principled boundary)
SE masks help when channels have **structured cross-dependencies** (road sensors, building loads). Evidence both ways:
- PEMS (structured road graphs): large gains.
- ECL (building load structure): StructMamba wins.
- Traffic N=862: gains shrink / iTransformer competitive — discuss as scale × structure-density boundary (preliminary; long-horizon runs memory-limited).
- Small-N / diffuse (ETT, Weather, Solar from prior work): ~0 gain — the framework degrades gracefully to the base backbone.

## Tables (status)
- T1 dataset stats ✅ | T2 main results (PEMS ✅, ECL/Traffic filling) | T3 protocol decomposition ✅ | T4 reproducibility/stability ✅ | **T5 SEC + relation ablation (RUNNING)** | T6 efficiency (TODO timings) | T7 k / lookback sensitivity (lookback RUNNING)

## Figures
- F1 framework diagram (SE masks → 3 backbones) | F2 gains vs horizon ✅ | F3 scale-dependent winner ✅ | F4 stability boxplot ✅ | F5 capacity-premium ✅ | F6 SE mask viz ✅

## Reviewer-risk checklist (what would get us rejected, and the mitigation)
- ❌ "SECrossformer claimed universal" → FIX: positioned as backbone-specific demonstration; framework is the claim.
- ❌ "Only traffic" → MITIGATION: ECL generalization (StructMamba beats published iT/MR) + scope claim.
- ❌ "Unfair baselines" → STRENGTH: that's our audit; single protocol, per-seed, released code.
- ❌ "Traffic results weak" → frame as structure-density boundary; lead with PEMS+ECL.
- ✅ Ablation (T5), stability (T4), protocol decomposition (T3) pre-empt the standard "is it real?" critiques.

## Target & model paper
TKDE. Calibrated against Shao et al. (BasicTS, TKDE 2024) — fair-benchmarking rigor + heterogeneity analysis. Our paper adds a *method* (framework) on top of the audit, which is stronger than benchmarking alone.
