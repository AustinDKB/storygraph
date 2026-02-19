# Ugly version: plain line chart with default styling
import matplotlib.pyplot as plt
import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))

df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'temperature_anomaly.csv'))
world = df[df['Entity'] == 'World'].sort_values('Year').copy()

fig, ax = plt.subplots()

ax.plot(world['Year'], world['Average'], marker='o', markersize=2)
ax.fill_between(world['Year'], world['Lower bound'], world['Upper bound'], alpha=0.3)
ax.set_title('Global Temperature Anomaly Over Time')
ax.set_ylabel('Temperature Anomaly (C)', rotation=90)
ax.set_xlabel('Year')
ax.legend(['Average', 'Confidence interval'])
ax.grid(True)

plt.savefig(os.path.join(SCRIPT_DIR, '03_ugly.png'), dpi=150)
plt.show()
