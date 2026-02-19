# CONTEXT
# Audience: Anyone interested in how countries power their grid
# Insight: France gets 65% from nuclear while most nations barely use it
# Action: Nuclear is a massive untapped clean energy lever for most countries

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
df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'energy_mix.csv'))

# Countries with diverse energy stories
countries = ['Norway', 'Brazil', 'France', 'Canada', 'Germany',
             'United States', 'Japan', 'China', 'Australia', 'Poland',
             'India', 'South Africa']

# Get 2023 data
cols = ['coal_share_elec', 'gas_share_elec', 'oil_share_elec',
        'nuclear_share_elec', 'hydro_share_elec', 'solar_share_elec',
        'wind_share_elec']
sub = df[df['country'].isin(countries) & (df['year'] == 2023)][['country'] + cols].copy()
sub = sub.set_index('country').fillna(0)

# Group into categories:
# Nuclear = primary purple (THE STORY)
# Renewables (hydro + solar + wind) = positive green
# Fossil (coal + gas + oil) = neutral gray
sub['Nuclear'] = sub['nuclear_share_elec']
sub['Renewables'] = sub['hydro_share_elec'] + sub['solar_share_elec'] + sub['wind_share_elec']
sub['Fossil'] = sub['coal_share_elec'] + sub['gas_share_elec'] + sub['oil_share_elec']

# "Other" fills to 100% so all bars are the same length
sub['Other'] = (100 - sub['Nuclear'] - sub['Renewables'] - sub['Fossil']).clip(lower=0)

# Sort by nuclear share — greatest to least (story = nuclear dominance)
sub = sub.sort_values('Nuclear', ascending=True)
# Nuclear first (leftmost) so the story metric is easy to compare across countries
plot_cols = ['Nuclear', 'Renewables', 'Fossil', 'Other']

# Build stacked horizontal bar
fig, ax = plt.subplots(figsize=(11, 7))

y_pos = range(len(sub))
bar_height = 0.6

colors = {
    'Fossil': PALETTE['neutral'],
    'Other': '#E0E0E0',
    'Renewables': PALETTE['positive'],
    'Nuclear': PALETTE['primary'],
}

# Find top 3 nuclear users for labeling
top3_nuclear = sub['Nuclear'].nlargest(3).index.tolist()

lefts = np.zeros(len(sub))
for col in plot_cols:
    bars = ax.barh(y_pos, sub[col], left=lefts, height=bar_height,
                   color=colors[col])
    # Only label nuclear segments for top 3 nuclear users
    if col == 'Nuclear':
        for i, (country, val, left) in enumerate(zip(sub.index, sub[col], lefts)):
            if country in top3_nuclear and val > 5:
                ax.text(left + val / 2, i, f'{val:.0f}%',
                        ha='center', va='center', fontsize=9,
                        color='white', fontweight='bold')
    lefts += sub[col].values

# Country labels
ax.set_yticks(y_pos)
ax.set_yticklabels(sub.index, fontsize=10)

# Declutter
ax.tick_params(left=False, bottom=False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.set_xlim(0, 100)
ax.set_ylim(-0.5, len(sub) - 0.3)
ax.set_xticks([])

# Direct labels instead of legend — place at top matching the stacking order (left to right)
ax.text(0.02, 1.01, 'Nuclear', transform=ax.transAxes, fontsize=10,
        fontweight='bold', color=PALETTE['primary'], va='bottom')
ax.text(0.14, 1.01, 'Renewables', transform=ax.transAxes, fontsize=10,
        fontweight='bold', color=PALETTE['positive'], va='bottom')
ax.text(0.30, 1.01, 'Fossil', transform=ax.transAxes, fontsize=10,
        fontweight='bold', color=PALETTE['neutral'], va='bottom')
ax.text(0.40, 1.01, 'Other', transform=ax.transAxes, fontsize=10,
        fontweight='bold', color='#E0E0E0', va='bottom')

# No annotation needed — France at 65% vs near-zero for most countries is self-evident.
# The in-bar "65%" label and insight title carry the story.

# Insight title
ax.text(0, 1.12, 'Most countries barely use nuclear — France is the exception',
        transform=ax.transAxes, fontsize=14, fontweight='bold',
        color='#333333')
ax.text(0, 1.07, 'Share of electricity generation by source, 2023',
        transform=ax.transAxes, fontsize=11, color='#888888')

add_source_note(ax, 'Source: Our World in Data / Energy Institute Statistical Review 2024')

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, '08_stacked_bar_electricity_mix.png'),
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
print("Saved: graphs/08_stacked_bar_electricity_mix.png")
