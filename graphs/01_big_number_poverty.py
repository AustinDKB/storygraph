# CONTEXT
# Audience: Anyone who thinks the world is getting worse
# Insight: 130,000 people escaped extreme poverty EVERY DAY for 25 years
# Action: Recognize massive progress while acknowledging work remains

import matplotlib.pyplot as plt
import pandas as pd
import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, 'austin_style_kit'))
plt.style.use(os.path.join(ROOT_DIR, 'austin_style_kit', 'my_notebook.mplstyle'))
from austin_annotations import PALETTE, add_source_note

# Load data
df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'extreme_poverty.csv'))

# Calculate the headline stat: people escaping poverty per day (1990 → 2015)
poverty_1990 = df[df['Year'] == 1990]['Number of people living in extreme poverty'].values[0]
poverty_2015 = df[df['Year'] == 2015]['Number of people living in extreme poverty'].values[0]
years_between = 2015 - 1990
days_between = years_between * 365.25
people_escaped = poverty_1990 - poverty_2015
per_day = int(people_escaped / days_between)

# Build the big number display
fig, ax = plt.subplots(figsize=(10, 6))

# The headline number
ax.text(0.5, 0.58, f'{per_day:,}',
        ha='center', va='center',
        fontsize=96, fontweight='bold',
        color=PALETTE['positive'],
        transform=ax.transAxes)

# Context line
ax.text(0.5, 0.38, 'people escaped extreme poverty every day',
        ha='center', va='center',
        fontsize=20, color=PALETTE['neutral'],
        transform=ax.transAxes)

# Time period
ax.text(0.5, 0.28, 'from 1990 to 2015',
        ha='center', va='center',
        fontsize=16, color='#999999',
        transform=ax.transAxes)

# The supporting stat
ax.text(0.5, 0.12, f'Total: {int(people_escaped/1e6):,} million fewer people in extreme poverty',
        ha='center', va='center',
        fontsize=13, color=PALETTE['neutral'],
        style='italic',
        transform=ax.transAxes)

ax.axis('off')

add_source_note(ax, 'Source: Our World in Data / World Bank PIP')

plt.savefig(os.path.join(SCRIPT_DIR, '01_big_number_poverty.png'),
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
print("Saved: graphs/01_big_number_poverty.png")
