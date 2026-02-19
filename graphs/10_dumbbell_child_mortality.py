# CONTEXT
# Audience: Anyone who cares about global progress
# Insight: Child mortality has been cut by more than half almost everywhere since 1990 — but Niger still loses 1 in 9 children
# Action: Massive progress is possible, but the hardest-hit nations still need focused intervention

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, 'austin_style_kit'))
plt.style.use(os.path.join(ROOT_DIR, 'austin_style_kit', 'my_notebook.mplstyle'))
from austin_annotations import annotate, PALETTE, add_source_note

# Load data
df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'child_mortality.csv'))

# Get 1990 and 2023 data, drop aggregates
aggregates = ['OWID_WRL', 'OWID_HIC', 'OWID_LIC', 'OWID_UMC', 'OWID_LMC']
d90 = df[(df['year'] == 1990) & df['code'].notna() & ~df['code'].isin(aggregates)].set_index('entity')['child_mortality_rate']
d23 = df[(df['year'] == 2023) & df['code'].notna() & ~df['code'].isin(aggregates)].set_index('entity')['child_mortality_rate']
both = pd.DataFrame({'y1990': d90, 'y2023': d23}).dropna()
both['drop'] = both['y1990'] - both['y2023']

# Select countries with diverse stories — worst still, biggest improvers, reference points
countries = [
    'Niger', 'Nigeria', 'Somalia', 'Chad',       # Still highest
    'Ethiopia', 'Bangladesh', 'India',             # Massive improvers
    'Brazil', 'China',                             # Middle success
    'United States', 'Japan', 'France',            # Already low
]
sub = both.loc[[c for c in countries if c in both.index]].copy()

# Sort by 2023 rate — worst at top
sub = sub.sort_values('y2023', ascending=True)

# Build dumbbell chart
fig, ax = plt.subplots(figsize=(11, 7))

y_pos = range(len(sub))

# Draw connecting lines (gray, showing the journey)
for i, (country, row) in enumerate(sub.iterrows()):
    ax.plot([row['y1990'], row['y2023']], [i, i],
            color=PALETTE['neutral'], linewidth=1.5, alpha=0.4, zorder=1)

# 1990 dots — gray (the past)
ax.scatter(sub['y1990'], y_pos, color=PALETTE['neutral'], s=50, zorder=2, alpha=0.6)

# 2023 dots — primary purple (the present / the story)
ax.scatter(sub['y2023'], y_pos, color=PALETTE['primary'], s=50, zorder=3)

# Country labels
ax.set_yticks(list(y_pos))
ax.set_yticklabels(sub.index, fontsize=10)

# Direct labels for the two years — at the top of the chart
ax.text(sub['y1990'].max() + 0.5, len(sub) - 0.5, '1990', fontsize=10,
        color=PALETTE['neutral'], fontweight='bold', ha='left', va='bottom')
ax.text(sub['y2023'].iloc[-1] - 0.5, len(sub) - 0.5, '2023', fontsize=10,
        color=PALETTE['primary'], fontweight='bold', ha='right', va='bottom')

# Declutter
ax.tick_params(left=False, bottom=False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.set_xlim(-1, sub['y1990'].max() + 2)

# Format x-axis as percentages
ax.set_xlabel('')
xticks = [0, 5, 10, 15, 20, 25, 30, 35]
ax.set_xticks(xticks)
ax.set_xticklabels([f'{x}%' for x in xticks], fontsize=10, color='#666666')

# No arrow annotation — the insight is front-loaded in the subtitle instead.
# The cluster of 4 Sub-Saharan countries at the top makes the story visually obvious.

# Insight title — three-tier: bold insight, purple stat, gray metadata
ax.text(0, 1.14, 'Child mortality has plummeted — but not everywhere',
        transform=ax.transAxes, fontsize=14, fontweight='bold',
        color='#333333')
ax.text(0, 1.08, '1 in 10 children in Sub-Saharan Africa still don\'t survive to age 5',
        transform=ax.transAxes, fontsize=11, fontweight='bold',
        color=PALETTE['primary'])
ax.text(0, 1.03, 'Deaths per 100 live births before age 5, 1990 vs 2023',
        transform=ax.transAxes, fontsize=11, color='#888888')

add_source_note(ax, 'Source: Our World in Data / UN Inter-agency Group for Child Mortality 2024')

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, '10_dumbbell_child_mortality.png'),
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
print("Saved: graphs/10_dumbbell_child_mortality.png")
