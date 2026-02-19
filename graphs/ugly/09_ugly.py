# Ugly version: histogram with default colors and grid
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))

df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'gdp_per_capita.csv'))

data = df[(df['year'] == 2023) & df['ny_gdp_pcap_pp_kd'].notna() & df['code'].notna()].copy()
aggregates = ['OWID_WRL', 'OWID_HIC', 'OWID_LIC', 'OWID_UMC', 'OWID_LMC']
data = data[~data['code'].isin(aggregates)]

fig, ax = plt.subplots()

ax.hist(data['ny_gdp_pcap_pp_kd'], bins=25)
ax.set_title('Distribution of GDP Per Capita (2023)')
ax.set_xlabel('GDP Per Capita (PPP)')
ax.set_ylabel('Number of Countries', rotation=90)
ax.legend(['Countries'])
ax.grid(True)

plt.savefig(os.path.join(SCRIPT_DIR, '09_ugly.png'), dpi=150)
plt.show()
