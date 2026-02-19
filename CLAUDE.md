# StoryGraph — Claude Code Instructions

## What This Project Is

A data storytelling toolkit for matplotlib. When the user asks a question about data, **you write the full Python/matplotlib code** to answer it — using the austin_style_kit components below. You are the graph engine.

## The Style Kit (always use these)

### Load the Style
```python
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '/home/austin/Desktop/storygraph/austin_style_kit')
plt.style.use('/home/austin/Desktop/storygraph/austin_style_kit/my_notebook.mplstyle')
# For slides: plt.style.use('/home/austin/Desktop/storygraph/austin_style_kit/austin_presentation.mplstyle')
```

### The Palette (always use these colors — never use matplotlib defaults)
```python
from austin_annotations import annotate, PALETTE, add_source_note, add_title_annotation

PALETTE = {
    'primary':   '#5C2593',  # Deep purple — main data, key callouts
    'secondary': '#0A5E73',  # Dark teal — second series
    'negative':  '#BF5B04',  # Deep orange (NOT red) — bad news, decreases
    'positive':  '#1A936F',  # Sea green — good news, increases
    'neutral':   '#4A4A4A',  # Dark gray — context, de-emphasized
    'accent':    '#E8B72C',  # Bright gold — highlights, special callouts
}
```

### Annotation Presets (use instead of raw ax.annotate)
```python
annotate(ax, 'text', xy=(x,y), xytext=(tx,ty), preset='callout')
```
Available presets: `callout`, `callout_box`, `subtle`, `label`, `highlight`, `trend`, `positive`, `negative`, `neutral`, `accent`

### Colormaps (for heatmaps, scatter color-coding)
```python
from austin_colormaps import austin_cmap, austin_diverging, get_n_colors, register_cmaps
```
- Sequential: `austin_cmap` (grey→purple), `austin_cmap_extended`
- Diverging: `austin_diverging` (orange→white→purple), `austin_diverging_teal`, `austin_diverging_green`

---

## Hard Rules (NEVER break these)

### MAXIMUM 3 COLORS per graph
Every graph uses at most 3 colors total. Typical pattern:
- `PALETTE['neutral']` for context/background data (gray)
- `PALETTE['primary']` for the main story (purple)
- ONE more color only if needed for contrast (positive, negative, or secondary)

If you have 10 bars, 8 are neutral gray, 1-2 are colored. That's it.

### EXACTLY 1 KEY INSIGHT per graph
Every graph delivers ONE insight to the viewer — via arrow annotation, colored subtitle, or the title itself. Never zero, never two. See Rule 5 for the three delivery methods and when to use each.

### ACCENT COLOR (gold) is RESERVED
`PALETTE['accent']` (#E8B72C) is ONLY for truly shocking or critical information. If the data isn't genuinely surprising or urgent, do not use it. Most graphs will never use accent. When in doubt, use primary instead.

---

## Storytelling Rules (follow EVERY time you make a graph)

### 1. Title = Insight, Not Label
```
BAD:  "Sales by Region Q3 2024"
GOOD: "Northeast sales dropped 23% — the only region declining"
```
Use `ax.text()` for the title, not `ax.set_title()`. Place it above the axes with `transform=ax.transAxes`.

### 2. No Legends — Use Direct Labels
Never use `ax.legend()`. Instead, place text directly next to lines/bars using the line's color:
```python
ax.text(x_end + 0.3, y_end, 'Series Name', color=PALETTE['primary'], fontweight='bold', va='center')
```

### 3. Gray Everything, Color the Story
Default all data to `PALETTE['neutral']` or light gray. Then color ONLY what matters.
Remember: MAXIMUM 3 colors total.
```python
colors = [PALETTE['neutral']] * len(categories)
colors[important_index] = PALETTE['primary']  # That's 2 colors. Usually enough.
```

**Which color to reach for:**
| Situation | Color | Example |
|---|---|---|
| The main story / key callout | `primary` (purple) | The country you're highlighting, the highlighted bars |
| Good news, improvement, growth | `positive` (green) | Renewables share, life expectancy gains |
| Bad news, decline, danger | `negative` (orange) | Mortality rates, emissions increases |
| A second series for comparison | `secondary` (teal) | A second line on a dual-line chart |
| Context, background, everything else | `neutral` (gray) | All the bars/lines that aren't the story |
| Truly shocking / urgent (rare) | `accent` (gold) | Almost never — see Hard Rules |

Most graphs need only `neutral` + `primary`. Add a third color only when the story requires a contrast (e.g., positive vs negative trend).

### 4. Declutter Aggressively
- Top/right spines already removed by style file
- Remove tick marks: `ax.tick_params(left=False, bottom=False)`
- Remove left spine for bar charts: `ax.spines['left'].set_visible(False)`
- No data markers on lines unless highlighting a specific point
- Round numbers — no unnecessary decimals
- Use `'${}K'.format(int(v/1000))` for large numbers
- NEVER use rotated y-axis labels (`rotation=90`). They overlap tick numbers and are hard to read. Instead, place the y-axis description as a horizontal `ax.text()` above the y-axis or in the subtitle.
- **Reference lines — only when they add information color doesn't already convey.** If bars are already highlighted by color to show a threshold, don't add a redundant median/threshold line. But DO use reference lines when they provide a benchmark the viewer needs: a zero line on a diverging bar chart, an average line that isn't otherwise visible, or a target/goal line the data is being measured against.

### 5. One Insight — the "Why" (three delivery methods)
Every graph delivers ONE key insight. Choose the best method:

**A. Arrow annotation (default)**
Use when the insight points at a specific data element and the arrow can be placed cleanly.
```python
annotate(ax, '44% of the world\'s population earns less than $15,000 per year',
         xy=(15000, bar_top), xytext=(40000, 30), preset='callout',
         arrowprops=dict(arrowstyle='->', color=PALETTE['primary'], lw=2,
                         connectionstyle='arc3,rad=0.15', shrinkA=5, shrinkB=2))
```

**B. Colored subtitle**
Use when the insight adds context the viewer can't see (geographic grouping, human-scale framing) but the data cluster is already visually obvious. Promotes the stat into the title hierarchy:
```python
ax.text(0, 1.14, 'Child mortality has plummeted — but not everywhere',
        transform=ax.transAxes, fontsize=14, fontweight='bold', color='#333333')
ax.text(0, 1.08, '1 in 10 children in Sub-Saharan Africa still don\'t survive to age 5',
        transform=ax.transAxes, fontsize=11, fontweight='bold', color=PALETTE['primary'])
ax.text(0, 1.03, 'Deaths per 100 live births before age 5, 1990 vs 2023',
        transform=ax.transAxes, fontsize=11, color='#888888')
```

**C. Skip entirely**
Use when the chart structure + insight title + direct labels make the story unmissable in 2 seconds. A bar 10x longer than all others, a distribution with extreme skew, a single outlier that dwarfs the rest. The test: if you can't write an annotation that adds information the viewer doesn't already see, leave it out.

**Annotation text style — human-centered, number-anchored, punchy:**
- Frame in terms of **people affected**, not abstract units. Countries are abstract; people are real.
- Include the key number embedded naturally in a sentence about impact
- Keep it to one short line whenever possible
- Pattern: `"[WHO is affected] [WHAT happens] [KEY NUMBER] [CONTEXT]"`

```
GOOD: "44% of the world's population earns less than $15,000 per year"
GOOD: "1 in 10 children in Sub-Saharan Africa still don't survive to age 5"
GOOD: "People only report a +2 on life satisfaction beyond $20,000 GDP"

BAD:  "90 countries — 44% of the world — earn under $15K per person"  (counts countries, not people)
BAD:  "10x GDP increase, only +2 happiness points past $20K"  (metric-focused, not human)
BAD:  "Acceleration begins around 1980"  (vague, no number)
```

### 6. ALL Text Positioning Rules (CRITICAL)
These rules apply to EVERY piece of text on the chart — annotations, direct labels, baseline markers, endpoint labels. Not just annotations.

#### 6a. Direct Label Clearance
Any `ax.text()` label placed near data must have visible whitespace separating it from every visual element:
- **Lines & bands:** Offset text at least 5-10% of the y-axis range away from the nearest line, confidence band, or shaded region
- **Axes & spines:** Never place text so close to the axis edge that it touches or overlaps tick labels, axis lines, or gets clipped. Keep text inside the data area with comfortable margins.
- **Other labels:** When multiple labels cluster at similar y-values (e.g., several countries at 16-19% on a slope chart), manually offset them vertically so they don't overlap. Use at least 2-3% of the y-axis range between stacked labels.

#### 6b. Annotation Positioning
When using arrow annotations, place with precision:

**Arrow target (`xy`)** — point at the EDGE of data, not the center:
- Bars: top/bottom edge (offset by half bar height)
- Lines: just above or below (~2-3% of y-range clearance), clearing any confidence bands
- Scatter: near the dot, not on top of it

**Text position (`xytext`)** — always in the largest empty gap:
- Never on top of bars, lines, labels, or other data
- Never outside the graph area (forces the chart to expand)
- Check that text doesn't sit on ANY series, not just the one being annotated
- Prefer single-line text to reduce footprint

**Arrow path:**
- `connectionstyle='arc3,rad=0.2'` for gentle curves
- NEVER cross a data line or trend line — text and arrow target must be on the SAME SIDE
- `shrinkA=5, shrinkB=2` — pull arrowhead slightly away from text and target

#### 6c. Label Collision Avoidance
When placing direct labels at line endpoints (slope charts, line charts):
- **Detect collisions:** Before placing labels, sort by y-value and check for overlaps. If two labels would be less than ~3% of y-axis range apart, nudge them apart.
- **Nudge algorithm:** Shift overlapping labels up/down by equal amounts to separate them while keeping them close to their true position.
- **Example pattern:**
```python
# Sort labels by y-value, then nudge overlapping ones apart
min_gap = (y_max - y_min) * 0.03
labels_sorted = sorted(labels, key=lambda l: l['y'])
for i in range(1, len(labels_sorted)):
    if labels_sorted[i]['y'] - labels_sorted[i-1]['y'] < min_gap:
        labels_sorted[i]['y'] = labels_sorted[i-1]['y'] + min_gap
```

**Test mentally:** If the annotation/label were removed, would any data element be obscured? If yes, reposition.

### 7. Add Source Notes
```python
add_source_note(ax, 'Source: Statistics Canada, 2024')
```

### 8. Chart Type Selection
| Question Pattern | Chart Type | Notes |
|---|---|---|
| 1-2 numbers | Big text display | No chart needed |
| Compare categories | Horizontal bar | Never pie charts |
| Trend over time | Line chart | Annotate inflection points |
| Before/after (1-2 series) | Slope chart | Connect start→end |
| Before/after (many categories) | Dumbbell chart | Dots connected by lines, sorted by story metric |
| Relationship | Scatter | Add trend line if useful |
| Part of whole | Stacked horizontal bar | Or just horizontal bar |
| Distribution | Histogram or box | Keep it simple |
| Matrix/correlation | Heatmap | Use `austin_diverging` |

### 9. Stacked Bar Rules (CRITICAL for part-of-whole charts)
- **Bars MUST all be the same length (100%).** If your categories don't sum to 100%, add an "Other" category to fill the gap. Uneven bar lengths make the chart look broken and confuse the viewer.
- **Sort order must match the story.** If the story is about nuclear energy, sort by nuclear share. If it's about fossil dependence, sort by fossil share. The sort axis = the narrative axis.
- **Only label the segments that are the STORY.** Don't put % labels on every large segment — only the top 3 entities for the metric you're highlighting. Everything else is context. This keeps the eye on the insight, not on noise.
- **The story metric goes FIRST (leftmost in the bar).** This makes it easy to visually compare that metric across all bars since they all start from the same left edge.
- **Label ALL categories** in the direct-label legend at the top, including "Other". Every color in the chart must be explained.
- Use neutral gray for the "background" category, and color only the 1-2 categories that ARE the story.

---

## The Question Expansion Rule

**When the user asks ONE question about their data, think deeper.** Generate the code that answers their question, but ALSO tell them what other angles would complete the story. Suggest 3-5 follow-up questions like:

- "Your trend chart answers 'how has X changed' — but you should also ask:"
  - "**Who gained the most?** (ranked horizontal bar)"
  - "**When did it shift?** (annotated inflection point)"
  - "**Is the gap growing?** (dual-line with gap shading)"
  - "**What's the headline number?** (big text callout: '+47% since 2010')"

Then offer to generate code for those too.

### Question Expansion Patterns

**If user asks about trends →** also consider: rank, rate of change, inflection points, outliers
**If user asks about comparison →** also consider: over time, gap analysis, which direction is it heading
**If user asks about a single metric →** also consider: breakdown by group, vs benchmark, historical context
**If user asks "what happened" →** also consider: who was affected most, is it getting better/worse, what should we do

---

## Code Generation Rules

1. **Always produce complete, runnable code** — imports, data loading, figure creation, styling, save/show
2. **Always use the style kit** — load the mplstyle, use PALETTE colors, use annotation presets
3. **Always write the insight title first** as a comment, then build the chart around it
4. **Save to PNG** with `plt.savefig('descriptive_name.png', dpi=300, bbox_inches='tight')` and also `plt.show()`
5. **If working in a notebook**, wrap code in a single cell that produces the chart
6. **If the user provides a CSV/DataFrame**, read it and explore it first, then choose the most impactful chart
7. **Comment the context** at the top: audience, message, action
8. **Verify what the data measures before making claims.** If the data is per-country, don't claim "X% of the world's population" unless you've confirmed with population weighting. If the data is GDP per capita, don't call it "income." Match your annotation language to what the data actually represents — or flag the approximation honestly.

## File Locations

- Style files: `austin_style_kit/my_notebook.mplstyle`, `austin_style_kit/austin_presentation.mplstyle`
- Annotations: `austin_style_kit/austin_annotations.py`
- Colormaps: `austin_style_kit/austin_colormaps.py`
- Methodology guide: `storytelling_data.md`
- Example notebook: `austin_style_kit/emplyee_wages_in_canada.ipynb`
- Sample data: `austin_style_kit/test.csv`
