# T3 — Protocol decomposition: canonical vs published config (capacity/tuning premium)

| Model | Dataset | pred | Canonical (d256) | Published (tuned) | Premium |
|---|---|---|---|---|---|
| S-Mamba | PEMS03 | 12 | 0.0661 | 0.0656 | +1% |
| S-Mamba | PEMS03 | 24 | 0.0910 | 0.0878 | +4% |
| S-Mamba | PEMS03 | 48 | 0.1422 | 0.1647 | -14% |
| S-Mamba | PEMS03 | 96 | 0.2266 | 0.6062 (DIVERGED) | -63% |
| S-Mamba | PEMS04 | 12 | 0.0770 | 0.0726 | +6% |
| S-Mamba | PEMS04 | 24 | 0.0987 | 0.0843 | +17% |
| S-Mamba | PEMS04 | 48 | 0.1450 | 0.1006 | +44% |
| S-Mamba | PEMS04 | 96 | 0.2240 | 0.1235 | +81% |
| S-Mamba | PEMS07 | 96 | 0.1803 | 0.1182 | +53% |
| S-Mamba | PEMS08 | 12 | 0.0739 | 0.0755 | -2% |
| S-Mamba | PEMS08 | 24 | 0.1002 | 0.1084 | -8% |
| S-Mamba | PEMS08 | 48 | 0.1639 | 0.1632 | +0% |
| S-Mamba | PEMS08 | 96 | 0.2701 | 0.2659 | +2% |