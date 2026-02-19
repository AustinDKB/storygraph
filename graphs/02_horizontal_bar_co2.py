# CONTEXT
# Audience: Anyone who thinks carbon is evenly distributed
# Insight: Qatar emits 764x more CO2 per person than the Democratic Republic of Congo
# Action: Understand that a handful of nations drive per-capita emissions

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, 'austin_style_kit'))
plt.style.use(os.path.join(ROOT_DIR, 'austin_style_kit', 'my_notebook.mplstyle'))
from austin_annotations import annotate, PALETTE, add_source_note

# Load and prep data
df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'co2_per_capita.csv'))
col = 'CO₂ emissions per capita'
latest = df[df['Year'] == 2023].copy()  # 2023 for more complete data

# Pick a story-driven selection: top 5 emitters + key large economies + bottom 3
top_countries = ['Qatar', 'Kuwait', 'Bahrain', 'United Arab Emirates', 'Saudi Arabia',
                 'Australia', 'United States', 'Canada', 'Russia',
                 'China', 'United Kingdom', 'World', 'India',
                 'Ethiopia', 'Democratic Republic of Congo']

subset = latest[latest['Entity'].isin(top_countries)].copy()
subset = subset.sort_values(col, ascending=True)

# Colors: neutral for everything, primary for USA (relatable anchor), negative for top emitter
colors = []
for country in subset['Entity']:
    if country == 'Qatar':
        colors.append(PALETTE['negative'])
    elif country == 'United States':
        colors.append(PALETTE['primary'])
    else:
        colors.append(PALETTE['neutral'])

# Build the chart
fig, ax = plt.subplots(figsize=(10, 8))

bars = ax.barh(range(len(subset)), subset[col].values, color=colors, height=0.7)

# Y-axis labels
ax.set_yticks(range(len(subset)))
ax.set_yticklabels(subset['Entity'].values, fontsize=11)

# Direct value labels on bars
for i, (val, country) in enumerate(zip(subset[col].values, subset['Entity'].values)):
    if val > 2:
        ax.text(val + 0.3, i, f'{val:.1f}t', va='center', fontsize=10,
                color=PALETTE['negative'] if country == 'Qatar' else
                      PALETTE['primary'] if country == 'United States' else
                      PALETTE['neutral'])
    else:
        ax.text(val + 0.3, i, f'{val:.2f}t', va='center', fontsize=10,
                color=PALETTE['neutral'])

# Declutter
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(left=False, bottom=False)
ax.set_xticks([])

# One annotation — the ratio
qatar_val = subset[subset['Entity'] == 'Qatar'][col].values[0]
drc_val = subset[subset['Entity'] == 'Democratic Republic of Congo'][col].values[0]
ratio = int(qatar_val / drc_val)

qatar_idx = list(subset['Entity'].values).index('Qatar')

# Arrow points at the end of Qatar's bar, text sits below in existing chart space
annotate(ax, f'A person in Qatar emits {ratio}x more than in the DRC',
         xy=(qatar_val, qatar_idx - 0.35),
         xytext=(20, qatar_idx - 6),
         preset='negative',
         arrowprops=dict(
             arrowstyle='->', color=PALETTE['negative'], lw=2,
             connectionstyle='arc3,rad=0.25', shrinkB=0, shrinkA=5,
         ))

# Insight title
ax.text(0, 1.06, 'Carbon inequality: top emitters dwarf the rest of the world',
        transform=ax.transAxes, fontsize=14, fontweight='bold',
        color='#333333')
ax.text(0, 1.02, 'CO\u2082 emissions per capita (tonnes), 2023',
        transform=ax.transAxes, fontsize=11, color='#888888')

add_source_note(ax, 'Source: Our World in Data / Global Carbon Budget 2024')

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, '02_horizontal_bar_co2.png'),
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
print("Saved: graphs/02_horizontal_bar_co2.png")
