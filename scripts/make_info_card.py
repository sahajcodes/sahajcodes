#!/usr/bin/env python3
"""Generate a neofetch-inspired developer info card as an SVG.

Output: <project root>/data/info-card.svg

Usage (Windows PowerShell):
    python scripts/make_info_card.py                       # animated
    $env:STATIC="1"; python scripts/make_info_card.py      # static
    Remove-Item Env:STATIC                                 # back to animated
"""

from __future__ import annotations

import os
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

# --------------------------------------------------------------------------
# Paths (resolved relative to this script, not the terminal's current folder)
# --------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "info-card.svg"

# --------------------------------------------------------------------------
# Colors
# --------------------------------------------------------------------------
BG = "#0d1117"
PANEL = "#161b22"
BORDER = "#30363d"
TEXT = "#e6edf3"
MUTED = "#8b949e"
BLUE = "#58a6ff"
GREEN = "#3fb950"

DOT_RED = "#ff5f56"
DOT_YELLOW = "#ffbd2e"
DOT_GREEN = "#27c93f"

# --------------------------------------------------------------------------
# Content
# --------------------------------------------------------------------------
TITLE = "sahajcodes \u2014 info"
PROMPT_USER = "sahajcodes@github"
PROMPT_COMMAND = "neofetch"

ROWS = [
    ("NOW", "Building practical projects and learning by doing"),
    ("FOCUS", "Web development, problem solving, and DSA"),
    ("STACK", "HTML, CSS, JavaScript, Python, and Git"),
    ("HIGHLIGHTS", "Project-driven learning and continuous improvement"),
]

# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------
WIDTH = 760
CORNER_RADIUS = 12
TITLE_BAR_HEIGHT = 44
PADDING_X = 36
LABEL_X = PADDING_X
VALUE_X = 190
WRAP_CHARS = 54          # max characters per value line (fits inside the card)
LINE_HEIGHT = 22
ROW_GAP = 16
PROMPT_Y = 86
SEPARATOR_Y = 108
FIRST_ROW_Y = 142
BOTTOM_PADDING = 30

# --------------------------------------------------------------------------
# Animation
# --------------------------------------------------------------------------
ANIM_START_DELAY = 0.35   # seconds before the first row appears
ANIM_STAGGER = 0.18       # seconds between rows
ANIM_DURATION = 0.6       # seconds per row


def is_static_mode() -> bool:
    """Return True when the STATIC environment variable is set to a truthy value."""
    value = os.environ.get("STATIC", "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def wrap_value(text: str) -> list[str]:
    """Wrap a value string into lines that fit inside the card."""
    lines = textwrap.wrap(text, width=WRAP_CHARS)
    return lines if lines else [""]


def build_css(animated: bool) -> str:
    """Build the <style> contents. Plain strings are used on purpose so that
    CSS braces never conflict with Python f-string syntax."""
    css = [
        ".mono { font-family: ui-monospace, SFMono-Regular, Consolas, "
        "\"Liberation Mono\", Menlo, monospace; }",
        ".title { font-size: 13px; fill: " + MUTED + "; }",
        ".prompt { font-size: 15px; }",
        ".label { font-size: 14px; font-weight: 700; letter-spacing: 0.6px; "
        "fill: " + BLUE + "; }",
        ".value { font-size: 14px; fill: " + TEXT + "; }",
    ]

    if animated:
        css.append(
            ".row { opacity: 0; "
            "animation-name: rowIn; "
            "animation-duration: " + str(ANIM_DURATION) + "s; "
            "animation-timing-function: ease-out; "
            "animation-fill-mode: both; }"
        )
        css.append(
            "@keyframes rowIn { "
            "from { opacity: 0; transform: translateY(8px); } "
            "to { opacity: 1; transform: translateY(0); } }"
        )
        css.append(
            "@media (prefers-reduced-motion: reduce) { "
            ".row { animation: none; opacity: 1; } }"
        )

    return "\n    ".join(css)


def build_row(index: int, label: str, value: str, y: float,
              animated: bool, is_last: bool) -> tuple[str, float]:
    """Build the SVG group for one row.

    Returns (svg_markup, baseline_y_of_the_last_text_line).
    """
    lines = wrap_value(value)
    last_baseline = y + (len(lines) - 1) * LINE_HEIGHT

    if animated:
        delay = ANIM_START_DELAY + index * ANIM_STAGGER
        open_tag = '<g class="row" style="animation-delay: {:.2f}s">'.format(delay)
    else:
        open_tag = "<g>"

    parts = [open_tag]
    parts.append(
        f'<text class="mono label" x="{LABEL_X}" y="{y}">{escape(label)}</text>'
    )
    for i, line in enumerate(lines):
        line_y = y + i * LINE_HEIGHT
        parts.append(
            f'<text class="mono value" x="{VALUE_X}" y="{line_y}">{escape(line)}</text>'
        )

    if not is_last:
        sep_y = last_baseline + (LINE_HEIGHT + ROW_GAP - 8) / 2
        parts.append(
            f'<line x1="{PADDING_X}" y1="{sep_y}" x2="{WIDTH - PADDING_X}" '
            f'y2="{sep_y}" stroke="{BORDER}" stroke-opacity="0.45" stroke-width="1"/>'
        )

    parts.append("</g>")
    return "\n  ".join(parts), last_baseline


def build_svg(animated: bool) -> str:
    """Assemble the complete SVG document."""
    # Lay out rows first so the card height fits the content.
    row_markup = []
    y = float(FIRST_ROW_Y)
    last_baseline = y
    for index, (label, value) in enumerate(ROWS):
        is_last = index == len(ROWS) - 1
        markup, last_baseline = build_row(index, label, value, y, animated, is_last)
        row_markup.append(markup)
        y = last_baseline + LINE_HEIGHT + ROW_GAP

    height = int(last_baseline + BOTTOM_PADDING)
    inner_width = WIDTH - 1
    inner_height = height - 1

    prompt = (
        f'<text class="mono prompt" x="{PADDING_X}" y="{PROMPT_Y}" xml:space="preserve">'
        f'<tspan fill="{GREEN}">{escape(PROMPT_USER)}</tspan>'
        f'<tspan fill="{MUTED}">:</tspan>'
        f'<tspan fill="{BLUE}">~</tspan>'
        f'<tspan fill="{MUTED}">$ </tspan>'
        f'<tspan fill="{TEXT}">{escape(PROMPT_COMMAND)}</tspan>'
        f"</text>"
    )

    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img" '
        f'aria-label="Developer information card">',
        "  <title>Developer information card</title>",
        "  <style>",
        "    " + build_css(animated),
        "  </style>",
        "  <defs>",
        f'    <clipPath id="card-clip"><rect x="0.5" y="0.5" width="{inner_width}" '
        f'height="{inner_height}" rx="{CORNER_RADIUS}" ry="{CORNER_RADIUS}"/></clipPath>',
        "  </defs>",
        "",
        "  <!-- Card background -->",
        f'  <rect x="0.5" y="0.5" width="{inner_width}" height="{inner_height}" '
        f'rx="{CORNER_RADIUS}" ry="{CORNER_RADIUS}" fill="{BG}"/>',
        "",
        "  <!-- Title bar -->",
        '  <g clip-path="url(#card-clip)">',
        f'    <rect x="0" y="0" width="{WIDTH}" height="{TITLE_BAR_HEIGHT}" fill="{PANEL}"/>',
        f'    <line x1="0" y1="{TITLE_BAR_HEIGHT}" x2="{WIDTH}" y2="{TITLE_BAR_HEIGHT}" '
        f'stroke="{BORDER}" stroke-width="1"/>',
        "  </g>",
        f'  <circle cx="24" cy="22" r="6" fill="{DOT_RED}"/>',
        f'  <circle cx="44" cy="22" r="6" fill="{DOT_YELLOW}"/>',
        f'  <circle cx="64" cy="22" r="6" fill="{DOT_GREEN}"/>',
        f'  <text class="mono title" x="{WIDTH / 2}" y="26" text-anchor="middle">'
        f"{escape(TITLE)}</text>",
        "",
        "  <!-- Prompt line -->",
        "  " + prompt,
        f'  <line x1="{PADDING_X}" y1="{SEPARATOR_Y}" x2="{WIDTH - PADDING_X}" '
        f'y2="{SEPARATOR_Y}" stroke="{BORDER}" stroke-width="1"/>',
        "",
        "  <!-- Information rows -->",
    ]

    for markup in row_markup:
        svg.append("  " + markup)

    svg.extend([
        "",
        "  <!-- Card border -->",
        f'  <rect x="0.5" y="0.5" width="{inner_width}" height="{inner_height}" '
        f'rx="{CORNER_RADIUS}" ry="{CORNER_RADIUS}" fill="none" stroke="{BORDER}" '
        f'stroke-width="1"/>',
        "</svg>",
        "",
    ])

    return "\n".join(svg)


def main() -> None:
    static = is_static_mode()
    svg_text = build_svg(animated=not static)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(svg_text, encoding="utf-8", newline="\n")

    mode = "static (no animation)" if static else "animated"
    print(f"[OK] Saved: {OUTPUT_PATH}")
    print(f"[OK] Mode:  {mode}")


if __name__ == "__main__":
    main()