# Ugly version: stacked bar with default rainbow colors
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))

df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'energy_mix.csv'))

countries = ['Norway', 'Brazil', 'France', 'Canada', 'Germany',
             'United States', 'Japan', 'China', 'Australia', 'Poland',
             'India', 'South Africa']

cols = ['coal_share_elec', 'gas_share_elec', 'oil_share_elec',
        'nuclear_share_elec', 'hydro_share_elec', 'solar_share_elec',
        'wind_share_elec']
sub = df[df['country'].isin(countries) & (df['year'] == 2023)][['country'] + cols].copy()
sub = sub.set_index('country').fillna(0)

fig, ax = plt.subplots()

sub.plot(kind='barh', stacked=True, ax=ax)
ax.set_title('Electricity Mix by Country (2023)')
ax.set_xlabel('Share (%)')
ax.legend(fontsize=7, title='Source')

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, '08_ugly.png'), dpi=150)
plt.show()
