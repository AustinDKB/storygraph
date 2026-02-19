# CONTEXT
# Audience: Anyone tracking the global energy transition
# Insight: Denmark tripled its renewables share in 13 years — from 32% to 86%
# Action: The transition IS happening, at wildly different speeds

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, 'austin_style_kit'))
plt.style.use(os.path.join(ROOT_DIR, 'austin_style_kit', 'my_notebook.mplstyle'))
from austin_annotations import annotate, PALETTE, add_source_note

# Load data
df = pd.read_csv(os.path.join(ROOT_DIR, 'datasets', 'renewables_share.csv'))

# Select countries with dramatic stories
countries = ['Denmark', 'United Kingdom', 'Germany', 'Australia', 'Spain',
             'United States', 'China', 'Japan', 'South Korea', 'Russia']

# Get 2010 and 2023 values
rows = []
for c in countries:
    v2010 = df[(df['Entity'] == c) & (df['Year'] == 2010)]['Renewables'].values
    v2023 = df[(df['Entity'] == c) & (df['Year'] == 2023)]['Renewables'].values
    if len(v2010) > 0 and len(v2023) > 0:
        rows.append({'country': c, 'y2010': v2010[0], 'y2023': v2023[0],
                     'change': v2023[0] - v2010[0]})
data = pd.DataFrame(rows).sort_values('change', ascending=False)

# --- Label collision avoidance ---
y_range = data['y2023'].max() - data['y2010'].min()
min_gap = y_range * 0.03  # minimum 3% gap between labels

def nudge_labels(label_list, min_gap):
    """Sort labels by y-value and nudge overlapping ones apart."""
    labels = sorted(label_list, key=lambda l: l['y'])
    for i in range(1, len(labels)):
        if labels[i]['y'] - labels[i-1]['y'] < min_gap:
            labels[i]['y'] = labels[i-1]['y'] + min_gap
    return labels

# Collect label positions for left and right sides
left_labels = []
right_labels = []
for _, row in data.iterrows():
    if row['country'] == 'Denmark':
        color = PALETTE['primary']
        alpha = 1.0
        bold = True
    elif row['country'] == 'Russia':
        color = PALETTE['negative']
        alpha = 0.8
        bold = True
    else:
        color = PALETTE['neutral']
        alpha = 0.4
        bold = False

    left_labels.append({
        'country': row['country'], 'y': row['y2010'], 'y_orig': row['y2010'],
        'color': color, 'alpha': max(alpha, 0.7), 'bold': bold
    })
    right_labels.append({
        'country': row['country'], 'y': row['y2023'], 'y_orig': row['y2023'],
        'color': color, 'alpha': max(alpha, 0.7), 'bold': bold
    })

left_labels = nudge_labels(left_labels, min_gap)
right_labels = nudge_labels(right_labels, min_gap)

# Build slope chart
fig, ax = plt.subplots(figsize=(10, 8))

# Draw slope lines
for _, row in data.iterrows():
    if row['country'] == 'Denmark':
        color = PALETTE['primary']
        lw = 3
        alpha = 1.0
    elif row['country'] == 'Russia':
        color = PALETTE['negative']
        lw = 2
        alpha = 0.8
    else:
        color = PALETTE['neutral']
        lw = 1.5
        alpha = 0.4

    ax.plot([0, 1], [row['y2010'], row['y2023']], color=color,
            linewidth=lw, alpha=alpha, solid_capstyle='round')

# Place nudged left labels (2010)
for lbl in left_labels:
    ax.text(-0.03, lbl['y'], f"{lbl['country']}  {lbl['y_orig']:.0f}%",
            ha='right', va='center', fontsize=9, color=lbl['color'],
            fontweight='bold' if lbl['bold'] else 'normal',
            alpha=lbl['alpha'])

# Place nudged right labels (2023)
for lbl in right_labels:
    ax.text(1.03, lbl['y'], f"{lbl['y_orig']:.0f}%  {lbl['country']}",
            ha='left', va='center', fontsize=9, color=lbl['color'],
            fontweight='bold' if lbl['bold'] else 'normal',
            alpha=lbl['alpha'])

# Column headers
ax.text(0, 105, '2010', ha='center', fontsize=12, fontweight='bold', color='#555555')
ax.text(1, 105, '2023', ha='center', fontsize=12, fontweight='bold', color='#555555')

# Declutter
ax.set_xlim(-0.35, 1.35)
ax.set_ylim(-5, 110)
ax.axis('off')

# One annotation — Denmark's story
# Place text above and to the right of Denmark's line, in the open space
# Arrow points at Denmark's midpoint, staying on the same side to avoid crossing lines
annotate(ax, '54% increase in only 13 years',
         xy=(0.35, 52),
         xytext=(0.15, 75),
         preset='callout',
         arrowprops=dict(
             arrowstyle='->', color=PALETTE['primary'], lw=2,
             connectionstyle='arc3,rad=0.2', shrinkA=5, shrinkB=3,
         ))

# Insight title
ax.text(0.5, 1.06, 'Denmark tripled its clean energy — Russia barely moved',
        transform=ax.transAxes, fontsize=14, fontweight='bold',
        color='#333333', ha='center')
ax.text(0.5, 1.01, 'Share of electricity from renewable sources (%)',
        transform=ax.transAxes, fontsize=11, color='#888888', ha='center')

add_source_note(ax, 'Source: Our World in Data / Ember Global Electricity Review 2024')

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, '04_slope_chart_renewables.png'),
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
print("Saved: graphs/04_slope_chart_renewables.png")
