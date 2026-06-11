---
layout: page
title: Critique Literature
permalink: /literature/
---
## Critique literature worth reading

- **Zeng, Chen, Zhang, Xu — "Are Transformers Effective for Time Series
  Forecasting?" (AAAI 2023).** One-layer linear models beat sophisticated
  Transformers across the standard LTSF suite — the canonical demonstration
  that the field's comparison tables were not measuring what they claimed.
- **Elsayed et al. — "Do We Really Need Deep Learning Models for Time Series
  Forecasting?" (arXiv:2101.02118).** A well-configured GBRT matches or beats
  most deep baselines of its era.
- **Qiu et al. — "TFB: Towards Comprehensive and Fair Benchmarking of Time
  Series Forecasting Methods" (PVLDB 2024).** Systematic fair re-benchmark;
  documents pipeline bugs (including drop-last evaluation) and shows method
  rankings reorder under a clean protocol.
- **Shao et al. — BasicTS / "Exploring Progress in Multivariate Time Series
  Forecasting" (TKDE).** Fair benchmarking infrastructure for multivariate and
  spatio-temporal forecasting; shows heterogeneity across datasets dominates
  many claimed advances.
- **Hewamalage, Ackermann, Bergmeir — "Forecast evaluation for data
  scientists: common pitfalls and best practices" (DMKD 2023).** The most
  complete pitfalls catalogue: leakage, metric choice, aggregation traps.
- **Bergmeir & Benítez — "On the use of cross-validation for time series
  predictor evaluation" (Information Sciences 2012).** Foundational treatment
  of why naive CV leaks in temporal data and what to do instead.
- **Godahewa et al. — Monash Time Series Forecasting Archive (NeurIPS 2021
  D&B).** Standardised datasets + protocols precisely to stop ad-hoc
  evaluation drift.
- **Makridakis et al. — the M4/M5 competition analyses (IJF).** Blind, held-out
  competitions repeatedly rank methods very differently from self-reported
  benchmark tables.

Cross-domain reality checks with the same lesson: Dacrema et al., "Are We
Really Making Much Progress?" (RecSys 2019); Musgrave et al., "A Metric
Learning Reality Check" (ECCV 2020); Henderson et al., "Deep RL that Matters"
(AAAI 2018); Picard, "torch.manual_seed(3407) is all you need"
(arXiv:2109.08203).

