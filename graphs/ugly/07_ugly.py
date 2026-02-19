# Ugly version: two plain lines with default colors and legend box
import matplotlib.pyplot as plt
import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))

df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'life_expectancy_gender.csv'))
russia = df[df['Entity'] == 'Russia'].sort_values('Year').copy()

fig, ax = plt.subplots()

ax.plot(russia['Year'], russia['Life expectancy of women'], marker='o', markersize=3, label='Women')
ax.plot(russia['Year'], russia['Life expectancy of men'], marker='o', markersize=3, label='Men')
ax.set_title('Life Expectancy in Russia by Gender')
ax.set_ylabel('Life Expectancy (years)', rotation=90)
ax.set_xlabel('Year')
ax.legend()
ax.grid(True)

plt.savefig(os.path.join(SCRIPT_DIR, '07_ugly.png'), dpi=150)
plt.show()
