"""Tests for austin_rules — one test per storytelling rule the kit enforces."""

import io
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # no display needed

import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.patches import FancyArrowPatch

KIT = Path(__file__).resolve().parent.parent / 'austin_style_kit'
sys.path.insert(0, str(KIT))

from austin_annotations import PALETTE  # noqa: E402
from austin_rules import (  # noqa: E402
    StoryGraphRuleError,
    add_breakout,
    check_figure,
    connect_panels,
    gap_intervals,
    lint,
    plot_with_gaps,
)


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close('all')


def rules(fig):
    return [v.rule for v in check_figure(fig)]


def bar_chart():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(['north', 'south', 'east'], [10, 4, 7],
            color=[PALETTE['neutral'], PALETTE['primary'], PALETTE['neutral']])
    ax.set_xlim(0, 12)
    return fig, ax


# ============================================================
# Issue #1: no dual y axis
# ============================================================

def test_twin_axis_is_a_hard_error():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    ax.twinx().plot([1, 2, 3], [9, 4, 1])

    found = check_figure(fig)
    assert [v.rule for v in found] == ['dual-axis']
    assert found[0].severity == 'error'
    with pytest.raises(StoryGraphRuleError):
        lint(fig)


def test_secondary_axis_is_a_hard_error():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    ax.secondary_yaxis('right')

    assert 'dual-axis' in rules(fig)


def test_one_scale_passes():
    fig, ax = bar_chart()

    assert 'dual-axis' not in rules(fig)


# ============================================================
# Issue #2 item 1: labels must not touch tick labels
# ============================================================

def test_label_on_a_tick_label_is_flagged():
    fig, ax = bar_chart()
    fig.canvas.draw()

    tick = ax.yaxis.get_ticklabels()[0]
    box = tick.get_window_extent()
    x, y = ax.transData.inverted().transform((box.x0 + 1, box.y0 + box.height / 2))
    ax.text(x, y, tick.get_text())

    assert 'label-vs-tick' in rules(fig)


def test_label_inside_the_plot_passes():
    fig, ax = bar_chart()
    ax.text(6, 1, 'clear of the ticks', va='center')

    assert 'label-vs-tick' not in rules(fig)


# ============================================================
# Issue #2 item 3: labels must not sit on plot elements
# ============================================================

def test_label_on_a_line_is_flagged():
    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.arange(10)
    ax.plot(x, x * 2)
    ax.set_ylim(0, 30)
    ax.text(5, 10, 'sitting on the line')

    assert 'label-on-data' in rules(fig)


def test_label_with_clearance_passes():
    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.arange(10)
    ax.plot(x, x * 2)
    ax.set_ylim(0, 30)
    ax.text(1, 25, 'clear of the line')

    assert 'label-on-data' not in rules(fig)


def test_dark_label_inside_a_dark_bar_is_flagged():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar([0], [10], color=PALETTE['neutral'])
    ax.set_ylim(0, 12)
    ax.text(0, 5, '5', ha='center', va='center', color='#333333')

    assert 'label-on-data' in rules(fig)


def test_white_label_inside_a_stacked_segment_passes():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar([0], [10], color=PALETTE['primary'])
    ax.set_ylim(0, 12)
    ax.text(0, 5, '10', ha='center', va='center', color='white')

    assert 'label-on-data' not in rules(fig)


# ============================================================
# Issue #2 item 2: missing-data periods must be marked
# ============================================================

def test_unmarked_gap_is_flagged():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(np.arange(6), [1, 2, np.nan, np.nan, 5, 6])

    assert 'gap-unmarked' in rules(fig)


def test_plot_with_gaps_shades_the_gap():
    fig, ax = plt.subplots(figsize=(6, 4))
    x, y = np.arange(6), [1, 2, np.nan, np.nan, 5, 6]
    plot_with_gaps(ax, x, y, gap_label='no data')

    assert len(ax.patches) == 1              # the shaded band
    assert 'gap-unmarked' not in rules(fig)


def test_gap_intervals_bounds_the_run_by_its_neighbours():
    x = np.arange(6)
    y = [1, 2, np.nan, np.nan, 5, 6]

    assert gap_intervals(x, y) == [(1.0, 4.0)]


def test_gap_intervals_ignores_a_run_at_the_edge():
    assert gap_intervals(np.arange(4), [np.nan, 2, 3, np.nan]) == []


def test_datetime_axis_is_supported():
    import pandas as pd

    fig, ax = plt.subplots(figsize=(6, 4))
    plot_with_gaps(ax, pd.date_range('2020-01-01', periods=6),
                   [1, 2, np.nan, 4, 5, 6], gap_label='no data')

    assert check_figure(fig) == []


def test_categorical_axis_is_supported():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(['north', 'south'], [3, 5])

    assert check_figure(fig) == []


# ============================================================
# Issue #2 item 5: no label that repeats the title's number
# ============================================================

def test_label_repeating_a_title_number_is_flagged():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot([1, 2], [3, 4])
    ax.set_ylim(0, 10)
    ax.text(0, 1.05, 'Sales fell 23%', transform=ax.transAxes)
    ax.text(3, 1, '23%')

    assert 'title-repeats' in rules(fig)


def test_a_year_used_as_an_axis_label_passes():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot([1, 2], [3, 4])
    ax.set_ylim(0, 10)
    ax.text(0, 1.05, 'Deaths per 100 live births, 1990 vs 2023',
            transform=ax.transAxes)
    ax.text(1, 8, '1990')

    assert 'title-repeats' not in rules(fig)


# ============================================================
# Issue #2 item 4: connected narratives + breakout support
# ============================================================

def test_connect_panels_joins_two_panels():
    fig, (left, right) = plt.subplots(1, 2)
    left.plot([1, 2], [1, 4])
    right.plot([1, 2], [4, 1])
    connector = connect_panels(fig, left, right, text='who drove it')

    assert isinstance(connector, FancyArrowPatch)
    assert connector in fig.artists
    assert check_figure(fig) == []


def test_add_breakout_zooms_the_slice():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(np.arange(50), np.sin(np.arange(50)))
    inset = add_breakout(ax, xlim=(10, 20), ylim=(-0.5, 0.5), text='zoom')

    assert inset.get_xlim() == (10.0, 20.0)
    assert inset.get_ylim() == (-0.5, 0.5)
    assert inset in ax.child_axes


def test_add_breakout_rejects_an_empty_range():
    fig, ax = plt.subplots()

    with pytest.raises(ValueError):
        add_breakout(ax, xlim=(5, 5))


# ============================================================
# Reporting behaviour
# ============================================================

def test_lint_prints_warnings_without_raising():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(np.arange(6), [1, 2, np.nan, np.nan, 5, 6])
    out = io.StringIO()

    found = lint(fig, stream=out)

    assert any(v.rule == 'gap-unmarked' for v in found)
    assert 'gap-unmarked' in out.getvalue()


def test_a_finished_storytelling_chart_is_clean():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(['north', 'south', 'east'], [10, 4, 7],
            color=[PALETTE['neutral'], PALETTE['primary'], PALETTE['neutral']])
    ax.set_xlim(0, 12)
    ax.text(0, 1.08, 'South is the only region falling', transform=ax.transAxes,
            fontsize=14, fontweight='bold', color='#333333')
    ax.text(0, 1.03, 'Sales by region, 2024', transform=ax.transAxes,
            fontsize=11, color='#888888')
    ax.text(0.02, -0.08, 'Source: StoryGraph demo', transform=ax.transAxes,
            ha='left', fontsize=8, color='#888888')

    assert check_figure(fig) == []
