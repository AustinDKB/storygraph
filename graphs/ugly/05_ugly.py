# Ugly version: scatter with default colors and grid
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))

df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'gdp_vs_happiness.csv'))
data = df[(df['Year'] == 2023) &
          df['Life satisfaction'].notna() &
          df['GDP per capita'].notna() &
          df['Code'].notna()].copy()

aggregates = ['World', 'High-income countries', 'Low-income countries',
              'Upper-middle-income countries', 'Lower-middle-income countries']
data = data[~data['Entity'].isin(aggregates)]

fig, ax = plt.subplots()

ax.scatter(data['GDP per capita'], data['Life satisfaction'], marker='o')
ax.set_title('GDP Per Capita vs Life Satisfaction')
ax.set_xlabel('GDP Per Capita (PPP)')
ax.set_ylabel('Life Satisfaction Score', rotation=90)
ax.legend(['Countries'])
ax.grid(True)

plt.savefig(os.path.join(SCRIPT_DIR, '05_ugly.png'), dpi=150)
plt.show()
