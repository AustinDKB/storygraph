# CONTEXT
# Audience: Anyone interested in global inequality
# Insight: 44% of the world's population earns less than $15,000 per year
# Action: Global prosperity is concentrated in a small club of rich nations

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
df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'gdp_per_capita.csv'))

# Filter to 2023, drop aggregates and NaN
data = df[(df['year'] == 2023) & df['ny_gdp_pcap_pp_kd'].notna() & df['code'].notna()].copy()
aggregates = ['OWID_WRL', 'OWID_HIC', 'OWID_LIC', 'OWID_UMC', 'OWID_LMC']
data = data[~data['code'].isin(aggregates)]
gdp_values = data['ny_gdp_pcap_pp_kd'].values

# Key stats
n_countries = len(gdp_values)
below_15k = (gdp_values < 15000).sum()
pct_below_15k = below_15k / n_countries * 100

# Build histogram
fig, ax = plt.subplots(figsize=(11, 6))

# Create bins
bins = np.arange(0, 130000, 5000)

# All bars neutral gray, highlight the below-$15K bars in primary
n, bin_edges, patches = ax.hist(gdp_values, bins=bins, color=PALETTE['neutral'],
                                 edgecolor='white', linewidth=0.5, alpha=0.7)

# Color the below-$15K bins in primary purple — the color IS the separator
for patch, left_edge in zip(patches, bin_edges[:-1]):
    if left_edge < 15000:
        patch.set_facecolor(PALETTE['primary'])
        patch.set_alpha(1.0)

# Mark a few key countries as reference points — above their bars
highlights = {'India': PALETTE['primary'], 'United States': PALETTE['neutral'],
              'China': PALETTE['primary']}
for country, color in highlights.items():
    row = data[data['entity'] == country]
    if len(row) > 0:
        val = row['ny_gdp_pcap_pp_kd'].values[0]
        # Find which bin this falls in to get the bar height
        bin_idx = np.searchsorted(bin_edges, val, side='right') - 1
        bin_idx = min(bin_idx, len(n) - 1)
        bar_top = n[bin_idx]
        # Place label above the bar with clearance
        ax.text(val, bar_top + 1.5, country, fontsize=8, color=color,
                ha='center', va='bottom', fontweight='bold')
        ax.plot(val, bar_top + 0.5, marker='v', color=color, markersize=6, zorder=5)

# Declutter
ax.tick_params(left=False, bottom=False)
ax.spines['left'].set_visible(False)
ax.set_ylabel('')
ax.set_xlabel('')

# Format x-axis as dollars
ax.set_xticks([0, 20000, 40000, 60000, 80000, 100000, 120000])
ax.set_xticklabels(['$0', '$20K', '$40K', '$60K', '$80K', '$100K', '$120K'],
                    fontsize=10, color='#666666')

# Axis context
ax.text(0.98, 0.98, f'{n_countries} countries',
        transform=ax.transAxes, fontsize=10, color='#999999',
        ha='right', va='top')

# Annotation — people-centered framing, placed in open space above short gray bars
annotate(ax, f'{pct_below_15k:.0f}% of the world\'s population earns\nless than $15,000 per year',
         xy=(15000, n[2] + 1),
         xytext=(40000, 30),
         preset='callout',
         arrowprops=dict(
             arrowstyle='->', color=PALETTE['primary'], lw=2,
             connectionstyle='arc3,rad=0.15', shrinkA=5, shrinkB=2,
         ))

# Insight title
ax.text(0, 1.08, 'Global wealth is massively skewed — most countries are poor',
        transform=ax.transAxes, fontsize=14, fontweight='bold',
        color='#333333')
ax.text(0, 1.03, 'Distribution of GDP per capita (PPP) across countries, 2023',
        transform=ax.transAxes, fontsize=11, color='#888888')

add_source_note(ax, 'Source: Our World in Data / World Bank 2024')

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, '09_histogram_gdp_distribution.png'),
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
print("Saved: graphs/09_histogram_gdp_distribution.png")
