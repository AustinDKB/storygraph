# Ugly version: grouped bar chart instead of dumbbell chart
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))

df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'child_mortality.csv'))

aggregates = ['OWID_WRL', 'OWID_HIC', 'OWID_LIC', 'OWID_UMC', 'OWID_LMC']
d90 = df[(df['year'] == 1990) & df['code'].notna() & ~df['code'].isin(aggregates)].set_index('entity')['child_mortality_rate']
d23 = df[(df['year'] == 2023) & df['code'].notna() & ~df['code'].isin(aggregates)].set_index('entity')['child_mortality_rate']
both = pd.DataFrame({'y1990': d90, 'y2023': d23}).dropna()

countries = ['Niger', 'Nigeria', 'Somalia', 'Chad', 'Ethiopia', 'Bangladesh',
             'India', 'Brazil', 'China', 'United States', 'Japan', 'France']
sub = both.loc[[c for c in countries if c in both.index]].copy()

x = np.arange(len(sub))
width = 0.35

fig, ax = plt.subplots()

ax.bar(x - width/2, sub['y1990'], width, label='1990')
ax.bar(x + width/2, sub['y2023'], width, label='2023')
ax.set_xticks(x)
ax.set_xticklabels(sub.index, rotation=90)
ax.set_title('Child Mortality Rate by Country')
ax.set_ylabel('Deaths per 100 live births', rotation=90)
ax.legend()
ax.grid(True, axis='y')

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, '10_ugly.png'), dpi=150)
plt.show()
