# Ugly version: heatmap with default colormap and styling
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))

df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'life_expectancy_who.csv'))

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

fig, ax = plt.subplots()

im = ax.imshow(corr.values, aspect='auto')
ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns, rotation=90, fontsize=7)
ax.set_yticklabels(corr.columns, fontsize=7)
ax.set_title('Correlation Matrix - Life Expectancy Factors')
plt.colorbar(im, ax=ax)

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, '06_ugly.png'), dpi=150)
plt.show()
