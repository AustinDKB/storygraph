# Ugly version: vertical bar chart with rainbow colors and rotated labels
import matplotlib.pyplot as plt
import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))

df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'co2_per_capita.csv'))
col = 'CO\u2082 emissions per capita'
latest = df[df['Year'] == 2023].copy()

top_countries = ['Qatar', 'Kuwait', 'Bahrain', 'United Arab Emirates', 'Saudi Arabia',
                 'Australia', 'United States', 'Canada', 'Russia',
                 'China', 'United Kingdom', 'World', 'India',
                 'Ethiopia', 'Democratic Republic of Congo']

subset = latest[latest['Entity'].isin(top_countries)].copy()
subset = subset.sort_values(col, ascending=False)

fig, ax = plt.subplots()

ax.bar(range(len(subset)), subset[col].values)
ax.set_xticks(range(len(subset)))
ax.set_xticklabels(subset['Entity'].values, rotation=90)
ax.set_title('CO2 Emissions Per Capita by Country')
ax.set_ylabel('Tonnes CO2 per capita', rotation=90)
ax.legend(['CO2 per capita'])

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, '02_ugly.png'), dpi=150)
plt.show()
