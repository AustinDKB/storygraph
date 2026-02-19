# CONTEXT
# Audience: Anyone interested in demographic catastrophes
# Insight: Russian men's life expectancy collapsed to 57 in 1995 while women held at 71 — a 14-year gap
# Action: Understand how economic collapse disproportionately kills men

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
df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'life_expectancy_gender.csv'))
russia = df[df['Entity'] == 'Russia'].sort_values('Year').copy()
russia['gap'] = russia['Life expectancy of women'] - russia['Life expectancy of men']

# Build the chart
fig, ax = plt.subplots(figsize=(12, 6))

# Gap shading
ax.fill_between(russia['Year'],
                russia['Life expectancy of men'],
                russia['Life expectancy of women'],
                color=PALETTE['primary'], alpha=0.08)

# Women's line — neutral (the stable anchor)
ax.plot(russia['Year'], russia['Life expectancy of women'],
        color=PALETTE['neutral'], linewidth=2.5)

# Men's line — primary (the dramatic story)
ax.plot(russia['Year'], russia['Life expectancy of men'],
        color=PALETTE['primary'], linewidth=3)

# Direct labels at end of lines
last = russia.iloc[-1]
ax.text(last['Year'] + 0.8, last['Life expectancy of women'],
        f"Women: {last['Life expectancy of women']:.0f}",
        fontsize=11, fontweight='bold', color=PALETTE['neutral'], va='center')
ax.text(last['Year'] + 0.8, last['Life expectancy of men'],
        f"Men: {last['Life expectancy of men']:.0f}",
        fontsize=11, fontweight='bold', color=PALETTE['primary'], va='center')

# Declutter
ax.tick_params(left=False, bottom=False)
ax.set_ylabel('')
ax.set_xlabel('')
ax.set_xlim(1950, 2030)
ax.set_ylim(48, 85)

# Mark the Soviet collapse
ax.axvline(x=1991, color='#DDDDDD', linewidth=1, linestyle='--', zorder=0)
ax.text(1991, 84, 'Soviet Union\ncollapses', fontsize=8, color='#AAAAAA',
        ha='center', va='top')

# One annotation — human-centered, single line
# Text and arrow target both BELOW the men's line (same side), arrow doesn't cross
worst = russia.loc[russia['gap'].idxmax()]
worst_men = worst['Life expectancy of men']
annotate(ax, f'Russian men lived only {worst_men:.0f} years — 14 fewer than women',
         xy=(worst['Year'], worst_men - 0.5),
         xytext=(1958, 51),
         preset='callout',
         arrowprops=dict(
             arrowstyle='->', color=PALETTE['primary'], lw=2,
             connectionstyle='arc3,rad=0.2', shrinkA=5, shrinkB=2,
         ))

# Insight title
ax.text(0, 1.08, 'The collapse that killed Russian men: a 14-year life expectancy gap',
        transform=ax.transAxes, fontsize=14, fontweight='bold',
        color='#333333')
ax.text(0, 1.03, 'Life expectancy at birth, Russia, 1950\u20132023',
        transform=ax.transAxes, fontsize=11, color='#888888')

add_source_note(ax, 'Source: Our World in Data / UN World Population Prospects 2024')

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, '07_dual_line_life_expectancy.png'),
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
print("Saved: graphs/07_dual_line_life_expectancy.png")
