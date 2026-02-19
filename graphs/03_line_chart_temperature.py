# CONTEXT
# Audience: Anyone who needs to see the climate signal in one glance
# Insight: 130 years of flat, then an unbroken climb — 2024 hit +1.53C
# Action: The acceleration is undeniable and accelerating

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
df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'temperature_anomaly.csv'))
world = df[df['Entity'] == 'World'].sort_values('Year').copy()

# Build the chart
fig, ax = plt.subplots(figsize=(12, 6))

# Confidence band in light gray
ax.fill_between(world['Year'], world['Lower bound'], world['Upper bound'],
                color='#E8E0F0', alpha=0.5, linewidth=0)

# The line — neutral gray for the flat era, primary purple for the climb
split_year = 1980
before = world[world['Year'] <= split_year]
after = world[world['Year'] >= split_year]

ax.plot(before['Year'], before['Average'], color=PALETTE['neutral'], linewidth=2.5)
ax.plot(after['Year'], after['Average'], color=PALETTE['primary'], linewidth=3)

# Zero baseline
ax.axhline(y=0, color='#CCCCCC', linewidth=1, linestyle='-', zorder=0)

# Declutter
ax.tick_params(left=False, bottom=False)
ax.spines['bottom'].set_visible(False)
ax.set_ylabel('')
ax.set_xlabel('')

# Direct labels at key points
ax.text(1855, -0.2, '1850\nbaseline', fontsize=9, color=PALETTE['neutral'],
        ha='center', va='top')

# End point label
last_year = world['Year'].iloc[-1]
last_val = world['Average'].iloc[-1]
ax.text(last_year + 1, last_val, f'+{last_val:.2f}\u00b0C',
        fontsize=13, fontweight='bold', color=PALETTE['primary'], va='center')

# One annotation — point just below the line so arrow is visible
inflection_val = world[world['Year'] == 1980]['Average'].values[0]
annotate(ax, 'Acceleration begins around 1980',
         xy=(1980, inflection_val - 0.06),
         xytext=(1890, 1.1),
         preset='callout',
         arrowprops=dict(
             arrowstyle='->', color=PALETTE['primary'], lw=2,
             connectionstyle='arc3,rad=-0.2', shrinkB=5, shrinkA=5,
         ))

# Y-axis context — horizontal text in subtitle instead of rotated label
ax.text(0, 1.03, 'Temperature anomaly (\u00b0C vs. 1850\u20131900 baseline)',
        transform=ax.transAxes, fontsize=11, color='#888888')

# Insight title
ax.text(0, 1.08, '130 years of stability, then a relentless climb',
        transform=ax.transAxes, fontsize=14, fontweight='bold',
        color='#333333')

add_source_note(ax, 'Source: Our World in Data / HadCRUT5')

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, '03_line_chart_temperature.png'),
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
print("Saved: graphs/03_line_chart_temperature.png")
