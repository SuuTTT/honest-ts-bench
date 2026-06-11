# honest-ts-bench

Honest benchmarking for long-horizon time-series forecasting (LTSF) — a
companion to [honest-rl-bench](https://github.com/SuuTTT/honest-rl-bench).

The LTSF literature has a benchmark-integrity problem: published comparison
tables mix protocols, copy stale baseline numbers, and occasionally leak test
information — so "SOTA" claims often measure experimental setup, not
architecture. This project collects:

- a **taxonomy** of the failure modes (stale copied baselines, protocol
  heterogeneity, drop-last/scaler leakage, seed cherry-picking, dataset
  selection bias, divergence laundering, capacity confounds) — `docs/pitfalls.md`
- the **critique literature** documenting them — `docs/literature.md`
- a verified **PEMS case study**: the same models span 1.3–1.7x MSE ranges
  across papers' protocols — `docs/case-study-pems.md`
- a **single-protocol re-benchmark** of recent PEMS forecasters
  (CrossFormer, iTransformer, S-Mamba, DMamba, PatchTST, DLinear, TimesNet,
  MultiRel, StructMamba), all self-run under the canonical Time-Series-Library
  protocol, per-seed results in `results/` — in progress
- a **live dashboard** (`tools/live_dashboard.py`) showing fleet GPUs, active
  runs, and the queue

## The checklist

1. Rerun every baseline under one canonical protocol; never copy table rows.
2. ≥3 seeds; report mean and per-seed values; release the raw per-seed JSON.
3. Read every number from the metrics file; keep the provenance log.
4. Fit scalers/graphs on the training split only.
5. Report all datasets attempted, including nulls and negatives.
6. State divergence handling explicitly.
7. Significance-test headline comparisons (Diebold–Mariano).
8. Separate "same-budget" from "tuned-per-method" tables.

## Live dashboard

```bash
python3 tools/live_dashboard.py --port 5180
# probes the GPU fleet over ssh every 2 minutes; serves HTML at / and JSON at /api/status
```

Site: https://suuttt.github.io/honest-ts-bench
