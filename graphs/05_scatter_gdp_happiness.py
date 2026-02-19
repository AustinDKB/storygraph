# CONTEXT
# Audience: Anyone who believes money buys happiness
# Insight: Going from $2K to $20K transforms life satisfaction. $20K to $100K barely moves the needle.
# Action: The returns on wealth diminish drastically — after a point, other things matter more

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
df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'gdp_vs_happiness.csv'))
data = df[(df['Year'] == 2023) &
          df['Life satisfaction'].notna() &
          df['GDP per capita'].notna() &
          df['Code'].notna()].copy()

# Remove aggregates
aggregates = ['World', 'High-income countries', 'Low-income countries',
              'Upper-middle-income countries', 'Lower-middle-income countries']
data = data[~data['Entity'].isin(aggregates)]

# Build scatter
fig, ax = plt.subplots(figsize=(11, 7))

# All dots in neutral gray
ax.scatter(data['GDP per capita'], data['Life satisfaction'],
           color=PALETTE['neutral'], alpha=0.35, s=50, edgecolors='none', zorder=2)

# Highlight a few storytelling outliers
highlights = {
    'Finland': PALETTE['primary'],
    'Costa Rica': PALETTE['positive'],
    'United States': PALETTE['primary'],
    'Afghanistan': PALETTE['neutral'],
    'Luxembourg': PALETTE['neutral'],
}

for country, color in highlights.items():
    row = data[data['Entity'] == country]
    if len(row) > 0:
        ax.scatter(row['GDP per capita'], row['Life satisfaction'],
                   color=color, s=90, edgecolors='white', linewidth=1.5, zorder=3)
        # Direct label with clearance from dots
        gdp = row['GDP per capita'].values[0]
        sat = row['Life satisfaction'].values[0]
        offset_x = 1.05
        va = 'center'
        ha = 'left'
        if country == 'Luxembourg':
            va = 'bottom'
        ax.text(gdp * offset_x, sat, country, fontsize=9, color=color,
                fontweight='bold', va=va, ha=ha)

# Log scale for x-axis to show the diminishing returns curve
ax.set_xscale('log')
ax.set_xlim(800, 200000)
ax.set_ylim(1, 8.5)

# Format x-axis as dollars
ax.set_xticks([1000, 2000, 5000, 10000, 20000, 50000, 100000])
ax.set_xticklabels(['$1K', '$2K', '$5K', '$10K', '$20K', '$50K', '$100K'],
                    fontsize=10, color='#666666')

# Declutter
ax.tick_params(left=False, bottom=False)
ax.set_xlabel('')
ax.set_ylabel('')

# Add a log-fit curve to show the diminishing returns
x_fit = np.linspace(data['GDP per capita'].min(), data['GDP per capita'].max(), 200)
log_gdp = np.log(data['GDP per capita'])
coeffs = np.polyfit(log_gdp, data['Life satisfaction'], 1)
y_fit = coeffs[0] * np.log(x_fit) + coeffs[1]
ax.plot(x_fit, y_fit, color=PALETTE['primary'], linewidth=2, alpha=0.4,
        linestyle='--', zorder=1)

# One annotation — human-centered, number-anchored
# Text and arrow target both ABOVE the trend line so the arrow never crosses it
trend_at_20k = coeffs[0] * np.log(20000) + coeffs[1]
annotate(ax, 'People only report +2 life satisfaction beyond $20,000 GDP',
         xy=(20000, trend_at_20k + 0.1),
         xytext=(1500, 7.8),
         preset='callout',
         arrowprops=dict(
             arrowstyle='->', color=PALETTE['primary'], lw=2,
             connectionstyle='arc3,rad=-0.15', shrinkA=5, shrinkB=2,
         ))

# Axis context labels
ax.text(0.02, 0.02, 'GDP per capita (PPP, log scale) \u2192',
        transform=ax.transAxes, fontsize=10, color='#999999')
ax.text(0.01, 0.98, '\u2191 Life satisfaction (0\u201310)',
        transform=ax.transAxes, fontsize=10, color='#999999', va='top')

# Insight title
ax.text(0, 1.08, 'Money buys happiness \u2014 but only up to a point',
        transform=ax.transAxes, fontsize=14, fontweight='bold',
        color='#333333')
ax.text(0, 1.03, 'GDP per capita vs. self-reported life satisfaction, 2023',
        transform=ax.transAxes, fontsize=11, color='#888888')

add_source_note(ax, 'Source: Our World in Data / World Happiness Report 2024')

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, '05_scatter_gdp_happiness.png'),
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
print("Saved: graphs/05_scatter_gdp_happiness.png")
