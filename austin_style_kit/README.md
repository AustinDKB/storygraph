# Austin Style Kit

A complete matplotlib styling system for data storytelling. Colorblind-safe, minimal, beautiful.

## Installation

```bash
# Copy style files to matplotlib's style library
mkdir -p ~/.config/matplotlib/stylelib/
cp my_notebook.mplstyle ~/.config/matplotlib/stylelib/
cp austin_presentation.mplstyle ~/.config/matplotlib/stylelib/

# Copy Python modules to your project or site-packages
cp austin_annotations.py /path/to/your/project/
cp austin_colormaps.py /path/to/your/project/
```

## Quick Start

```python
import matplotlib.pyplot as plt

# Load the style
plt.style.use('austin_notebook')  # or 'austin_presentation' for slides

# Use annotation presets
from austin_annotations import annotate, PALETTE
annotate(ax, 'Key insight!', xy=(3, 5), xytext=(5, 7), preset='callout')

# Use colormaps for heatmaps
from austin_colormaps import austin_cmap, austin_diverging
ax.imshow(data, cmap=austin_cmap)
```

---

## Palette

High Contrast, Colorblind Safe:

| Role | Hex | Usage |
|------|-----|-------|
| **Primary** | `#5C2593` | Main data, key callouts, titles |
| **Secondary** | `#0A5E73` | Second series, supporting info |
| **Positive** | `#1A936F` | Wins, increases, good news |
| **Accent** | `#E8B72C` | Highlights, special emphasis |
| **Negative** | `#BF5B04` | Warnings, decreases *(orange, not red!)* |
| **Neutral** | `#4A4A4A` | Context, de-emphasized elements |

Access colors directly:
```python
from austin_annotations import PALETTE
ax.plot(x, y, color=PALETTE['primary'])
```

---

## Style Files

### austin_notebook.mplstyle
- `figure.dpi: 150` — crisp on modern screens
- `savefig.dpi: 300` — high quality exports
- `lines.linewidth: 2.5` — visible but not heavy
- Standard font sizes for screen reading

### austin_presentation.mplstyle
- `figure.figsize: 12, 7` — 16:9 friendly
- `lines.linewidth: 3.5` — visible from back of room
- ~40% larger fonts throughout
- Thicker ticks and spines

**Switch between them:**
```python
# Notebook work
plt.style.use('austin_notebook')

# For slides
with plt.style.context('austin_presentation'):
    fig, ax = plt.subplots()
    # ... create chart ...
    plt.savefig('for_slides.png')
```

---

## Annotations

### Available Presets

| Preset | Use Case |
|--------|----------|
| `'callout'` | Main insights (bold purple arrow) |
| `'callout_box'` | Maximum emphasis (white on purple box) |
| `'subtle'` | Secondary context (gray italic) |
| `'label'` | Just identify a point (simple line) |
| `'highlight'` | Important notes (purple on light background) |
| `'trend'` | Show direction (double-headed arrow) |
| `'positive'` | Good news (sea green) |
| `'negative'` | Bad news (orange) |
| `'neutral'` | Just facts (dark gray) |
| `'accent'` | Special emphasis (gold) |

### Usage

```python
from austin_annotations import annotate, add_source_note

# Basic annotation
annotate(ax, 'Peak revenue!', xy=(7, 85), xytext=(5, 95), preset='positive')

# For presentations (larger)
annotate(ax, 'Key point', xy=(3, 50), xytext=(5, 60), preset='callout', presentation=True)

# Add source note
add_source_note(ax, 'Source: Company data, 2024')
```

---

## Colormaps

### Sequential (Grey → Purple)
For values from 0 to max: percentages, counts, intensity.

```python
from austin_colormaps import austin_cmap
ax.imshow(data, cmap=austin_cmap)
```

### Diverging (Orange → White → Purple)
For data with meaningful center: correlations, change from baseline.

```python
from austin_colormaps import austin_diverging
ax.imshow(corr_matrix, cmap=austin_diverging, vmin=-1, vmax=1)
```

### Available Colormaps

| Colormap | Gradient | Use For |
|----------|----------|---------|
| `austin_cmap` | Grey → Purple | Percentages, counts |
| `austin_cmap_r` | Purple → Grey | Reversed |
| `austin_cmap_extended` | Grey → Purple → Dark | More range |
| `austin_diverging` | Orange → White → Purple | Correlations |
| `austin_diverging_teal` | Teal → White → Purple | Alternative |
| `austin_diverging_green` | Green → White → Purple | Alternative |

### Register for String Access

```python
from austin_colormaps import register_cmaps
register_cmaps()

# Now use by name
ax.imshow(data, cmap='austin')
```

---

## Why Colorblind Safe?

- **Orange for negative** instead of red — 8% of men can't distinguish red/green
- **Purple stays distinct** across all colorblind types
- **Luminance-based sequential** — works even in grayscale
- **Clear white center** in diverging maps

---

## File Structure

```
austin_style_kit/
├── austin_notebook.mplstyle      # Daily notebook work
├── austin_presentation.mplstyle  # Slides and presentations
├── austin_annotations.py         # Annotation presets + PALETTE
├── austin_colormaps.py           # Heatmap colormaps
└── README.md                     # This file
```

---

## Font Note

The style uses **IBM Plex Sans** with fallbacks to DejaVu Sans and Arial.

To install IBM Plex Sans:
- **macOS**: `brew install --cask font-ibm-plex`
- **Linux**: `apt install fonts-ibm-plex`
- **Manual**: Download from https://github.com/IBM/plex/releases

After installing, rebuild matplotlib's font cache:
```python
import matplotlib.font_manager as fm
fm._load_fontmanager(try_read_cache=False)
```
