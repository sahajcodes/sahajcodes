#!/usr/bin/env python3
"""Render a GitHub-style contribution heatmap SVG from data/contributions.json.

Input : <project root>/data/contributions.json   (created by fetch_contributions.py)
Output: <project root>/data/contrib-heatmap.svg

Usage (Windows PowerShell):
    python scripts/render_heatmap_svg.py                      # animated
    $env:STATIC="1"; python scripts/render_heatmap_svg.py     # static
    Remove-Item Env:STATIC                                    # back to animated
"""

from __future__ import annotations

import json
import math
import os
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Optional
from xml.sax.saxutils import escape

# --------------------------------------------------------------------------
# Paths (resolved relative to this script, not the terminal's current folder)
# --------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
INPUT_PATH = PROJECT_ROOT / "data" / "contributions.json"
OUTPUT_PATH = PROJECT_ROOT / "data" / "contrib-heatmap.svg"

DEFAULT_USERNAME = "sahajcodes"

# --------------------------------------------------------------------------
# Colors
# --------------------------------------------------------------------------
PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0",
]

BG = "#0d1117"
BORDER = "#30363d"
TEXT = "#e6edf3"
MUTED = "#8b949e"

# --------------------------------------------------------------------------
# Layout (all values are whole pixels so coordinates stay clean)
# --------------------------------------------------------------------------
CELL_SIZE = 11
CELL_GAP = 3
PITCH = CELL_SIZE + CELL_GAP          # distance from one cell to the next
CELL_RADIUS = 2
CARD_RADIUS = 12

PAD_X = 28
LABEL_COLUMN_WIDTH = 34               # room for Mon / Wed / Fri labels
GRID_X = PAD_X + LABEL_COLUMN_WIDTH
GRID_Y = 110
MIN_WIDTH = 760
HEIGHT = 352

TITLE_Y = 42
SUBTITLE_Y = 63
MONTH_LABEL_Y = GRID_Y - 8
SEPARATOR_Y = 250
STAT_LABEL_Y = 282
STAT_VALUE_Y = 308
STAT_SUB_Y = 328

MIN_LABEL_GAP_COLS = 3                # minimum columns between month labels

# --------------------------------------------------------------------------
# Animation
# --------------------------------------------------------------------------
ANIM_START_DELAY = 0.20               # seconds before the first column appears
ANIM_COLUMN_STEP = 0.012              # extra delay per week-column
ANIM_DURATION = 0.45                  # seconds per column

MONTH_ABBR = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]
EN_DASH = "\u2013"


class HeatmapError(Exception):
    """Raised for any problem reading the data or building the heatmap."""


@dataclass
class Cell:
    """One drawn calendar day."""

    day: date
    count: int
    level: int
    col: int      # week column, 0 = oldest
    row: int      # 0 = Sunday ... 6 = Saturday


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------
def is_static_mode() -> bool:
    """True when the STATIC environment variable is set to a truthy value."""
    return os.environ.get("STATIC", "").strip().lower() in {"1", "true", "yes", "on"}


def is_plain_int(value: Any) -> bool:
    """True for real integers (bool is excluded, since bool is an int subclass)."""
    return isinstance(value, int) and not isinstance(value, bool)


def parse_iso(value: Any) -> Optional[date]:
    """Parse 'YYYY-MM-DD' into a date, or return None if it is not valid."""
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def fmt_date(day: date) -> str:
    """Format like 'Mar 14, 2026' (no locale or platform-specific strftime codes)."""
    return f"{MONTH_ABBR[day.month - 1]} {day.day}, {day.year}"


def fmt_short(day: date) -> str:
    """Format like 'Mar 14'."""
    return f"{MONTH_ABBR[day.month - 1]} {day.day}"


def fmt_range(start: date, end: date) -> str:
    """Format a date range compactly."""
    if start == end:
        return fmt_date(end)
    if start.year == end.year:
        return f"{fmt_short(start)} {EN_DASH} {fmt_date(end)}"
    return f"{fmt_date(start)} {EN_DASH} {fmt_date(end)}"


def plural(count: int, word: str) -> str:
    """'1 day' / '3 days' with thousands separators."""
    return f"{count:,} {word}" + ("" if count == 1 else "s")


# --------------------------------------------------------------------------
# Reading and validating the JSON
# --------------------------------------------------------------------------
def load_report(path: Path) -> dict[str, Any]:
    """Read contributions.json and make sure it is a JSON object."""
    if not path.exists():
        raise HeatmapError(
            f"Input file not found: {path}\n"
            "Run this first: python scripts/fetch_contributions.py"
        )
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as error:
        raise HeatmapError(f"Could not read {path}: {error}")

    if not text.strip():
        raise HeatmapError(f"{path} is empty. Re-run fetch_contributions.py.")

    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise HeatmapError(
            f"{path} is not valid JSON (line {error.lineno}, column {error.colno}: "
            f"{error.msg}). Re-run fetch_contributions.py."
        )

    if not isinstance(data, dict):
        raise HeatmapError("Unexpected JSON format: the top level must be an object.")
    return data


def extract_days(data: dict[str, Any]) -> list[tuple[date, int]]:
    """Validate data['days'] and return sorted (date, count) pairs."""
    raw_days = data.get("days")
    if not isinstance(raw_days, list) or not raw_days:
        raise HeatmapError(
            "The JSON has no 'days' list (or it is empty). "
            "Re-run fetch_contributions.py."
        )

    seen: dict[date, int] = {}
    for index, item in enumerate(raw_days):
        if not isinstance(item, dict):
            raise HeatmapError(f"days[{index}] is not an object.")
        day = parse_iso(item.get("date"))
        if day is None:
            raise HeatmapError(f"days[{index}] has an invalid date: {item.get('date')!r}")
        count = item.get("count")
        if not is_plain_int(count) or count < 0:
            raise HeatmapError(
                f"days[{index}] ({item.get('date')}) has an invalid count: {count!r}"
            )
        if day in seen:
            raise HeatmapError(f"Duplicate date in the JSON: {day.isoformat()}")
        seen[day] = count

    return [(day, seen[day]) for day in sorted(seen)]


# --------------------------------------------------------------------------
# Levels and layout
# --------------------------------------------------------------------------
def compute_thresholds(counts: list[int]) -> list[int]:
    """Return 4 upper bounds that split nonzero counts into levels 1-5.

    Logic: sort every nonzero daily count and cut the list into five
    equal-sized groups (quantiles at 20%, 40%, 60%, 80%).
      - count <= cut[0]  -> level 1
      - count <= cut[1]  -> level 2
      - count <= cut[2]  -> level 3
      - count <= cut[3]  -> level 4
      - anything higher  -> level 5
    Using quantiles of your own data means a few huge days cannot make
    every ordinary day look empty. If there are no contributions, there
    are no thresholds (every day is level 0).
    """
    nonzero = sorted(count for count in counts if count > 0)
    if not nonzero:
        return []
    total = len(nonzero)
    cuts = []
    for step in range(1, 5):
        index = max(0, math.ceil(total * step / 5) - 1)
        cuts.append(nonzero[index])
    return cuts


def level_for(count: int, cuts: list[int]) -> int:
    """Map a daily count to a palette level from 0 to 5."""
    if count <= 0:
        return 0
    for position, cut in enumerate(cuts):
        if count <= cut:
            return position + 1
    return 5


def build_cells(days: list[tuple[date, int]]) -> tuple[list[Cell], int, list[int]]:
    """Place every day into its real week column and weekday row."""
    first_day = days[0][0]

    # Calendar weeks start on Sunday. date.weekday(): Monday=0 ... Sunday=6,
    # so (weekday + 1) % 7 gives Sunday=0 ... Saturday=6.
    grid_start = first_day - timedelta(days=(first_day.weekday() + 1) % 7)

    cuts = compute_thresholds([count for _, count in days])

    cells: list[Cell] = []
    for day, count in days:
        col, row = divmod((day - grid_start).days, 7)
        # Safety check: the computed row must equal the real weekday row.
        if row != (day.weekday() + 1) % 7:
            raise HeatmapError(f"Internal weekday mismatch for {day.isoformat()}.")
        cells.append(Cell(day=day, count=count, level=level_for(count, cuts), col=col, row=row))

    weeks = max(cell.col for cell in cells) + 1
    return cells, weeks, cuts


def report_gaps(days: list[tuple[date, int]]) -> int:
    """Return how many calendar dates are missing between the first and last day."""
    expected = (days[-1][0] - days[0][0]).days + 1
    return expected - len(days)


def compute_month_labels(cells: list[Cell]) -> list[tuple[int, str]]:
    """Choose (column, month name) labels without overlap."""
    first_day_in_col: dict[int, date] = {}
    for cell in cells:
        first_day_in_col.setdefault(cell.col, cell.day)

    labels: list[tuple[int, str]] = []
    last_month: Optional[tuple[int, int]] = None
    for col in sorted(first_day_in_col):
        day = first_day_in_col[col]
        month_key = (day.year, day.month)
        if month_key != last_month:
            labels.append((col, MONTH_ABBR[day.month - 1]))
            last_month = month_key

    # A tiny partial first month would collide with the next label: drop it.
    if len(labels) > 1 and labels[1][0] - labels[0][0] < MIN_LABEL_GAP_COLS:
        labels.pop(0)

    kept: list[tuple[int, str]] = []
    for col, name in labels:
        if not kept or col - kept[-1][0] >= MIN_LABEL_GAP_COLS:
            kept.append((col, name))
    return kept


# --------------------------------------------------------------------------
# Statistics (read from the JSON; derived from real days only as a fallback)
# --------------------------------------------------------------------------
def compute_total(data: dict[str, Any], cells: list[Cell]) -> int:
    """Total contributions, preferring the JSON value and warning on mismatch."""
    computed = sum(cell.count for cell in cells)
    raw_total = data.get("total_contributions")
    if is_plain_int(raw_total) and raw_total >= 0:
        if raw_total != computed:
            print(
                f"[WARN] JSON total ({raw_total}) differs from the sum of days "
                f"({computed}). Using the JSON value.",
                file=sys.stderr,
            )
        return raw_total
    return computed


def describe_streak(streak: Any, empty_text: str) -> tuple[str, str]:
    """Return (value, sub-text) for a streak entry from the JSON."""
    if not isinstance(streak, dict):
        return "N/A", "Not available in JSON"
    length = streak.get("length")
    if not is_plain_int(length) or length < 0:
        return "N/A", "Not available in JSON"
    if length == 0:
        return "0 days", empty_text
    start = parse_iso(streak.get("start"))
    end = parse_iso(streak.get("end"))
    sub = fmt_range(start, end) if start and end else ""
    return plural(length, "day"), sub


def describe_best_day(data: dict[str, Any], cells: list[Cell]) -> tuple[str, str]:
    """Return (value, sub-text) for the best contribution day."""
    best: Optional[tuple[date, int]] = None

    raw = data.get("best_day")
    if isinstance(raw, dict):
        best_date = parse_iso(raw.get("date"))
        best_count = raw.get("count")
        if best_date is not None and is_plain_int(best_count) and best_count > 0:
            best = (best_date, best_count)

    if best is None:
        # Fallback: derive from the real drawn days (earliest day wins ties).
        top: Optional[Cell] = None
        for cell in cells:
            if cell.count > 0 and (top is None or cell.count > top.count):
                top = cell
        if top is not None:
            best = (top.day, top.count)

    if best is None:
        return "None yet", "No contributions in range"
    best_date, best_count = best
    return f"{best_count:,}", f"on {fmt_date(best_date)}"


def build_stats(data: dict[str, Any], cells: list[Cell], total: int) -> list[tuple[str, str, str]]:
    """Return four (label, value, sub-text) blocks for the footer."""
    current_value, current_sub = describe_streak(data.get("current_streak"), "No active streak")
    longest_value, longest_sub = describe_streak(data.get("longest_streak"), "No streak yet")
    best_value, best_sub = describe_best_day(data, cells)
    return [
        ("TOTAL CONTRIBUTIONS", f"{total:,}", f"across {plural(len(cells), 'day')}"),
        ("CURRENT STREAK", current_value, current_sub),
        ("LONGEST STREAK", longest_value, longest_sub),
        ("BEST DAY", best_value, best_sub),
    ]


# --------------------------------------------------------------------------
# SVG rendering
# --------------------------------------------------------------------------
def build_css(animated: bool) -> str:
    """Build the <style> contents using plain strings (no f-string braces)."""
    rules = [
        'text { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }',
        ".title { font-size: 18px; font-weight: 600; fill: " + TEXT + "; }",
        ".subtitle { font-size: 12px; fill: " + MUTED + "; }",
        ".axis { font-size: 10px; fill: " + MUTED + "; }",
        ".legend { font-size: 11px; fill: " + MUTED + "; }",
        ".stat-label { font-size: 11px; font-weight: 600; letter-spacing: 0.8px; "
        "fill: " + MUTED + "; }",
        ".stat-value { font-size: 18px; font-weight: 700; fill: " + TEXT + "; }",
        ".stat-sub { font-size: 12px; fill: " + MUTED + "; }",
    ]
    if animated:
        # Cells are visible by default; 'backwards' fill hides them only during
        # their delay, so nothing stays invisible if animation is unsupported.
        rules.append(
            ".col { animation: slideIn " + f"{ANIM_DURATION}s" + " ease-out backwards; }"
        )
        rules.append(
            "@keyframes slideIn { "
            "from { opacity: 0; transform: translateY(-6px); } "
            "to { opacity: 1; transform: translateY(0); } }"
        )
        rules.append(
            "@media (prefers-reduced-motion: reduce) { .col { animation: none; } }"
        )
    return "\n    ".join(rules)


def render_svg(
    data: dict[str, Any],
    cells: list[Cell],
    weeks: int,
    total: int,
    stats: list[tuple[str, str, str]],
    animated: bool,
) -> str:
    """Assemble the complete SVG document."""
    raw_username = data.get("username")
    username = raw_username if isinstance(raw_username, str) and raw_username else DEFAULT_USERNAME

    grid_width = weeks * PITCH - CELL_GAP
    width = max(MIN_WIDTH, GRID_X + grid_width + PAD_X)
    right_edge = width - PAD_X
    grid_bottom = GRID_Y + 7 * PITCH - CELL_GAP

    first_day = min(cell.day for cell in cells)
    last_day = max(cell.day for cell in cells)
    subtitle = (
        f"{plural(total, 'contribution')} from {fmt_date(first_day)} to {fmt_date(last_day)}"
    )
    aria = f"{username} contribution heatmap: {subtitle}"

    svg: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{HEIGHT}" '
        f'viewBox="0 0 {width} {HEIGHT}" role="img" '
        f'aria-label="{escape(aria, {chr(34): "&quot;"})}">',
        f"  <title>{escape(username)} contribution heatmap</title>",
        f"  <desc>{escape(subtitle)}</desc>",
        "  <style>",
        "    " + build_css(animated),
        "  </style>",
        "",
        "  <!-- Card -->",
        f'  <rect x="0.5" y="0.5" width="{width - 1}" height="{HEIGHT - 1}" '
        f'rx="{CARD_RADIUS}" ry="{CARD_RADIUS}" fill="{BG}" stroke="{BORDER}" stroke-width="1"/>',
        f'  <text class="title" x="{PAD_X}" y="{TITLE_Y}">'
        f"{escape(username)} {EN_DASH} contribution activity</text>",
        f'  <text class="subtitle" x="{PAD_X}" y="{SUBTITLE_Y}">{escape(subtitle)}</text>',
        "",
        "  <!-- Month labels -->",
    ]

    for col, name in compute_month_labels(cells):
        x = GRID_X + col * PITCH
        svg.append(f'  <text class="axis" x="{x}" y="{MONTH_LABEL_Y}">{name}</text>')

    svg.append("")
    svg.append("  <!-- Weekday labels -->")
    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        y = GRID_Y + row * PITCH + 9
        svg.append(f'  <text class="axis" x="{PAD_X}" y="{y}">{name}</text>')

    svg.append("")
    svg.append("  <!-- Contribution cells (one group per week column) -->")
    columns: dict[int, list[Cell]] = {}
    for cell in cells:
        columns.setdefault(cell.col, []).append(cell)

    for col in sorted(columns):
        if animated:
            delay = ANIM_START_DELAY + col * ANIM_COLUMN_STEP
            svg.append(f'  <g class="col" style="animation-delay: {delay:.3f}s">')
        else:
            svg.append("  <g>")
        x = GRID_X + col * PITCH
        for cell in sorted(columns[col], key=lambda item: item.row):
            y = GRID_Y + cell.row * PITCH
            svg.append(
                f'    <rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
                f'rx="{CELL_RADIUS}" ry="{CELL_RADIUS}" fill="{PALETTE[cell.level]}"/>'
            )
        svg.append("  </g>")

    # Legend: Less [swatches] More, right-aligned under the grid.
    swatch_total_width = len(PALETTE) * PITCH - CELL_GAP
    swatches_x = right_edge - 36 - swatch_total_width
    legend_y = grid_bottom + 14
    svg.append("")
    svg.append("  <!-- Legend -->")
    svg.append(
        f'  <text class="legend" x="{swatches_x - 6}" y="{legend_y + 9}" '
        f'text-anchor="end">Less</text>'
    )
    for position, color in enumerate(PALETTE):
        x = swatches_x + position * PITCH
        svg.append(
            f'  <rect x="{x}" y="{legend_y}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
            f'rx="{CELL_RADIUS}" ry="{CELL_RADIUS}" fill="{color}"/>'
        )
    svg.append(
        f'  <text class="legend" x="{right_edge}" y="{legend_y + 9}" '
        f'text-anchor="end">More</text>'
    )

    # Statistics footer.
    svg.append("")
    svg.append("  <!-- Statistics -->")
    svg.append(
        f'  <line x1="{PAD_X}" y1="{SEPARATOR_Y}" x2="{right_edge}" y2="{SEPARATOR_Y}" '
        f'stroke="{BORDER}" stroke-width="1"/>'
    )
    block_width = (width - 2 * PAD_X) // len(stats)
    for index, (label, value, sub) in enumerate(stats):
        block_x = PAD_X + index * block_width
        text_x = block_x if index == 0 else block_x + 18
        if index > 0:
            svg.append(
                f'  <line x1="{block_x}" y1="{SEPARATOR_Y + 16}" x2="{block_x}" '
                f'y2="{HEIGHT - 24}" stroke="{BORDER}" stroke-opacity="0.7" stroke-width="1"/>'
            )
        svg.append(f'  <text class="stat-label" x="{text_x}" y="{STAT_LABEL_Y}">{escape(label)}</text>')
        svg.append(f'  <text class="stat-value" x="{text_x}" y="{STAT_VALUE_Y}">{escape(value)}</text>')
        if sub:
            svg.append(f'  <text class="stat-sub" x="{text_x}" y="{STAT_SUB_Y}">{escape(sub)}</text>')

    svg.append("</svg>")
    svg.append("")
    return "\n".join(svg)


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
def main() -> int:
    """Read the JSON, render the SVG, save it. Returns a process exit code."""
    animated = not is_static_mode()
    try:
        data = load_report(INPUT_PATH)
        days = extract_days(data)

        missing = report_gaps(days)
        if missing > 0:
            print(
                f"[WARN] {missing} calendar date(s) are missing from the JSON; "
                "they are left empty in the heatmap, not invented.",
                file=sys.stderr,
            )

        cells, weeks, cuts = build_cells(days)
        total = compute_total(data, cells)
        stats = build_stats(data, cells, total)
        svg_text = render_svg(data, cells, weeks, total, stats, animated)

        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(svg_text, encoding="utf-8", newline="\n")
    except HeatmapError as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"[ERROR] Could not write the output file: {error}", file=sys.stderr)
        return 1

    mode = "animated" if animated else "static (no animation)"
    print(f"[OK] Saved: {OUTPUT_PATH}")
    print(f"[OK] Mode:  {mode}")
    print(f"[OK] Range: {days[0][0].isoformat()} to {days[-1][0].isoformat()} "
          f"({len(cells)} days, {weeks} week columns)")
    print(f"[OK] Total contributions: {total}")
    if cuts:
        print(f"[OK] Level cut-offs (levels 1-4 up to): {cuts}; level 5 is anything higher")
    else:
        print("[OK] No contributions in range: every cell is level 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())