# CONTEXT
# Audience: Health policy makers, curious public
# Insight: Schooling (r=0.75) predicts life expectancy better than GDP (r=0.46)
# Action: Invest in education — it saves more lives than raw economic growth

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, 'austin_style_kit'))
plt.style.use(os.path.join(ROOT_DIR, 'austin_style_kit', 'my_notebook.mplstyle'))
from austin_colormaps import austin_diverging, register_cmaps
from austin_annotations import PALETTE, add_source_note

register_cmaps()

# Load data
df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'life_expectancy_who.csv'))

# Select the most meaningful columns (rename for readability)
cols = {
    'Life_expectancy ': 'Life Expectancy',
    'Schooling': 'Schooling',
    'Income_composition_of_resources': 'Income Index',
    ' BMI ': 'BMI',
    'GDP': 'GDP',
    'Alcohol': 'Alcohol',
    'Adult_Mortality': 'Adult Mortality',
    ' HIV/AIDS': 'HIV/AIDS',
    ' thinness  1-19 years': 'Thinness (teens)',
    'Polio': 'Polio Immunization',
    'Diphtheria ': 'Diphtheria Imm.',
}

subset = df[list(cols.keys())].rename(columns=cols).dropna()
corr = subset.corr()

# Build heatmap
fig, ax = plt.subplots(figsize=(10, 8))

im = ax.imshow(corr.values, cmap=austin_diverging, vmin=-1, vmax=1, aspect='auto')

# Labels
ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns, rotation=45, ha='right', fontsize=9)
ax.set_yticklabels(corr.columns, fontsize=9)

# Add correlation values in cells
for i in range(len(corr)):
    for j in range(len(corr)):
        val = corr.iloc[i, j]
        # Only show strong correlations to reduce clutter
        if abs(val) >= 0.4 or (i == j):
            color = 'white' if abs(val) > 0.6 else '#333333'
            fontweight = 'bold' if abs(val) >= 0.7 and i != j else 'normal'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                    fontsize=8, color=color, fontweight=fontweight)

# Colorbar
cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
cbar.set_label('Correlation', fontsize=10, color='#666666')
cbar.ax.tick_params(labelsize=9)

# Declutter
ax.tick_params(left=False, bottom=False)

# One annotation — human-centered schooling insight, placed in subtitle area with clearance
ax.text(0, 1.02, 'Years of schooling (r=0.75) predicts how long people live better than GDP (r=0.46)',
        transform=ax.transAxes, fontsize=10, fontweight='bold',
        color=PALETTE['primary'], ha='left', va='bottom')

# Insight title
ax.text(0, 1.12, 'Education predicts life expectancy more than wealth',
        transform=ax.transAxes, fontsize=14, fontweight='bold',
        color='#333333')
ax.text(0, 1.07, 'Pearson correlations across 193 countries (WHO data)',
        transform=ax.transAxes, fontsize=11, color='#888888')

add_source_note(ax, 'Source: WHO Life Expectancy Dataset / Our World in Data')

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, '06_heatmap_life_expectancy.png'),
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
print("Saved: graphs/06_heatmap_life_expectancy.png")
