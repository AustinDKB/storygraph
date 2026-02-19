# Complete Guide: Data Storytelling Principles in Matplotlib

## Introduction

This guide provides a systematic implementation of major data storytelling principles using Python's matplotlib library, inspired by best practices from the data visualization community. Unlike scattered tutorials that cherry-pick a few techniques, this document covers the complete framework.

## Core Principle 1: Understanding Context

Before writing any code, you must establish three things: who is your audience, what do they need to know, and how will you communicate it to them. This is not a matplotlib problem but a thinking problem. The book emphasizes that context drives every subsequent decision.

**Practical Application in Code:**
Before you start a visualization, write these answers as comments in your code:

```python
# CONTEXT
# Audience: Executive team with limited technical background
# Need: Understand why Q3 sales declined in the Northeast region
# Communication method: Single slide in quarterly review presentation
# Desired action: Approve additional marketing budget for Northeast
```

This forces you to make deliberate choices about complexity, annotations, and emphasis.

## Core Principle 2: Choosing an Effective Visual

The data storytelling framework provides decision frameworks for selecting chart types. The key insight is that most business communication needs only a handful of chart types: simple text, tables, heatmaps, scatterplots, line graphs, slope graphs, vertical bars, horizontal bars, and waterfall charts.

**Matplotlib Implementation Strategy:**

```python
import matplotlib.pyplot as plt
import numpy as np

# When you only need to show a single number, use text instead of a chart
fig, ax = plt.subplots(figsize=(8, 6))
ax.text(0.5, 0.5, '47%', 
        ha='center', va='center', 
        fontsize=120, fontweight='bold',
        color='#4A81BF')
ax.text(0.5, 0.35, 'customer retention rate in Q3',
        ha='center', va='center',
        fontsize=24, color='#555655')
ax.axis('off')
plt.tight_layout()
```

The principle: if you have one or two numbers to show, do not create a chart. Text is more effective.

**For Horizontal Bar Charts (comparing categories):**

```python
# Horizontal bars are superior to vertical bars for categorical comparisons
# because category names are easier to read horizontally
categories = ['Northeast', 'Southeast', 'Midwest', 'West', 'Southwest']
values = [210, 245, 198, 267, 189]

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(categories, values, color='#4A81BF')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(left=False)
ax.set_xlabel('Sales ($ thousands)', color='#555655')
```

**For Line Charts (showing trends over time):**

```python
months = np.arange(1, 13)
revenue = [420, 438, 445, 461, 478, 492, 485, 469, 453, 441, 456, 468]

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(months, revenue, linewidth=2.5, color='#4A81BF')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_xlabel('Month', color='#555655')
ax.set_ylabel('Revenue ($000s)', color='#555655')
```

## Core Principle 3: Clutter is Your Enemy

Best practice emphasizes that every element in your visualization adds cognitive load. The chapter "Clutter is your enemy!" provides the cognitive principle of reducing extraneous elements.

**Implementing Clutter Reduction in Matplotlib:**

### Remove Chart Borders (Spines)

```python
# By default, matplotlib creates a box around plots
# The top and right spines serve no purpose in most business charts

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# For some charts, even left and bottom can be removed
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
```

### Remove Unnecessary Tick Marks

```python
# Tick marks are often redundant visual elements
ax.tick_params(left=False, bottom=False)

# Keep the labels but remove the marks themselves
# This reduces visual noise without sacrificing information
```

### Eliminate or Simplify Gridlines

```python
# Default gridlines are too prominent
# Either remove them entirely or make them subtle

# Remove completely:
ax.grid(False)

# Or make them subtle background elements:
ax.grid(True, axis='y', alpha=0.3, color='#BFBEBE', linestyle='-', linewidth=0.5)
ax.set_axisbelow(True)  # Put gridlines behind data
```

### Remove Data Markers on Line Charts

```python
# For line charts with many points, markers add clutter
# Show the line only, unless you need to emphasize specific points

ax.plot(x, y, linewidth=2.5, color='#4A81BF')  # No marker parameter

# If you must show markers, use them sparingly:
ax.plot(x, y, linewidth=2.5, color='#4A81BF', 
        marker='o', markersize=4, markevery=3)  # Every 3rd point only
```

### Simplify Axis Labels

```python
# Remove redundant axis labels
ax.set_ylabel('')  # If the title makes it clear what the y-axis represents

# Use thousands or millions to avoid long numbers
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1000)}K'))
```

## Core Principle 4: Focus Attention Where You Want It

This principle teaches you to use preattentive attributes to guide the viewer's eye. The key attributes are: size, color, position, and contrast.

### Strategic Use of Color

```python
# Define a consistent color palette based on the book's recommendations
COLORS = {
    'gray1': '#414040',
    'gray2': '#555655', 
    'gray3': '#646369',
    'gray4': '#76787B',
    'gray5': '#828282',
    'gray6': '#929497',
    'gray7': '#A6A6A5',
    'gray8': '#BFBEBE',
    'gray9': '#D9D9D9',
    'blue1': '#174A7E',
    'blue2': '#4A81BF',
    'blue3': '#94B2D7',
    'blue4': '#94AFC5',
    'red1': '#C3514E',
    'red2': '#E6BAB7',
    'green1': '#0C8040',
    'green2': '#9ABB59',
    'orange1': '#F79747'
}

# Use gray for everything except what you want to emphasize
categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 67, 34, 28]

# Highlight category C
bar_colors = [COLORS['gray8'], COLORS['gray8'], COLORS['blue2'], 
              COLORS['gray8'], COLORS['gray8']]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(categories, values, color=bar_colors)
```

### Bold and Color for Text Emphasis

```python
# Use bold text for the key takeaway
ax.text(0.5, 0.9, 'Sales declined 23% in Q3',
        transform=ax.transAxes,
        fontsize=16, fontweight='bold',
        color=COLORS['gray1'])

# Use regular weight for supporting details  
ax.text(0.5, 0.85, 'First quarterly decline in 3 years',
        transform=ax.transAxes,
        fontsize=12, fontweight='normal',
        color=COLORS['gray5'])

# For emphasizing part of a string, use matplotlib's text formatting
# $\bf{text}$ for bold within a string
ax.text(0.5, 0.5, 'The $\bf{critical}$ issue is customer churn',
        ha='center', fontsize=14)
```

### Size as Emphasis

```python
# Make the most important number larger
fig, ax = plt.subplots(figsize=(8, 6))
ax.text(0.5, 0.6, '34%', 
        ha='center', va='center',
        fontsize=80, fontweight='bold',
        color=COLORS['blue2'])
ax.text(0.5, 0.4, 'increase in customer complaints',
        ha='center', va='center',
        fontsize=16, color=COLORS['gray3'])
ax.axis('off')
```

## Core Principle 5: Think Like a Designer

This chapter emphasizes visual hierarchy, accessibility, and thoughtful use of white space.

### Establishing Visual Hierarchy Through Size and Weight

```python
fig, ax = plt.subplots(figsize=(10, 6))

# Title: Largest, boldest
ax.text(0, 1.05, 'Q3 Performance Review',
        transform=ax.transAxes,
        fontsize=18, fontweight='bold',
        color=COLORS['gray1'])

# Subtitle: Smaller, less bold
ax.text(0, 1.00, 'Revenue trends across regions',
        transform=ax.transAxes,
        fontsize=12, fontweight='normal',
        color=COLORS['gray4'])

# Your chart here
ax.plot([1,2,3,4], [10,15,13,17])

# Source/footer: Smallest, lightest
ax.text(1, -0.1, 'Source: Internal sales database',
        transform=ax.transAxes,
        fontsize=8, fontweight='normal',
        color=COLORS['gray7'], ha='right')
```

### Alignment and White Space

```python
# Use consistent alignment and generous margins
fig, ax = plt.subplots(figsize=(10, 6))

# Set explicit margins to create breathing room
plt.subplots_adjust(left=0.15, right=0.95, top=0.90, bottom=0.15)

# Align text elements to create clean visual lines
ax.text(0, 1.05, 'Title Aligned Left', transform=ax.transAxes, ha='left')
ax.text(0, 0.95, 'Subtitle Also Left', transform=ax.transAxes, ha='left')
```

### Accessibility: Color Contrast

```python
# Ensure sufficient contrast between elements
# The book recommends testing your charts in grayscale

# Good contrast example:
ax.plot(x, y1, color=COLORS['blue2'], linewidth=2.5, label='Series 1')
ax.plot(x, y2, color=COLORS['gray4'], linewidth=2.5, label='Series 2')

# This works even in grayscale because of the lightness difference
```

## Core Principle 6: Direct Annotation

One of the most powerful data storytelling principles is replacing legends with direct labels. This eliminates the cognitive task of matching colors to labels.

### Replace Legends with Direct Labels

```python
# BEFORE (typical approach with legend):
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(months, revenue_2023, color=COLORS['blue2'], label='2023')
ax.plot(months, revenue_2024, color=COLORS['gray5'], label='2024')
ax.legend()  # Forces viewer to match colors to labels

# AFTER (direct labeling):
fig, ax = plt.subplots(figsize=(10, 6))
line1 = ax.plot(months, revenue_2023, color=COLORS['blue2'], linewidth=2.5)
line2 = ax.plot(months, revenue_2024, color=COLORS['gray5'], linewidth=2.5)

# Add labels directly on the chart
ax.text(months[-1] + 0.2, revenue_2023[-1], '2023',
        va='center', color=COLORS['blue2'], fontsize=12, fontweight='bold')
ax.text(months[-1] + 0.2, revenue_2024[-1], '2024',
        va='center', color=COLORS['gray5'], fontsize=12, fontweight='bold')
```

### Annotate Key Points

```python
# Use annotations to explain significant events or insights
ax.annotate('Product launch',
            xy=(6, 485),  # Point to annotate
            xytext=(6, 520),  # Where to place text
            arrowprops=dict(arrowstyle='->', color=COLORS['gray5'], lw=1.5),
            fontsize=11, color=COLORS['gray3'],
            ha='center')

# For insights that don't point to a specific data point
ax.text(0.5, 0.95, 'Revenue declined following the August price increase',
        transform=ax.transAxes,
        fontsize=11, color=COLORS['gray3'],
        ha='center', style='italic')
```

### Add Data Labels Directly on Bars

```python
# For bar charts, add values directly on or above bars
categories = ['Q1', 'Q2', 'Q3', 'Q4']
values = [234, 267, 198, 245]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(categories, values, color=COLORS['blue2'])

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'${int(height)}K',
            ha='center', va='bottom',
            fontsize=11, color=COLORS['gray2'])
```

## Core Principle 7: Tell a Story

Best practice emphasizes structuring your visualization around a clear narrative arc. This goes beyond individual chart design to how you sequence and frame information.

### Using Titles as Headlines

```python
# WEAK: Generic descriptive title
ax.set_title('Q3 Sales by Region')

# STRONG: Action-oriented title that conveys the insight
ax.text(0, 1.05, 'Northeast region shows 23% decline in Q3 sales',
        transform=ax.transAxes,
        fontsize=14, fontweight='bold',
        color=COLORS['gray1'])
```

### Progressive Disclosure with Annotations

```python
# Build the story through layered annotations
fig, ax = plt.subplots(figsize=(12, 7))

# The data
ax.plot(months, sales, linewidth=2.5, color=COLORS['blue2'])

# Annotation 1: Establish the trend
ax.text(2, 500, 'Strong growth through Q2',
        fontsize=11, color=COLORS['gray3'], style='italic')

# Annotation 2: Identify the inflection point
ax.annotate('', xy=(7, sales[6]), xytext=(7, 550),
            arrowprops=dict(arrowstyle='->', color=COLORS['red1'], lw=2))
ax.text(7, 560, 'Decline begins in July',
        fontsize=11, color=COLORS['red1'], fontweight='bold', ha='center')

# Annotation 3: Call to action
ax.text(10, 400, 'Action needed to reverse trend',
        fontsize=12, color=COLORS['gray1'], fontweight='bold',
        bbox=dict(boxstyle='round', facecolor=COLORS['gray9'], edgecolor='none'))
```

## Core Principle 8: Gestalt Principles of Visual Perception

The book discusses how humans perceive visual information through principles like proximity, similarity, enclosure, and continuity.

### Proximity: Group Related Elements

```python
# Use spacing to create visual groups
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Increase space between subplots to clearly separate them
plt.subplots_adjust(wspace=0.4)

# Use proximity in annotations
ax1.text(0.5, 1.15, 'Region A Performance',
         transform=ax1.transAxes, ha='center', fontweight='bold')
ax1.text(0.5, 1.08, 'Q1-Q4 2024',
         transform=ax1.transAxes, ha='center', fontsize=10)
# The proximity of these two text elements signals they belong together
```

### Similarity: Consistent Visual Treatment

```python
# Use the same color for all elements that are conceptually related
baseline_color = COLORS['gray6']
highlight_color = COLORS['blue2']

# All baseline regions in gray
for i, region in enumerate(regions):
    if region == 'Northeast':
        color = highlight_color
    else:
        color = baseline_color
    ax.bar(i, values[i], color=color)
```

### Enclosure: Group with Containers

```python
# Use background shading or boxes to group related time periods
ax.axvspan(6, 9, alpha=0.15, color=COLORS['gray8'], zorder=0)
ax.text(7.5, max(sales) * 0.95, 'Problem Period',
        ha='center', fontsize=10, color=COLORS['gray4'], style='italic')
```

### Continuity: Visual Flow

```python
# Connect related data points to show relationships
fig, ax = plt.subplots(figsize=(10, 6))

# Start and end points
start_values = [45, 67, 34, 89, 23]
end_values = [52, 61, 38, 95, 31]
categories = ['A', 'B', 'C', 'D', 'E']

# Draw lines connecting start to end
for i, cat in enumerate(categories):
    color = COLORS['blue2'] if end_values[i] > start_values[i] else COLORS['red1']
    ax.plot([0, 1], [start_values[i], end_values[i]], 
            color=color, linewidth=2, alpha=0.7)
    
ax.set_xlim(-0.2, 1.2)
ax.set_xticks([0, 1])
ax.set_xticklabels(['2023', '2024'])
```

## Complete Example: Putting It All Together

Here is a complete example that integrates all principles:

```python
import matplotlib.pyplot as plt
import numpy as np

# Define color palette
COLORS = {
    'gray1': '#414040', 'gray2': '#555655', 'gray3': '#646369',
    'gray4': '#76787B', 'gray5': '#828282', 'gray8': '#BFBEBE',
    'blue2': '#4A81BF', 'red1': '#C3514E'
}

# Context (written as comments before coding)
# Audience: Department heads in monthly operations review
# Message: Customer service team is falling behind due to August call volume spike
# Action: Approve hiring two additional representatives

# Data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
calls_received = [150, 155, 148, 152, 158, 160, 165, 210, 215, 218, 220, 222]
calls_answered = [148, 153, 147, 151, 157, 159, 164, 175, 170, 165, 168, 170]

# Create figure
fig, ax = plt.subplots(figsize=(12, 7))
plt.subplots_adjust(left=0.1, right=0.95, top=0.85, bottom=0.15)

# Plot data
ax.plot(range(len(months)), calls_received, 
        linewidth=3, color=COLORS['blue2'], zorder=3)
ax.plot(range(len(months)), calls_answered,
        linewidth=3, color=COLORS['gray5'], zorder=3)

# Remove clutter
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(left=False, bottom=False)

# Add subtle gridlines
ax.grid(True, axis='y', alpha=0.3, color=COLORS['gray8'], 
        linestyle='-', linewidth=0.5, zorder=0)
ax.set_axisbelow(True)

# Set axis properties
ax.set_xlim(-0.5, len(months) - 0.5)
ax.set_xticks(range(len(months)))
ax.set_xticklabels(months, fontsize=11, color=COLORS['gray3'])
ax.set_ylabel('Number of Calls', fontsize=11, color=COLORS['gray3'])

# Direct labels instead of legend
ax.text(len(months) - 0.5, calls_received[-1] + 5, 'Calls Received',
        va='bottom', ha='right', fontsize=11, 
        color=COLORS['blue2'], fontweight='bold')
ax.text(len(months) - 0.5, calls_answered[-1] - 5, 'Calls Answered',
        va='top', ha='right', fontsize=11,
        color=COLORS['gray5'], fontweight='bold')

# Highlight the problem period
ax.axvspan(7, 11, alpha=0.1, color=COLORS['red1'], zorder=0)

# Key annotation
ax.annotate('Call volume spiked in August,\nand we have not recovered',
            xy=(7.5, 210), xytext=(9.5, 240),
            fontsize=12, color=COLORS['gray1'],
            arrowprops=dict(arrowstyle='->', color=COLORS['gray4'], lw=1.5),
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor=COLORS['gray8'], linewidth=1.5))

# Title as headline
ax.text(0, 1.12, 'Customer Service falling behind: Gap between calls received and answered continues to grow',
        transform=ax.transAxes,
        fontsize=14, fontweight='bold', color=COLORS['gray1'])

# Subtitle with context
ax.text(0, 1.05, 'Monthly call volumes from January through December 2024',
        transform=ax.transAxes,
        fontsize=11, color=COLORS['gray4'])

# Call to action
ax.text(0.98, 0.05, 'Recommendation: Hire 2 additional representatives to close the gap',
        transform=ax.transAxes, ha='right', fontsize=11,
        color=COLORS['gray2'], style='italic',
        bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['gray9'], 
                 edgecolor='none'))

plt.tight_layout()
plt.savefig('complete_example.png', dpi=300, bbox_inches='tight')
plt.show()
```

## Advanced Techniques

### Creating a Custom Matplotlib Style

Rather than setting these properties for every chart, create a custom style file:

```python
# Save as 'storytelling.mplstyle'
# Then use with: plt.style.use('storytelling')

# Figure properties
figure.figsize: 10, 6
figure.dpi: 100

# Font properties  
font.size: 11
font.family: sans-serif
font.sans-serif: Arial, Helvetica, sans-serif

# Axes properties
axes.spines.left: True
axes.spines.bottom: True
axes.spines.top: False
axes.spines.right: False
axes.edgecolor: 646369
axes.labelcolor: 555655
axes.linewidth: 1.5
axes.grid: True
axes.grid.axis: y
axes.axisbelow: True

# Grid properties
grid.color: BFBEBE
grid.linestyle: -
grid.linewidth: 0.5
grid.alpha: 0.3

# Tick properties
xtick.color: 646369
ytick.color: 646369
xtick.major.size: 0
ytick.major.size: 0

# Line properties
lines.linewidth: 2.5
lines.solid_capstyle: round

# Legend (though we prefer direct labeling)
legend.frameon: False
```

### Reusable Function for Decluttered Charts

```python
def declutter_axes(ax, keep_spines=None):
    """
    Remove visual clutter from matplotlib axes.
    
    Parameters:
    -----------
    ax : matplotlib axes object
    keep_spines : list, optional
        Which spines to keep. Default is ['left', 'bottom']
    """
    if keep_spines is None:
        keep_spines = ['left', 'bottom']
    
    # Remove unwanted spines
    for spine in ['top', 'right', 'left', 'bottom']:
        if spine not in keep_spines:
            ax.spines[spine].set_visible(False)
    
    # Remove tick marks but keep labels
    ax.tick_params(left=False, bottom=False, top=False, right=False)
    
    # Add subtle gridlines on y-axis only
    ax.grid(True, axis='y', alpha=0.3, color='#BFBEBE', 
            linestyle='-', linewidth=0.5, zorder=0)
    ax.set_axisbelow(True)
    
    # Set spine colors to gray
    for spine_name in keep_spines:
        ax.spines[spine_name].set_color('#646369')
    
    # Set tick label colors
    ax.tick_params(colors='#555655')
    
    return ax

# Usage:
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
declutter_axes(ax)
```

## Common Mistakes to Avoid

### Mistake 1: Over-relying on Color

Do not use color as the only way to encode information. Your chart should still be interpretable in grayscale.

```python
# BAD: Only color differentiates these lines
ax.plot(x, y1, color='red')
ax.plot(x, y2, color='blue')

# GOOD: Different line styles plus color
ax.plot(x, y1, color='#C3514E', linewidth=2.5, label='Actual')
ax.plot(x, y2, color='#646369', linewidth=2.5, linestyle='--', label='Target')
# Plus direct labels as discussed earlier
```

### Mistake 2: Using Legends When Direct Labels Would Work

Legends force the viewer to perform extra cognitive work. Use direct labels whenever possible.

### Mistake 3: Including Unnecessary Decimal Places

```python
# BAD: False precision adds clutter
ax.text(0.5, 0.5, f'{value:.3f}%')  # "23.476%"

# GOOD: Round to meaningful precision
ax.text(0.5, 0.5, f'{value:.0f}%')  # "23%"
```

### Mistake 4: Defaulting to Pie Charts

Pie charts are almost never the right choice. Human eyes are poor at comparing angles. Use horizontal bars instead.

```python
# Instead of a pie chart, use horizontal bars
categories = ['Product A', 'Product B', 'Product C', 'Product D']
values = [23, 34, 18, 25]

fig, ax = plt.subplots(figsize=(8, 5))
y_pos = np.arange(len(categories))
ax.barh(y_pos, values, color='#4A81BF')
ax.set_yticks(y_pos)
ax.set_yticklabels(categories)
declutter_axes(ax, keep_spines=['bottom'])
```

### Mistake 5: Not Testing Your Visualization

Before finalizing any chart, ask these questions:
- Can someone understand the main point in 3 seconds?
- Does it still work in grayscale?
- Are there any elements that could be removed without losing meaning?
- Is the title a headline that conveys the insight?
- Have you eliminated the need for a legend through direct labeling?

## Summary Checklist

Before you consider any visualization complete, verify that you have addressed each principle:

**Context**: Have you identified your audience, message, and desired action?

**Visual Choice**: Have you selected the simplest chart type that effectively shows your data?

**Clutter Reduction**: Have you removed unnecessary borders, gridlines, tick marks, data markers, and other visual elements?

**Focus**: Have you used color, size, and position to draw attention to what matters most?

**Design**: Have you established visual hierarchy through consistent font sizes and weights? Is there adequate white space?

**Direct Labeling**: Have you eliminated legends in favor of direct labels on the chart?

**Storytelling**: Does your title convey the insight rather than just describing the data? Have you added annotations that guide the viewer through the narrative?

**Gestalt Principles**: Have you used proximity, similarity, and enclosure to create logical groupings?

**Accessibility**: Does your chart work in grayscale? Is there sufficient contrast between elements?

**Simplicity**: Have you removed every element that does not directly support your message?

## Resources for Further Learning

The GitHub repository by empathy87 provides code implementations of specific figures from the book, though it lacks the systematic framework presented here.

Leonie Monigatti's article on Towards Data Science covers a subset of these techniques with practical examples.

The book itself remains essential reading. The value is not in the specific Excel techniques but in the decision-making framework and cognitive principles that apply regardless of your tools.

## Final Note

The hardest part of applying these principles is not the matplotlib syntax but the discipline to remove elements from your charts. Every beginner instinct tells you to add more color, more labels, more decoration. The data storytelling framework demands the opposite: relentless simplification until only the essential remains. This requires practice and, frankly, courage. Start with one principle at a time, master it, then layer in the next.