# Ugly version: grouped bar chart instead of slope chart
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))

df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'renewables_share.csv'))

countries = ['Denmark', 'United Kingdom', 'Germany', 'Australia', 'Spain',
             'United States', 'China', 'Japan', 'South Korea', 'Russia']

rows = []
for c in countries:
    v2010 = df[(df['Entity'] == c) & (df['Year'] == 2010)]['Renewables'].values
    v2023 = df[(df['Entity'] == c) & (df['Year'] == 2023)]['Renewables'].values
    if len(v2010) > 0 and len(v2023) > 0:
        rows.append({'country': c, 'y2010': v2010[0], 'y2023': v2023[0]})
data = pd.DataFrame(rows)

x = np.arange(len(data))
width = 0.35

fig, ax = plt.subplots()

ax.bar(x - width/2, data['y2010'], width, label='2010')
ax.bar(x + width/2, data['y2023'], width, label='2023')
ax.set_xticks(x)
ax.set_xticklabels(data['country'], rotation=90)
ax.set_title('Renewable Energy Share by Country')
ax.set_ylabel('% Share', rotation=90)
ax.legend()
ax.grid(True, axis='y')

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, '04_ugly.png'), dpi=150)
plt.show()
