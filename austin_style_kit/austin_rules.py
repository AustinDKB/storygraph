"""
AUSTIN RULES: storytelling checks the kit enforces
==================================================

USAGE:
    from austin_rules import lint, check_figure, plot_with_gaps, connect_panels, add_breakout

    lint(fig)              # print violations; raise on a hard rule (dual y axis)
    check_figure(fig)      # -> [Violation], no output

RULES
-----
dual-axis        Two scales on one plot (twinx/twiny/secondary_yaxis). Hard rule:
                 use an index, small multiples, or two panels joined by
                 :func:`connect_panels`. Rejected, not warned.
label-vs-tick    An in-plot label collides with a tick label or a gridline.
label-on-data    An in-plot label sits on a line, bar, or marker.
gap-unmarked     A line runs through a missing-data period without a marked gap.
                 :func:`plot_with_gaps` shades it for you.
title-repeats    A label repeats a number the title already states.

The checks are geometric and therefore approximate: they judge what the
renderer actually draws, so they work for any chart type built with this kit.
"""

import re
import sys
from dataclasses import dataclass, field

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.patches import ConnectionPatch, FancyArrowPatch, Rectangle
from matplotlib.collections import PathCollection
from matplotlib.path import Path
from matplotlib.text import Annotation, Text
from matplotlib.transforms import Bbox

# Artists the helpers below add on purpose; they are background, not data.
HELPER_GID = 'storygraph:helper'

# A shaded gap is chart furniture, so give it the light purple tint.
GAP_COLOR = '#EDE7F3'

# The gap-shade band plot_with_gaps draws, distinct from other helper furniture.
GAP_GID = 'storygraph:gap'


class StoryGraphRuleError(ValueError):
    """Raised when a chart breaks a hard storytelling rule."""

    def __init__(self, violations):
        self.violations = list(violations)
        lines = '\n'.join(f'  [{v.rule}] {v.message}' for v in self.violations)
        super().__init__(f'StoryGraph rule violations:\n{lines}')


@dataclass
class Violation:
    rule: str
    message: str
    severity: str = 'warning'
    artist: object = field(default=None, repr=False)


# ============================================================
# PUBLIC API
# ============================================================

def check_figure(fig=None, pad=1.0):
    """Return every rule violation the figure shows. ``pad`` is text clearance in pixels."""
    fig = plt.gcf() if fig is None else fig
    if fig.canvas is None:
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        FigureCanvasAgg(fig)
    fig.canvas.draw()  # text extents need a renderer

    found = []
    for ax in list(fig.axes):
        found += _check_dual_axis(fig, ax)
        inside, above = _text_boxes(ax)
        found += _check_labels_vs_ticks(ax, inside)
        found += _check_labels_vs_data(ax, inside, pad)
        found += _check_gaps(ax)
        found += _check_title_repeats(above, inside)
    return _dedupe(found)


def lint(fig=None, strict=False, pad=1.0, stream=None):
    """Print every violation. Raise on a hard rule, or on any rule when ``strict``."""
    violated = check_figure(fig, pad=pad)
    out = sys.stdout if stream is None else stream
    for v in violated:
        print(f'storygraph [{v.rule}] {v.message}', file=out)
    hard = violated if strict else [v for v in violated if v.severity == 'error']
    if hard:
        raise StoryGraphRuleError(hard)
    return violated


# ============================================================
# RULE 1: no dual y axis (issue #1)
# ============================================================

def _check_dual_axis(fig, ax):
    """A twin or secondary scale on the same plot box."""
    found = []
    mine = tuple(np.round(ax.get_position().bounds, 6))
    for other in fig.axes:
        if other is ax:
            continue
        if tuple(np.round(other.get_position().bounds, 6)) == mine:
            found.append(Violation(
                'dual-axis',
                'two scales share one plot box — use an index, small multiples, '
                'or two panels joined by connect_panels()',
                severity='error', artist=other))
    for child in getattr(ax, 'child_axes', []):
        if type(child).__name__ == 'SecondaryAxis':
            found.append(Violation(
                'dual-axis',
                'secondary axis adds a second scale — use an index, small multiples, '
                'or two panels joined by connect_panels()',
                severity='error', artist=child))
    return found


# ============================================================
# RULE 2 and 3: labels clear of ticks, gridlines, and data
# ============================================================

def _text_box(text):
    patch = text.get_bbox_patch()
    if patch is not None:
        return patch.get_window_extent()
    if isinstance(text, Annotation):
        # Annotation.get_window_extent() covers the arrow too — measure the words.
        text.update_positions(text.figure.canvas.get_renderer())
        return Text.get_window_extent(text)
    return text.get_window_extent()


def _text_boxes(ax):
    """Split the axes' texts into (inside the plot area, the title band above it).

    A text anchored above the plot area is a title band; one anchored below is
    a source note. Neither is a label that can sit on data, and only the title
    band feeds the title-repeats check.
    """
    ax_box = ax.get_window_extent()
    inside, above = [], []
    for text in ax.texts:
        if not text.get_visible() or not text.get_text().strip():
            continue
        if text.get_alpha() == 0:
            continue
        anchor = text.get_transform().transform(text.get_position())
        box = _text_box(text)
        if ax_box.y0 <= anchor[1] <= ax_box.y1:
            inside.append((text, box))
        elif anchor[1] > ax_box.y1:
            above.append((text, box))
    return inside, above


def _check_labels_vs_ticks(ax, inside):
    found = []
    tick_boxes = [t.get_window_extent()
                  for axis in (ax.xaxis, ax.yaxis)
                  for t in axis.get_ticklabels()
                  if t.get_visible() and t.get_text().strip()]
    grid_y = [gl for gl in ax.yaxis.get_gridlines()
              if gl.get_visible() and len(gl.get_ydata())]
    grid_x = [gl for gl in ax.xaxis.get_gridlines()
              if gl.get_visible() and len(gl.get_xdata())]

    for text, box in inside:
        for tick in tick_boxes:
            if box.overlaps(tick):
                found.append(Violation(
                    'label-vs-tick',
                    f'label {text.get_text()!r} collides with an axis tick label',
                    artist=text))
        for line in grid_y:
            y = line.get_transform().transform((0, line.get_ydata()[0]))[1]
            if box.y0 <= y <= box.y1:
                found.append(Violation(
                    'label-vs-tick',
                    f'label {text.get_text()!r} sits on a horizontal gridline',
                    artist=text))
        for line in grid_x:
            x = line.get_transform().transform((line.get_xdata()[0], 0))[0]
            if box.x0 <= x <= box.x1:
                found.append(Violation(
                    'label-vs-tick',
                    f'label {text.get_text()!r} sits on a vertical gridline',
                    artist=text))
    return found


def _line_xy(ax, line):
    """Line data as numbers, converted the way the axes converts it."""
    x = np.asarray(ax.convert_xunits(line.get_xdata()), dtype=float)
    y = np.asarray(ax.convert_yunits(line.get_ydata()), dtype=float)
    return x, y


def _segments(ax, line):
    """Finite consecutive point pairs of a line, in display coordinates."""
    x, y = _line_xy(ax, line)
    points = line.get_transform().transform(np.column_stack([x, y]))
    for start, end in zip(points[:-1], points[1:]):
        if np.isfinite(start).all() and np.isfinite(end).all():
            yield start, end


def _is_guide(line):
    """A two-point hline/vline is a reference guide, not a data series."""
    x, y = (np.asarray(v) for v in line.get_data())
    return x.size == 2 and (x[0] == x[1] or y[0] == y[1])


def _draws_line(line):
    """True when a line actually draws its connecting segments."""
    return line.get_linestyle() not in ('None', 'none', '', ' ', None)


def _has_marker(line):
    return line.get_marker() not in ('None', 'none', '', ' ', None)


def _luminance(rgb):
    channels = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    r, g, b = channels
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contrast_ratio(one, other):
    high, low = sorted((_luminance(one), _luminance(other)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def _legible_on(text, patch):
    """A label inside a filled patch is fine while its contrast stays readable."""
    face = patch.get_facecolor()
    if face[3] == 0:
        return True
    background = tuple(face[i] * face[3] + (1 - face[3]) for i in range(3))  # over white
    return _contrast_ratio(to_rgb(text.get_color()), background) >= 3.0


def _marker_boxes(ax, coll):
    """Display-space boxes of each marker in a collection (scatter points)."""
    offsets = coll.get_offsets()
    if offsets is None or len(offsets) == 0:
        return []
    sizes = np.asarray(coll.get_sizes(), dtype=float)
    if sizes.size == 0:
        return []
    try:
        display = np.asarray(coll.get_offset_transform().transform(offsets), dtype=float)
    except ValueError:
        return []
    dpi = ax.figure.get_dpi()
    radii = np.sqrt(np.maximum(sizes, 0)) / 2.0 * dpi / 72.0
    radii = np.broadcast_to(radii, display.shape[:1])
    return [Bbox([[x - r, y - r], [x + r, y + r]])
            for (x, y), r in zip(display, radii)
            if np.isfinite(x) and np.isfinite(y)]


def _line_marker_boxes(ax, line):
    """Display-space boxes of a line's drawn markers."""
    if not _has_marker(line):
        return []
    size = line.get_markersize()
    if size <= 0:
        return []
    x, y = _line_xy(ax, line)
    points = line.get_transform().transform(np.column_stack([x, y]))
    radius = size / 2.0 * ax.figure.get_dpi() / 72.0
    return [Bbox([[px - radius, py - radius], [px + radius, py + radius]])
            for px, py in points if np.isfinite(px) and np.isfinite(py)]


def _check_labels_vs_data(ax, inside, pad):
    found = []
    bar_boxes = [(p, p.get_window_extent()) for p in ax.patches
                 if p.get_visible() and p.get_gid() != HELPER_GID]
    data_lines = [ln for ln in ax.lines
                  if ln.get_visible() and len(ln.get_xdata()) > 1
                  and ln.get_gid() != HELPER_GID and not _is_guide(ln)
                  and _draws_line(ln)]
    markers = [b for coll in ax.collections
               if isinstance(coll, PathCollection)
               and coll.get_visible() and coll.get_gid() != HELPER_GID
               for b in _marker_boxes(ax, coll)]
    markers += [b for ln in ax.lines
                if ln.get_visible() and ln.get_gid() != HELPER_GID
                for b in _line_marker_boxes(ax, ln)]

    for text, box in inside:
        box = box.padded(pad) if pad else box
        for patch, bar in bar_boxes:
            if box.overlaps(bar) and not _legible_on(text, patch):
                found.append(Violation(
                    'label-on-data',
                    f'label {text.get_text()!r} sits on a bar with too little contrast — '
                    f'move it out or give the text a bbox',
                    artist=text))
        for line in data_lines:
            for start, end in _segments(ax, line):
                if Path([start, end]).intersects_bbox(box, filled=False):
                    name = line.get_label()
                    owner = f'line {name!r}' if not name.startswith('_') else 'a line'
                    found.append(Violation(
                        'label-on-data',
                        f'label {text.get_text()!r} sits on {owner} — give it clearance',
                        artist=text))
                    break
        for marker in markers:
            if box.overlaps(marker):
                found.append(Violation(
                    'label-on-data',
                    f'label {text.get_text()!r} sits on a marker — give it clearance',
                    artist=text))
                break
    return found


# ============================================================
# RULE 4: missing-data periods must be marked (issue #2 item 2)
# ============================================================

def gap_intervals(x, y):
    """x-ranges of missing-data runs: last good point to the next good point."""
    x = np.asarray(x)
    good = np.isfinite(np.asarray(y, dtype=float))
    spans, i, n = [], 0, good.size
    while i < n:
        if good[i]:
            i += 1
            continue
        end = i
        while end < n and not good[end]:
            end += 1
        if i > 0 and end < n:  # a run at either edge has no line to break
            spans.append((x[i - 1], x[end]))
        i = end
    return spans


def _patch_x_span(patch, ax):
    box = patch.get_path().get_extents(patch.get_transform())
    box = box.transformed(ax.transData.inverted())
    return box.x0, box.x1


def _is_gap_shade(patch, ax):
    """A vertical span that marks a missing-data period (the kit band or a user axvspan)."""
    if patch.get_gid() == GAP_GID:
        return True
    if patch.get_gid() is not None:
        return False
    ax_box = ax.get_window_extent()
    box = patch.get_window_extent()
    return box.y0 <= ax_box.y0 + 1.0 and box.y1 >= ax_box.y1 - 1.0


def _check_gaps(ax):
    found = []
    formatter = ax.xaxis.get_major_formatter()
    patches = [p for p in ax.patches if p.get_visible() and _is_gap_shade(p, ax)]
    for line in ax.lines:
        if not line.get_visible():
            continue
        x, y = _line_xy(ax, line)
        if len(y) < 3:
            continue
        for left, right in gap_intervals(x, y):
            covered = any(
                x0 <= left + 1e-9 and x1 >= right - 1e-9
                for x0, x1 in (_patch_x_span(p, ax) for p in patches))
            if not covered:
                found.append(Violation(
                    'gap-unmarked',
                    f'a line runs from {formatter.format_data_short(left)} to '
                    f'{formatter.format_data_short(right)} over missing data — '
                    f'break it and shade the gap with plot_with_gaps()',
                    artist=line))
    return found


# ============================================================
# RULE 5: a label must not repeat what the title says (issue #2 item 5)
# ============================================================

NUMBER_RE = re.compile(r'\d{1,3}(?:[,_]\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?')


def numbers_in(text):
    """Every number in a string, thousands separators removed."""
    return {n.replace(',', '').replace('_', '') for n in NUMBER_RE.findall(text)}


def _is_year_label(text):
    """A label that is only a year acts as an axis, not as a repeated value."""
    return bool(re.fullmatch(r'\s*\d{4}\s*', text)) and 1800 <= int(text) <= 2200


def _check_title_repeats(above, inside):
    """Numbers in the title band must not be restated by a label in the plot."""
    title_numbers = set()
    for text, _ in above:
        title_numbers |= numbers_in(text.get_text())
    if not title_numbers:
        return []

    found, seen = [], set()
    for text, _ in inside:
        if _is_year_label(text.get_text()):
            continue
        for number in numbers_in(text.get_text()) & title_numbers:
            if number in seen:
                continue
            seen.add(number)
            found.append(Violation(
                'title-repeats',
                f'label {text.get_text()!r} repeats {number} from the title — '
                f'drop the label or keep the number in one place',
                artist=text))
    return found


def _dedupe(violations):
    seen, out = set(), []
    for v in violations:
        key = (v.rule, v.message)
        if key not in seen:
            seen.add(key)
            out.append(v)
    return out


# ============================================================
# HELPERS
# ============================================================

def plot_with_gaps(ax, x, y, gap_label=None, color=None, shade_color=GAP_COLOR,
                   zorder=0, **line_kwargs):
    """Plot a time series and mark its missing-data periods.

    Matplotlib already breaks a line at NaN; this shades each gap and, when
    ``gap_label`` is given, names it once at the top of the first gap.
    Returns the Line2D.
    """
    from austin_annotations import PALETTE

    color = color or line_kwargs.pop('color', None) or PALETTE['primary']
    y = np.asarray(y, dtype=float)
    line = ax.plot(x, y, color=color, **line_kwargs)[0]

    spans = gap_intervals(x, y)
    for x0, x1 in spans:
        band = ax.axvspan(x0, x1, color=shade_color, alpha=0.6, linewidth=0, zorder=zorder)
        band.set_gid(GAP_GID)
    if spans and gap_label:
        x0, x1 = spans[0]
        middle = np.mean(np.asarray(ax.convert_xunits([x0, x1]), dtype=float))
        top = np.nanmax(y)
        note = ax.text(middle, top, gap_label, fontsize=9, color='#666666',
                       ha='center', va='bottom', style='italic')
        note.set_gid(HELPER_GID)
    return line


def connect_panels(fig, ax_from, ax_to, text=None, color=None, arrow=True):
    """Join two panels of a sequential story (total -> breakdown) with a connector.

    Draws a figure-level arrow from the right edge of ``ax_from`` to the left
    edge of ``ax_to``, with an optional label at the midpoint.
    """
    from austin_annotations import PALETTE

    color = color or PALETTE['primary']
    left, right = ax_from.get_position(), ax_to.get_position()
    start = (left.x1, (left.y0 + left.y1) / 2)
    end = (right.x0, (right.y0 + right.y1) / 2)
    style = dict(transform=fig.transFigure, color=color, linewidth=2,
                 shrinkA=2, shrinkB=2, zorder=1)
    if arrow:
        connector = FancyArrowPatch(start, end, arrowstyle='-|>',
                                    mutation_scale=18, **style)
    else:
        connector = FancyArrowPatch(start, end, arrowstyle='-', **style)
    connector.set_gid(HELPER_GID)
    fig.add_artist(connector)

    if text:
        label = fig.text((start[0] + end[0]) / 2, (start[1] + end[1]) / 2, text,
                         ha='center', va='bottom', fontsize=9, color=color,
                         transform=fig.transFigure)
        label.set_gid(HELPER_GID)
    return connector


def add_breakout(ax, xlim, ylim=None, bounds=(0.62, 0.6, 0.36, 0.38),
                 color=None, text=None):
    """Add a zoom panel (breakout) for a slice of the data.

    Outlines ``xlim``/``ylim`` on the parent axes, creates an inset axes zoomed
    to that slice, and links the two with connector lines. Plot the slice again
    into the returned inset — it carries the same limits.
    """
    from austin_annotations import PALETTE

    color = color or PALETTE['primary']
    x0, x1 = sorted(float(v) for v in xlim)
    if x1 <= x0:
        raise ValueError('add_breakout needs xlim=(low, high) with high > low')
    y0, y1 = ax.get_ylim() if ylim is None else sorted(float(v) for v in ylim)

    frame = Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, edgecolor=color,
                      linewidth=1, linestyle='--', zorder=3)
    frame.set_gid(HELPER_GID)
    ax.add_patch(frame)

    inset = ax.inset_axes(bounds)
    inset.set_xlim(x0, x1)
    inset.set_ylim(y0, y1)
    inset.tick_params(left=False, bottom=False, labelsize=8)

    for corner, anchor in ((0.0, 0.0), (1.0, 1.0)):
        connector = ConnectionPatch(
            xyA=(x0 if corner == 0.0 else x1, y1), coordsA=ax.transData,
            xyB=(anchor, 1.0), coordsB=inset.transAxes,
            color=color, linewidth=1, alpha=0.6)
        connector.set_gid(HELPER_GID)
        ax.figure.add_artist(connector)

    if text:
        label = inset.text(0.04, 0.96, text, transform=inset.transAxes,
                           ha='left', va='top', fontsize=8, color=color,
                           style='italic')
        label.set_gid(HELPER_GID)
    return inset
