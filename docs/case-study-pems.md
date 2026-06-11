---
layout: page
title: PEMS Case Study
permalink: /case-study-pems/
---
## Case study: the PEMS leaderboard is protocol soup

While preparing a structural-entropy forecasting paper we reran standard
baselines under the canonical Time-Series-Library protocol (input 96, 3 seeds,
fixed budget) and compared against the numbers circulating in recent Mamba-era
papers. Two findings, both verified from our own `metrics.npy` outputs:

**Published CrossFormer numbers understate it badly.** On PEMS03, published
tables (propagated from iTransformer's Table 9) report MSE 0.121 (pred-24) and
0.262 (pred-96). Our self-run CrossFormer under the canonical protocol:
**0.0874** and **0.1997** — roughly 30% better than its own published row, and
strong enough to beat several methods that "beat CrossFormer" in their tables.

**The same model spans a 1.7x range across papers' protocols.** Canonical-
protocol iTransformer on PEMS03 pred-96 scores 0.2755; the iTransformer row
cited in recent Mamba papers reports 0.164 for the same model and dataset —
a stronger tuned configuration. Any method comparing itself against one of
these numbers while training under the other regime gains (or loses) more from
the protocol than most architectures contribute.

Consequence: ranking claims among recent PEMS forecasters (CrossFormer,
iTransformer, S-Mamba, DMamba, ...) are not currently decidable from published
tables alone. We are running a single-protocol re-benchmark of all of them —
progress on the [dashboard](https://github.com/SuuTTT/honest-ts-bench#live-dashboard).

