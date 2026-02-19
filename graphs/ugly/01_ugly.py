# Ugly version: default matplotlib bar chart instead of a big number display
import matplotlib.pyplot as plt
import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))

df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'extreme_poverty.csv'))

fig, ax = plt.subplots()

ax.bar(df['Year'], df['Number of people living in extreme poverty'] / 1e9)
ax.set_title('Number of People in Extreme Poverty')
ax.set_ylabel('People (billions)')
ax.set_xlabel('Year')
ax.legend(['Extreme poverty'])

plt.savefig(os.path.join(SCRIPT_DIR, '01_ugly.png'), dpi=150)
plt.show()
