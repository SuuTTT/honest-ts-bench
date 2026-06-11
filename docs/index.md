---
layout: home
title: honest-ts-bench
---




The long-horizon forecasting literature (LTSF) has a benchmark-integrity problem
that mirrors the RL one this site started with: published comparison tables mix
protocols, copy stale baseline numbers, and occasionally leak test information —
so "SOTA" claims often measure experimental setup, not architecture. This page
catalogues the failure modes, the critique literature documenting them, and a
case study from our own measurements.


**Start here:** [Pitfalls](pitfalls/) · [Critique literature](literature/) ·
[PEMS case study](case-study-pems/) · [Live re-benchmark dashboard (when up)](https://github.com/SuuTTT/honest-ts-bench#live-dashboard)

## The checklist we hold ourselves to

1. Rerun every baseline under one canonical protocol; never copy table rows.
2. At least 3 seeds; report mean and per-seed values; release the raw
   per-seed JSON with the paper.
3. Read every reported number from the metrics file (`metrics.npy`/logs) —
   never retype from memory; keep the provenance log.
4. Fit scalers and graphs on the training split only; no test-window
   information anywhere upstream.
5. Report all datasets attempted, including the nulls and negatives.
6. State divergence handling explicitly; never launder instability into
   accuracy gains.
7. Significance-test headline comparisons (Diebold-Mariano for forecasts).
8. Separate "same-budget" from "tuned-per-method" tables when both exist.

