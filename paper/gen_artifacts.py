#!/usr/bin/env python3
"""Generate all TKDE paper tables (markdown) + figures from results/audit.json.
Run on center (reads JSON, light matplotlib). Outputs to paper/tables/ and paper/figs/."""
import json, os, collections, statistics
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE=os.path.dirname(os.path.abspath(__file__))
D=json.load(open(os.path.join(HERE,'..','results','audit.json')))['results']
os.makedirs(os.path.join(HERE,'tables'),exist_ok=True)
os.makedirs(os.path.join(HERE,'figs'),exist_ok=True)

def cfg(r): return (r.get('config') or '').upper()
def is_published(r):
    c=cfg(r); return ('PUBLISHED' in c) or ('EXACT OFFICIAL' in c) or ('PUBLISHED-STYLE' in c) or ('INTERMEDIATE' in c) or ('D1024' in c)
def is_canonical(r): return not is_published(r)
def std(r):
    s=r.get('seeds_mse')
    return statistics.pstdev(s) if (s and None not in s and len(s)>1) else 0.0
def diverged(r):
    s=r.get('seeds_mse'); return bool(s and any((x or 0)>1.0 for x in s))

PEMS=['PEMS03','PEMS04','PEMS07','PEMS08']; PH_PEMS=[12,24,48,96]; PH_LTSF=[96,192,336,720]
MODELS=['DLinear','PatchTST','Autoformer','FEDformer','Nonstationary_Transformer','TimesNet',
        'Crossformer','iTransformer','S-Mamba','MultiRel','StructMamba','SECrossformer']

def canon_mean(model,ds,pl):
    cands=[r for r in D if r['model']==model and r['dataset']==ds and r['pred_len']==pl and is_canonical(r) and r.get('mean_mse') is not None]
    return cands[0]['mean_mse'] if cands else None

# ---------- T2 MAIN RESULTS (canonical protocol) ----------
def t2():
    lines=["# T2 — Main results (canonical TSLib protocol, MSE, 3-seed mean)\n"]
    for ds in PEMS:
        lines.append(f"\n## {ds}")
        lines.append("| Model | pred-12 | pred-24 | pred-48 | pred-96 |")
        lines.append("|---|---|---|---|---|")
        # best per horizon
        best={pl:min([v for m in MODELS for v in [canon_mean(m,ds,pl)] if v is not None],default=None) for pl in PH_PEMS}
        for m in MODELS:
            row=[m]
            for pl in PH_PEMS:
                v=canon_mean(m,ds,pl)
                if v is None: row.append('—')
                elif v==best[pl]: row.append(f"**{v:.4f}**")
                else: row.append(f"{v:.4f}")
            if any(c!='—' for c in row[1:]): lines.append("| "+" | ".join(row)+" |")
    # Phase-3
    for ds in ['ECL','Traffic']:
        lines.append(f"\n## {ds} (Phase-3, horizons 96/192/336/720)")
        lines.append("| Model | 96 | 192 | 336 | 720 |"); lines.append("|---|---|---|---|---|")
        for m in MODELS:
            row=[m]; any_=False
            for pl in PH_LTSF:
                v=canon_mean(m,ds,pl); row.append('—' if v is None else f"{v:.4f}"); any_=any_ or v is not None
            if any_: lines.append("| "+" | ".join(row)+" |")
    open(os.path.join(HERE,'tables','T2_main.md'),'w').write("\n".join(lines))

# ---------- T3 PROTOCOL DECOMPOSITION ----------
def t3():
    lines=["# T3 — Protocol decomposition: canonical vs published config (capacity/tuning premium)\n",
           "| Model | Dataset | pred | Canonical (d256) | Published (tuned) | Premium |","|---|---|---|---|---|---|"]
    for model in ['S-Mamba','iTransformer']:
        for ds in PEMS:
            for pl in PH_PEMS:
                can=canon_mean(model,ds,pl)
                pubs=[r for r in D if r['model']==model and r['dataset']==ds and r['pred_len']==pl and is_published(r) and r.get('mean_mse')]
                if can and pubs:
                    pub=pubs[0]['mean_mse']
                    prem=f"{(can-pub)/pub*100:+.0f}%" if pub else '—'
                    flag=' (DIVERGED)' if diverged(pubs[0]) else ''
                    lines.append(f"| {model} | {ds} | {pl} | {can:.4f} | {pub:.4f}{flag} | {prem} |")
    open(os.path.join(HERE,'tables','T3_protocol.md'),'w').write("\n".join(lines))

# ---------- T4 REPRODUCIBILITY / DIVERGENCE ----------
def t4():
    lines=["# T4 — Reproducibility: seed-std & divergence (canonical protocol)\n",
           "| Model | worst seed-std | max seed-spread% | diverged cells |","|---|---|---|---|"]
    for m in MODELS:
        cells=[r for r in D if r['model']==m and is_canonical(r) and r.get('seeds_mse') and None not in r['seeds_mse']]
        if not cells: continue
        worst=max(std(r) for r in cells)
        spreads=[(max(r['seeds_mse'])-min(r['seeds_mse']))/min(r['seeds_mse'])*100 for r in cells if min(r['seeds_mse'])>0]
        ndiv=sum(diverged(r) for r in (r2 for r2 in D if r2['model']==m))
        lines.append(f"| {m} | {worst:.4f} | {max(spreads):.0f}% | {ndiv} |")
    open(os.path.join(HERE,'tables','T4_repro.md'),'w').write("\n".join(lines))

# ---------- F3 scale-dependent crossover (SEC vs StructMamba by N, pred-96) ----------
def f3():
    N={'PEMS08':170,'PEMS04':307,'PEMS03':358,'PEMS07':883}
    order=sorted(N,key=N.get)
    sec=[canon_mean('SECrossformer',ds,96) for ds in order]
    sm=[canon_mean('StructMamba',ds,96) for ds in order]
    xs=[N[ds] for ds in order]
    plt.figure(figsize=(5,3.2))
    plt.plot(xs,[s if s else np.nan for s in sec],'s-',color='#C00000',label='SECrossformer')
    plt.plot(xs,[s if s else np.nan for s in sm],'o-',color='#1E7B3C',label='StructMamba')
    for ds in order: plt.annotate(ds,(N[ds],min([v for v in [canon_mean('SECrossformer',ds,96),canon_mean('StructMamba',ds,96)] if v] or [0.3])),fontsize=6)
    plt.xlabel('channel count N'); plt.ylabel('MSE (pred-96)'); plt.title('Scale-dependent winner: SEC (mid-N) vs StructMamba (large-N)')
    plt.legend(fontsize=8); plt.grid(alpha=.3); plt.tight_layout()
    plt.savefig(os.path.join(HERE,'figs','F3_crossover.pdf'),dpi=200); plt.close()

# ---------- F4 variance/stability ----------
def f4():
    groups={'CrossFormer':'Crossformer','iTransformer':'iTransformer','TimesNet':'TimesNet','SECrossformer':'SECrossformer','StructMamba':'StructMamba'}
    data=[]; labels=[]
    for lab,m in groups.items():
        spreads=[(max(r['seeds_mse'])-min(r['seeds_mse']))/min(r['seeds_mse'])*100
                 for r in D if r['model']==m and is_canonical(r) and r.get('seeds_mse') and None not in r['seeds_mse'] and min(r['seeds_mse'])>0]
        if spreads: data.append(spreads); labels.append(lab)
    plt.figure(figsize=(5,3.2))
    plt.boxplot(data,labels=labels,showfliers=True)
    plt.ylabel('seed spread % (max-min)/min'); plt.title('Stability: full-attention vs SE-masked')
    plt.xticks(rotation=20,fontsize=7); plt.grid(alpha=.3,axis='y'); plt.tight_layout()
    plt.savefig(os.path.join(HERE,'figs','F4_variance.pdf'),dpi=200); plt.close()

# ---------- F2 gains vs horizon (SEC/StructMamba best vs iT) ----------
def f2():
    plt.figure(figsize=(5.5,3.2))
    for ds,c in zip(PEMS,['#4472C4','#C00000','#1E7B3C','#ED7D31']):
        it=[canon_mean('iTransformer',ds,pl) for pl in PH_PEMS]
        best=[min([v for v in [canon_mean('SECrossformer',ds,pl),canon_mean('StructMamba',ds,pl)] if v] or [None]) for pl in PH_PEMS]
        g=[ (i-b)/i*100 if (i and b) else np.nan for i,b in zip(it,best)]
        plt.plot(PH_PEMS,g,'o-',color=c,label=ds)
    plt.xlabel('horizon'); plt.ylabel('% improvement over iTransformer'); plt.title('Gains grow with horizon')
    plt.legend(fontsize=8); plt.grid(alpha=.3); plt.tight_layout()
    plt.savefig(os.path.join(HERE,'figs','F2_gains.pdf'),dpi=200); plt.close()

t2(); t3(); t4(); f2(); f3(); f4()
print("tables:", os.listdir(os.path.join(HERE,'tables')))
print("figs:", os.listdir(os.path.join(HERE,'figs')))
