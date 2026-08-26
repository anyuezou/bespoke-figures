# -*- coding: utf-8 -*-
"""Broken-scale radial (polar) paper chart from a generic table.
Recipe: recipes/broken-radial.md

Usage:
  python3 chart_broken_radial.py <data.xlsx> <outstem> ["Line1|Line2|Line3"]
  - centre title lines separated by '|'; default "Risk|Quotient|(RQ)";
    pass "" for no centre title.
Outputs <outstem>.png and <outstem>.svg.

Guards/behaviour:
  - the total column is recognised only when its name contains "sum"
    (case-insensitive); otherwise no total bar is drawn
  - errors out when the table has no positive values; skips rows whose
    total is <= 0 with a warning
  - prints a warning when Times New Roman is missing (falls back to default
    serif) and when more series than palette colours are present (reuse)
  - the bottom note mentions red/orange reference circles only when those
    decades actually fall inside the axis range

No personal data is hardcoded: paths/names come from argv, colours are
assigned by column order from a generic palette.
"""
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch

xlsx = sys.argv[1]
stem = sys.argv[2]
title_lines = (sys.argv[3] if len(sys.argv) > 3 else 'Risk|Quotient|(RQ)').split('|')
if title_lines == ['']:
    title_lines = []

# ---- Times New Roman + STIX, with an existence check ----
from matplotlib import font_manager as _fm
_fonts = {f.name for f in _fm.fontManager.ttflist}
if 'Times New Roman' not in _fonts:
    print('WARN: Times New Roman not found; falling back to default serif')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'stix'

DF = pd.read_excel(xlsx)
LABELS = [str(x) for x in DF.iloc[:, 0].tolist()]
sum_col = DF.columns[-1] if 'sum' in str(DF.columns[-1]).lower() else None
SERIES = [c for c in DF.columns[1:] if c != sum_col]

PALETTE = ['#E6194B', '#3CB44B', '#4363D8', '#F58231', '#911EB4', '#42D4F4',
           '#F032E6', '#BCF60C', '#9A6324', '#800000', '#808000', '#E6BEFF',
           '#FF7F0E', '#00BFC4', '#C49799', '#8C564B', '#7F7F7F', '#E7CB94']
if len(SERIES) > len(PALETTE):
    print(f'WARN: {len(SERIES)} series > {len(PALETTE)} palette colours; colours will be reused')
COLORS = {c: PALETTE[i % len(PALETTE)] for i, c in enumerate(SERIES)}
SUM_COLOR = '#333333'

# ---- value range + adaptive break ----
vals = []
for _, r in DF.iterrows():
    for c in SERIES:
        v = float(r[c])
        if v > 0:
            vals.append(v)
    if sum_col is not None and float(r[sum_col]) > 0:
        vals.append(float(r[sum_col]))
if not vals:
    raise SystemExit('ERROR: table has no positive values; nothing to plot')
vals = np.array(vals)
vlo = 10 ** np.floor(np.log10(vals.min()))
vhi = 10 ** np.ceil(np.log10(vals.max()))
lo_l = int(round(np.log10(vlo)))
hi_l = int(round(np.log10(vhi)))
break_l = int(round((lo_l + hi_l) / 2))
vbr = 10 ** break_l

R0 = 0.4
H_IN = 1.9
H_OUT = 1.55
R_BREAK = R0 + H_IN
R_TOP = R_BREAK + H_OUT
IN_LOG = break_l - lo_l
OUT_LOG = hi_l - break_l
if IN_LOG <= 0:
    IN_LOG = OUT_LOG + 1
if OUT_LOG <= 0:
    OUT_LOG = IN_LOG + 1

def r_of(v):
    lv = np.log10(v)
    if lv <= break_l:
        return R0 + (lv - lo_l) / IN_LOG * H_IN
    return R_BREAK + (lv - break_l) / OUT_LOG * H_OUT

N = len(LABELS)
SLOT = 2 * np.pi / N

fig = plt.figure(figsize=(11, 9.5))
ax = fig.add_subplot(111, projection='polar')
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)

# ---- grouped bars per label (+ total bar when recognised) ----
for i in range(N):
    row = DF.iloc[i]
    theta_c = i * 2.0 * np.pi / N
    vals_pt = [(c, float(row[c])) for c in SERIES if float(row[c]) > 0]
    total = float(row[sum_col]) if sum_col is not None else 0.0
    if sum_col is not None and total <= 0:
        print(f'WARN: row {LABELS[i]} total <= 0; skipping its total bar')
    has_total = sum_col is not None and total > 0
    k = len(vals_pt) + (1 if has_total else 0)
    bw = SLOT * 0.72 / max(k, 1)
    for j, (c, v) in enumerate(vals_pt):
        a = theta_c + (j - (k - 1) / 2.0) * bw * 1.05
        ax.bar(a, r_of(v) - R0, width=bw, bottom=R0,
               color=COLORS[c], edgecolor='white', linewidth=0.35, zorder=3)
    if has_total:
        a_sum = theta_c + (k - 1 - (k - 1) / 2.0) * bw * 1.05
        ax.bar(a_sum, r_of(total) - R0, width=bw * 0.7, bottom=R0,
               color=SUM_COLOR, edgecolor='white', linewidth=0.4, zorder=4)

# ---- dashed sector dividers ----
for i in range(N):
    theta_b = (i + 0.5) * 2.0 * np.pi / N
    ax.plot([theta_b, theta_b], [0.0, R_TOP + 0.35], color='#9A9A9A',
            ls='--', lw=0.8, alpha=0.75, zorder=2)

# ---- reference circles at each decade in range ----
th = np.linspace(0, 2 * np.pi, 720)
for k in range(lo_l, hi_l + 1):
    col = '#D62728' if k == 0 else ('#FF7F0E' if k == -1 else '#C8C8C8')
    lw = 1.5 if k in (0, -1) else 0.7
    ax.plot(th, np.full_like(th, r_of(10 ** k)), color=col, ls='--', lw=lw, zorder=5)
ax.plot(th, np.full_like(th, R_BREAK), color='#999999', ls='--', lw=1.1, zorder=5)

ax.set_rlim(0, R_TOP + 0.95)
ax.set_yticks([])

# ---- scale labels along east ray; small 'break' tight under the break value ----
tbr = None
for k in range(lo_l, hi_l + 1):
    lab = f'$10^{{{k}}}$'
    col = '#B00000' if k == 0 else ('#C26200' if k == -1 else '#333333')
    tx = ax.text(np.deg2rad(90), r_of(10 ** k) + 0.10, lab, fontsize=9, color=col,
                 rotation=0, ha='left', va='center', zorder=6,
                 bbox=dict(fc='white', ec='none', alpha=0.92, pad=1.0))
    if k == break_l:
        tbr = tx
if tbr is not None:
    ax.annotate('break', xy=(0, 0), xycoords=tbr, xytext=(0, -1),
                textcoords='offset points', fontsize=6.5, color='#444444',
                ha='left', va='top', zorder=6,
                bbox=dict(fc='white', ec='none', alpha=0.9, pad=0.6))

ax.set_thetagrids(np.arange(N) * 360.0 / N, LABELS, fontsize=7)
ax.tick_params(axis='x', length=0, pad=5)
ax.grid(False)
ax.spines['polar'].set_linewidth(1.0)

# ---- centre title (parameterized) ----
if title_lines:
    ax.text(0, 0, '\n'.join(title_lines), ha='center', va='center',
            fontsize=7.5, fontweight='bold', zorder=7,
            linespacing=1.35, bbox=dict(fc='white', ec='none', alpha=0.88, pad=1.0))

handles = [Patch(facecolor=COLORS[c], edgecolor='white', label=c) for c in SERIES]
if sum_col is not None:
    handles.append(Patch(facecolor=SUM_COLOR, label=str(sum_col)))
ax.legend(handles=handles, loc='center left', bbox_to_anchor=(1.09, 0.5),
          fontsize=9, frameon=False, handlelength=2.2, handleheight=1.6, labelspacing=0.7)

# ---- bottom note (dynamic: thresholds only when their decades are on-axis) ----
note = f'broken radial axis at {vbr:g}  \u00b7  inner zone {vlo:g}\u2013{vbr:g} (expanded)  \u00b7  outer zone {vbr:g}\u2013{vhi:g} (compressed)'
parts = []
if 0 in range(lo_l, hi_l + 1):
    parts.append('red = 1')
if -1 in range(lo_l, hi_l + 1):
    parts.append('orange = 0.1')
if sum_col is not None:
    parts.append('dark bar = Total')
if parts:
    note += '  \u00b7  ' + '  \u00b7  '.join(parts)
fig.subplots_adjust(left=0.06, right=0.73, top=0.96, bottom=0.04)
fig.text(0.03, 0.03, note, fontsize=8.5, color='#444444', ha='left', va='bottom',
         fontfamily='serif')

matplotlib.rcParams['svg.fonttype'] = 'path'
fig.savefig(stem + '.svg', format='svg')
fig.savefig(stem + '.png', dpi=200)
print('saved', stem + '.svg', stem + '.png')
