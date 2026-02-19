"""
AUSTIN COLORMAPS: Custom colormaps for heatmaps and visualizations
===================================================================

Grey-to-purple sequential and orange-white-purple diverging colormaps
that match the Austin Style High Contrast palette. Colorblind safe.

USAGE:
    from austin_colormaps import austin_cmap, austin_diverging, register_cmaps
    
    # Use directly
    ax.imshow(data, cmap=austin_cmap)
    sns.heatmap(data, cmap=austin_cmap)
    
    # Or register with matplotlib for string access
    register_cmaps()
    ax.imshow(data, cmap='austin')
    ax.imshow(data, cmap='austin_diverging')

"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


# ============================================================
# COLOR DEFINITIONS (High Contrast Palette)
# ============================================================

# Primary purple
PURPLE = '#5C2593'
PURPLE_DARK = '#3D1866'
PURPLE_LIGHT = '#B794D4'
PURPLE_VERY_LIGHT = '#EDE7F3'

# Palette colors (for diverging)
ORANGE = '#BF5B04'      # Negative (deep orange)
TEAL = '#0A5E73'        # Secondary (dark teal)
GREEN = '#1A936F'       # Positive (sea green)
GOLD = '#E8B72C'        # Accent


# ============================================================
# SEQUENTIAL COLORMAP: Grey → Purple
# ============================================================
# Use for: Values from 0 to max (percentages, counts, intensity)
# Light grey = low, Dark purple = high

_seq_colors = [
    '#F0F0F0',      # Light grey (low)
    '#D8CDE3',      # Grey-lavender
    '#B794D4',      # Medium purple
    '#8B5CAB',      # Purple
    PURPLE,         # Your primary purple (high)
]

austin_cmap = mcolors.LinearSegmentedColormap.from_list(
    'austin', _seq_colors, N=256
)

# Reversed version (purple to grey)
austin_cmap_r = mcolors.LinearSegmentedColormap.from_list(
    'austin_r', _seq_colors[::-1], N=256
)


# ============================================================
# SEQUENTIAL EXTENDED: Goes darker past primary
# ============================================================
# Use for: When you need more range at the high end

_seq_extended_colors = [
    '#F5F5F5',      # Near white (low)
    '#E0D4EB',      # Very light purple
    '#C4A8D8',      # Light purple
    '#A77CC4',      # Medium purple
    PURPLE,         # Primary purple
    '#471D75',      # Dark purple
    '#2E1150',      # Very dark purple (high)
]

austin_cmap_extended = mcolors.LinearSegmentedColormap.from_list(
    'austin_extended', _seq_extended_colors, N=256
)


# ============================================================
# DIVERGING COLORMAP: Orange → White → Purple
# ============================================================
# Use for: Data with meaningful center (correlations, change from baseline)
# Orange = negative, White = zero, Purple = positive

_div_colors = [
    ORANGE,         # Strong negative (deep orange)
    '#E5A97A',      # Light orange
    '#FAFAFA',      # Near white (center/zero)
    '#B794D4',      # Light purple  
    PURPLE,         # Strong positive (your purple)
]

austin_diverging = mcolors.LinearSegmentedColormap.from_list(
    'austin_diverging', _div_colors, N=256
)

# Reversed version
austin_diverging_r = mcolors.LinearSegmentedColormap.from_list(
    'austin_diverging_r', _div_colors[::-1], N=256
)


# ============================================================
# ALTERNATIVE DIVERGING: Teal → White → Purple
# ============================================================
# Use for: When orange doesn't fit semantically

_div_teal_colors = [
    TEAL,           # Negative (dark teal)
    '#6A9BA8',      # Light teal
    '#FAFAFA',      # Center
    '#B794D4',      # Light purple
    PURPLE,         # Positive (purple)
]

austin_diverging_teal = mcolors.LinearSegmentedColormap.from_list(
    'austin_diverging_teal', _div_teal_colors, N=256
)


# ============================================================
# ALTERNATIVE DIVERGING: Green → White → Purple
# ============================================================
# Use for: When you want positive=purple, negative=green

_div_green_colors = [
    GREEN,          # Negative (sea green)
    '#7DC4A8',      # Light green
    '#FAFAFA',      # Center
    '#B794D4',      # Light purple
    PURPLE,         # Positive (purple)
]

austin_diverging_green = mcolors.LinearSegmentedColormap.from_list(
    'austin_diverging_green', _div_green_colors, N=256
)


# ============================================================
# REGISTER WITH MATPLOTLIB
# ============================================================

def register_cmaps():
    """
    Register Austin colormaps with matplotlib so you can use them by string name.
    Uses plt.register_cmap for broad compatibility across Matplotlib versions.
    """
    cmaps_to_register = [
        ('austin', austin_cmap),
        ('austin_r', austin_cmap_r),
        ('austin_extended', austin_cmap_extended),
        ('austin_diverging', austin_diverging),
        ('austin_diverging_r', austin_diverging_r),
        ('austin_diverging_teal', austin_diverging_teal),
        ('austin_diverging_green', austin_diverging_green),
    ]

    for name, cmap in cmaps_to_register:
        try:
            plt.register_cmap(name=name, cmap=cmap)
        except Exception:
            # Already registered or other registration issue — ignore
            pass


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_color_at(value, cmap=austin_cmap, vmin=0, vmax=1):
    """
    Get a specific color from the colormap at a given value.
    
    Parameters
    ----------
    value : float
        The value to get color for
    cmap : colormap
        Which colormap to use
    vmin, vmax : float
        The range of values
    
    Returns
    -------
    color : tuple
        RGBA color tuple
    
    Example
    -------
    color = get_color_at(0.75)
    ax.bar(x, y, color=color)
    """
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    return cmap(norm(value))



def get_n_colors(n, cmap=austin_cmap):
    """
    Get n evenly-spaced colors from the colormap.

    Returns list of hex color strings. Handles n <= 0 and n == 1 safely.
    """
    if n <= 0:
        return []
    if n == 1:
        return [mcolors.to_hex(cmap(0.5))]
    return [mcolors.to_hex(cmap(i / (n - 1))) for i in range(n)]


def show_colormaps():
    """Display all Austin colormaps (robust when there is only one axis)."""
    cmaps_to_show = [
        ('austin (sequential)', austin_cmap),
        ('austin_r (reversed)', austin_cmap_r),
        ('austin_extended', austin_cmap_extended),
        ('austin_diverging', austin_diverging),
        ('austin_diverging_teal', austin_diverging_teal),
        ('austin_diverging_green', austin_diverging_green),
    ]

    n = len(cmaps_to_show)
    fig, axes = plt.subplots(n, 1, figsize=(10, n * 0.6 + 1))
    # Ensure axes is always iterable (even when n == 1)
    axes = np.atleast_1d(axes)

    fig.suptitle('Austin Colormaps', fontsize=14, fontweight='bold')
    gradient = np.linspace(0, 1, 256).reshape(1, -1)

    for ax, (name, cmap) in zip(axes, cmaps_to_show):
        ax.imshow(gradient, cmap=cmap, aspect='auto')
        ax.set_ylabel(name, rotation=0, ha='right', va='center', fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])

    plt.tight_layout()
    plt.show()

def show_colormap_demo():
    """Show colormaps in realistic heatmap context."""
    
    np.random.seed(42)
    data_seq = np.random.rand(8, 10) * 100
    data_div = np.random.randn(8, 8)
    data_div = (data_div + data_div.T) / 2  # Make symmetric
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Sequential
    im1 = axes[0].imshow(data_seq, cmap=austin_cmap, aspect='auto')
    axes[0].set_title('Sequential: austin_cmap', fontsize=12, fontweight='bold')
    plt.colorbar(im1, ax=axes[0], label='Value (%)')
    
    # Diverging
    im2 = axes[1].imshow(data_div, cmap=austin_diverging, aspect='auto', vmin=-2, vmax=2)
    axes[1].set_title('Diverging: austin_diverging', fontsize=12, fontweight='bold')
    plt.colorbar(im2, ax=axes[1], label='Value')
    
    plt.tight_layout()
    plt.show()


# ============================================================
# SEABORN INTEGRATION
# ============================================================

def as_seaborn_palette(cmap=austin_cmap, n_colors=6):
    """
    Convert colormap to a list of colors for seaborn.
    Handles n_colors <= 0 and n_colors == 1 safely.
    """
    if n_colors <= 0:
        return []
    if n_colors == 1:
        return [mcolors.to_hex(cmap(0.5))]
    return [mcolors.to_hex(cmap(i / (n_colors - 1))) for i in range(n_colors)]


# ============================================================
# QUICK REFERENCE
# ============================================================

COLORMAP_GUIDE = """
AUSTIN COLORMAPS - Quick Reference
==================================

SEQUENTIAL (low → high):
  austin_cmap            Grey → Purple (default)
  austin_cmap_r          Purple → Grey (reversed)
  austin_cmap_extended   Grey → Purple → Dark purple (more range)

DIVERGING (negative → zero → positive):
  austin_diverging       Orange → White → Purple
  austin_diverging_teal  Teal → White → Purple
  austin_diverging_green Green → White → Purple

USAGE:
  # Direct use
  ax.imshow(data, cmap=austin_cmap)
  
  # Register for string access
  register_cmaps()
  ax.imshow(data, cmap='austin')
  
  # With seaborn
  sns.heatmap(data, cmap=austin_cmap)
  
  # Get single color from gradient
  color = get_color_at(0.75)
  
  # Get n colors for categorical
  colors = get_n_colors(5)
"""


if __name__ == '__main__':
    print(COLORMAP_GUIDE)
    show_colormaps()
