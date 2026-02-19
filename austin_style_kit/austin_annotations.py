"""
AUSTIN ANNOTATIONS: Consistent Annotation Styles for Storytelling
==================================================================

High Contrast colorblind-safe palette built around primary: #5C2593

USAGE:
    from austin_annotations import annotate, PRESETS, PALETTE
    
    # Use a preset
    annotate(ax, 'Key insight!', xy=(3, 5), xytext=(5, 7), preset='callout')
    
    # Access colors directly
    ax.plot(x, y, color=PALETTE['primary'])

"""

import matplotlib.pyplot as plt


# ============================================================
# AUSTIN PALETTE - High Contrast, Colorblind Safe
# ============================================================

PALETTE = {
    'primary': '#5C2593',      # Deep purple - main data, key callouts
    'secondary': '#0A5E73',    # Dark teal - secondary data series
    'negative': '#BF5B04',     # Deep orange (NOT red) - warnings, decreases
    'positive': '#1A936F',     # Sea green - wins, increases, good news
    'neutral': '#4A4A4A',      # Dark gray - context, de-emphasized
    'accent': '#E8B72C',       # Bright gold - highlights, special emphasis
}

# Color cycle for automatic assignment (primary first)
COLOR_CYCLE = [
    PALETTE['primary'],
    PALETTE['secondary'],
    PALETTE['positive'],
    PALETTE['accent'],
    PALETTE['negative'],
    PALETTE['neutral'],
]


# ============================================================
# ANNOTATION PRESETS
# ============================================================

PRESETS = {
    # Bold callout - draws attention to key data points
    'callout': {
        'fontsize': 11,
        'fontweight': 'bold',
        'color': PALETTE['primary'],
        'arrowprops': dict(
            arrowstyle='->',
            color=PALETTE['primary'],
            lw=2,
            connectionstyle='arc3,rad=0.2',
            shrinkB=5,
        ),
    },
    
    # Callout with filled box - maximum emphasis
    'callout_box': {
        'fontsize': 11,
        'fontweight': 'bold',
        'color': 'white',
        'arrowprops': dict(
            arrowstyle='-|>',
            color=PALETTE['primary'],
            lw=2,
            shrinkB=5,
        ),
        'bbox': dict(
            boxstyle='round,pad=0.4',
            facecolor=PALETTE['primary'],
            edgecolor='none',
        ),
    },
    
    # Subtle note - secondary information
    'subtle': {
        'fontsize': 9,
        'color': PALETTE['neutral'],
        'style': 'italic',
        'arrowprops': dict(
            arrowstyle='->',
            color='#888888',
            lw=1,
            connectionstyle='arc3,rad=0.15',
            shrinkB=3,
        ),
    },
    
    # Simple label - just identifies a point
    'label': {
        'fontsize': 10,
        'fontweight': 'bold',
        'color': '#333333',
        'arrowprops': dict(
            arrowstyle='-',
            color='#333333',
            lw=1,
            shrinkB=3,
        ),
    },
    
    # Highlight with background - important callouts
    'highlight': {
        'fontsize': 12,
        'fontweight': 'bold',
        'color': PALETTE['primary'],
        'arrowprops': dict(
            arrowstyle='->',
            color=PALETTE['primary'],
            lw=2,
            shrinkB=5,
        ),
        'bbox': dict(
            boxstyle='round,pad=0.3',
            facecolor='#EDE7F3',  # Light purple tint
            edgecolor=PALETTE['primary'],
            linewidth=1.5,
        ),
    },
    
    # Trend indicator - shows direction/change
    'trend': {
        'fontsize': 10,
        'fontweight': 'bold',
        'color': PALETTE['secondary'],
        'arrowprops': dict(
            arrowstyle='<->',
            color=PALETTE['secondary'],
            lw=2,
            connectionstyle='arc3,rad=0',
        ),
    },
    
    # Positive callout - good news, increases, wins
    'positive': {
        'fontsize': 11,
        'fontweight': 'bold',
        'color': PALETTE['positive'],
        'arrowprops': dict(
            arrowstyle='->',
            color=PALETTE['positive'],
            lw=2,
            shrinkB=5,
        ),
    },
    
    # Negative callout - bad news, decreases, concerns
    # Uses ORANGE not red for colorblind safety
    'negative': {
        'fontsize': 11,
        'fontweight': 'bold',
        'color': PALETTE['negative'],
        'arrowprops': dict(
            arrowstyle='->',
            color=PALETTE['negative'],
            lw=2,
            shrinkB=5,
        ),
    },
    
    # Neutral info - factual, no emotional valence
    'neutral': {
        'fontsize': 10,
        'color': PALETTE['neutral'],
        'arrowprops': dict(
            arrowstyle='->',
            color='#777777',
            lw=1.5,
            shrinkB=4,
        ),
    },
    
    # Accent callout - special highlights
    'accent': {
        'fontsize': 11,
        'fontweight': 'bold',
        'color': PALETTE['accent'],
        'arrowprops': dict(
            arrowstyle='->',
            color=PALETTE['accent'],
            lw=2,
            shrinkB=5,
        ),
    },
}


# ============================================================
# PRESENTATION PRESETS (larger for slides)
# ============================================================

PRESETS_PRESENTATION = {
    'callout': {
        'fontsize': 14,
        'fontweight': 'bold',
        'color': PALETTE['primary'],
        'arrowprops': dict(
            arrowstyle='->',
            color=PALETTE['primary'],
            lw=3,
            connectionstyle='arc3,rad=0.2',
            shrinkB=8,
        ),
    },
    
    'callout_box': {
        'fontsize': 14,
        'fontweight': 'bold',
        'color': 'white',
        'arrowprops': dict(
            arrowstyle='-|>',
            color=PALETTE['primary'],
            lw=3,
            shrinkB=8,
        ),
        'bbox': dict(
            boxstyle='round,pad=0.5',
            facecolor=PALETTE['primary'],
            edgecolor='none',
        ),
    },
    
    'subtle': {
        'fontsize': 12,
        'color': PALETTE['neutral'],
        'style': 'italic',
        'arrowprops': dict(
            arrowstyle='->',
            color='#888888',
            lw=1.5,
            connectionstyle='arc3,rad=0.15',
            shrinkB=5,
        ),
    },
    
    'label': {
        'fontsize': 13,
        'fontweight': 'bold',
        'color': '#333333',
        'arrowprops': dict(
            arrowstyle='-',
            color='#333333',
            lw=1.5,
            shrinkB=5,
        ),
    },
    
    'highlight': {
        'fontsize': 16,
        'fontweight': 'bold',
        'color': PALETTE['primary'],
        'arrowprops': dict(
            arrowstyle='->',
            color=PALETTE['primary'],
            lw=3,
            shrinkB=8,
        ),
        'bbox': dict(
            boxstyle='round,pad=0.4',
            facecolor='#EDE7F3',
            edgecolor=PALETTE['primary'],
            linewidth=2,
        ),
    },
    
    'trend': {
        'fontsize': 13,
        'fontweight': 'bold',
        'color': PALETTE['secondary'],
        'arrowprops': dict(
            arrowstyle='<->',
            color=PALETTE['secondary'],
            lw=3,
            connectionstyle='arc3,rad=0',
        ),
    },
    
    'positive': {
        'fontsize': 14,
        'fontweight': 'bold',
        'color': PALETTE['positive'],
        'arrowprops': dict(
            arrowstyle='->',
            color=PALETTE['positive'],
            lw=3,
            shrinkB=8,
        ),
    },
    
    'negative': {
        'fontsize': 14,
        'fontweight': 'bold',
        'color': PALETTE['negative'],
        'arrowprops': dict(
            arrowstyle='->',
            color=PALETTE['negative'],
            lw=3,
            shrinkB=8,
        ),
    },
    
    'neutral': {
        'fontsize': 13,
        'color': PALETTE['neutral'],
        'arrowprops': dict(
            arrowstyle='->',
            color='#777777',
            lw=2,
            shrinkB=6,
        ),
    },
    
    'accent': {
        'fontsize': 14,
        'fontweight': 'bold',
        'color': PALETTE['accent'],
        'arrowprops': dict(
            arrowstyle='->',
            color=PALETTE['accent'],
            lw=3,
            shrinkB=8,
        ),
    },
}


# ============================================================
# HELPER FUNCTION
# ============================================================

def annotate(ax, text, xy, xytext, preset='callout', presentation=False, **kwargs):
    """
    Add annotation with consistent styling.
    
    Parameters
    ----------
    ax : matplotlib Axes
        The axes to annotate on
    text : str
        Annotation text
    xy : tuple
        Point to annotate (x, y)
    xytext : tuple
        Text position (x, y)
    preset : str
        One of: 'callout', 'callout_box', 'subtle', 'label', 
                'highlight', 'trend', 'positive', 'negative', 'neutral', 'accent'
    presentation : bool
        If True, use larger presentation-sized presets
    **kwargs : dict
        Override any preset parameters
    
    Returns
    -------
    annotation : matplotlib.text.Annotation
    """
    
    presets = PRESETS_PRESENTATION if presentation else PRESETS
    
    if preset not in presets:
        raise ValueError(f"Unknown preset '{preset}'. Choose from: {list(presets.keys())}")
    
    # Deep copy to avoid modifying original
    import copy
    style = copy.deepcopy(presets[preset])
    
    # Handle nested dicts (arrowprops, bbox)
    if 'arrowprops' in kwargs:
        style['arrowprops'] = {**style.get('arrowprops', {}), **kwargs.pop('arrowprops')}
    if 'bbox' in kwargs:
        style['bbox'] = {**style.get('bbox', {}), **kwargs.pop('bbox')}
    
    style.update(kwargs)
    
    return ax.annotate(text, xy=xy, xytext=xytext, **style)


# ============================================================
# QUICK TEXT HELPERS
# ============================================================

def add_title_annotation(ax, text, loc='upper left', **kwargs):
    """Add a title-style annotation in corner of plot."""
    locs = {
        'upper left': (0.02, 0.98, 'left', 'top'),
        'upper right': (0.98, 0.98, 'right', 'top'),
        'lower left': (0.02, 0.02, 'left', 'bottom'),
        'lower right': (0.98, 0.02, 'right', 'bottom'),
    }
    x, y, ha, va = locs.get(loc, locs['upper left'])
    
    defaults = dict(
        fontsize=10, fontweight='bold', color='#333333',
        transform=ax.transAxes, ha=ha, va=va,
    )
    defaults.update(kwargs)
    return ax.text(x, y, text, **defaults)


def add_source_note(ax, text, **kwargs):
    """Add a source/footnote at bottom of chart."""
    defaults = dict(
        fontsize=8, color='#888888', style='italic',
        transform=ax.transAxes, ha='left', va='bottom',
    )
    defaults.update(kwargs)
    return ax.text(0.02, -0.08, text, **defaults)


# ============================================================
# PALETTE HELPERS
# ============================================================

def get_color(name):
    """Get a color from the palette by name."""
    if name not in PALETTE:
        raise ValueError(f"Unknown color '{name}'. Choose from: {list(PALETTE.keys())}")
    return PALETTE[name]


def show_palette():
    """Display the palette visually."""
    fig, ax = plt.subplots(figsize=(12, 2))
    for i, (name, color) in enumerate(PALETTE.items()):
        ax.add_patch(plt.Rectangle((i, 0), 0.9, 1, facecolor=color))
        ax.text(i + 0.45, -0.25, f'{name}\n{color}', ha='center', fontsize=9)
    ax.set_xlim(-0.1, len(PALETTE))
    ax.set_ylim(-0.6, 1.1)
    ax.set_title('Austin Palette - High Contrast (Colorblind Safe)', fontweight='bold')
    ax.axis('off')
    plt.tight_layout()
    plt.show()


def show_presets():
    """Display all available presets visually."""
    import numpy as np
    fig, axes = plt.subplots(2, 5, figsize=(16, 6))
    fig.suptitle('Available Annotation Presets', fontsize=14, fontweight='bold')
    x = np.linspace(0, 10, 50)
    y = np.sin(x) * 2 + 5
    preset_names = list(PRESETS.keys())
    for ax, name in zip(axes.flat, preset_names):
        ax.plot(x, y, color=PALETTE['primary'], linewidth=2.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_ylim(2, 9)
        ax.set_title(f"'{name}'", fontsize=11)
        ax.set_xticks([])
        ax.set_yticks([])
        annotate(ax, f'{name}', xy=(3, y[15]), xytext=(6, 7.5), preset=name)
    for ax in axes.flat[len(preset_names):]:
        ax.axis('off')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    show_palette()
    show_presets()
