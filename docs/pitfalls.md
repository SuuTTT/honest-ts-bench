---
layout: page
title: Pitfalls
permalink: /pitfalls/
---
## A taxonomy of how benchmark numbers go wrong

**1. Copied (stale) baseline numbers.** Papers paste baseline rows from earlier
papers' tables instead of rerunning them. The copied number was produced under a
different protocol — or was weak to begin with — and then propagates for years.
Once one paper inherits a weak CrossFormer or iTransformer row, every follow-up
"beats" it too.

**2. Protocol heterogeneity sold as architecture gains.** Look-back length,
model width, training epochs, learning rate, and batch size all shift MSE by
amounts comparable to claimed architectural improvements. Comparing your
hyperparameter-searched model against baselines at someone else's fixed config
is the single most common pattern. The honest test: rerun *every* model under
*one* protocol, then separately report tuned-per-method results if you must.

**3. Test-set leakage.** Recurring concrete forms:
- normalisation statistics fitted on the full series instead of the training
  split only;
- early stopping or model selection on the *test* split;
- the `drop_last` evaluation bug — discarding the final incomplete test batch,
  which silently drops the hardest windows and inflates scores. TFB (Qiu et
  al., PVLDB 2024) documented this in widely used pipelines.

**4. Seed and run cherry-picking.** Reporting the best of N seeds, omitting
variance, never running significance tests. With 3-seed std on PEMS comparable
to the inter-method gaps at short horizons, a single lucky seed can "win" a
benchmark row.

**5. Dataset selection bias.** Reporting only the datasets where the method
wins; quietly dropping the channel-rich datasets (Traffic, PEMS07) where a
proposed channel-mixing scheme underperforms, or the small-N datasets (ETT)
where it adds nothing.

**6. Divergence laundering.** When a baseline diverges in some seeds, the
choices are: report the diverged mean (inflates your gain), silently rerun, or
report convergence rates. Almost nobody states which they did. If your gain
over a baseline comes from the baseline blowing up in 1/3 seeds, that is a
stability claim, not an accuracy claim — label it as such.

**7. Capacity confounds.** A new architecture evaluated at 4x the parameter
count or training budget of its baselines. Parameter-matched and budget-matched
comparisons are the exception, not the rule.

