#!/usr/bin/env python3
"""Fetch a public GitHub contribution calendar and save statistics as JSON.

No GraphQL API and no access token are needed. The script reads:
    https://github.com/users/<USERNAME>/contributions

Output: <project root>/data/contributions.json

Usage (Windows PowerShell):
    python scripts/fetch_contributions.py
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
USERNAME = "sahajcodes"
CONTRIBUTIONS_URL = f"https://github.com/users/{USERNAME}/contributions"
REQUEST_TIMEOUT_SECONDS = 20

# Paths are resolved relative to this script, not the terminal's folder.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "contributions.json"

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 "
        "sahajcodes-profile-readme-script"
    ),
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}

# Matches text such as "3 contributions on May 4th." or "No contributions on ..."
COUNT_TEXT_PATTERN = re.compile(r"^\s*(no|[\d,]+)\s+contributions?\b", re.IGNORECASE)


class ContributionError(Exception):
    """Raised for any problem fetching or parsing the contribution calendar."""


@dataclass
class ContributionDay:
    """One calendar day."""

    day: date
    count: int
    level: Optional[int]


# --------------------------------------------------------------------------
# Fetching
# --------------------------------------------------------------------------
def fetch_html(url: str) -> str:
    """Download the contribution calendar HTML, raising ContributionError on failure."""
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise ContributionError(
            f"The request timed out after {REQUEST_TIMEOUT_SECONDS} seconds. "
            "Check your internet connection and try again."
        )
    except requests.exceptions.HTTPError as error:
        status = error.response.status_code if error.response is not None else "unknown"
        if status == 404:
            raise ContributionError(
                f"HTTP 404: GitHub user '{USERNAME}' was not found. Check the username."
            )
        if status in (403, 429):
            raise ContributionError(
                f"HTTP {status}: GitHub is rate limiting or blocking this request. "
                "Wait a few minutes and try again."
            )
        raise ContributionError(f"GitHub returned HTTP status {status}.")
    except requests.exceptions.ConnectionError:
        raise ContributionError(
            "Could not connect to github.com. Check your internet connection, "
            "VPN, or firewall."
        )
    except requests.exceptions.RequestException as error:
        raise ContributionError(f"Network error while fetching data: {error}")

    if not response.text.strip():
        raise ContributionError("GitHub returned an empty response.")
    return response.text


# --------------------------------------------------------------------------
# Parsing
# --------------------------------------------------------------------------
def parse_count_text(text: str) -> Optional[int]:
    """Turn 'No contributions on ...' or '12 contributions on ...' into an int.

    Returns None when the text is not in the expected format.
    """
    match = COUNT_TEXT_PATTERN.match(text)
    if match is None:
        return None
    value = match.group(1).lower()
    if value == "no":
        return 0
    return int(value.replace(",", ""))


def parse_level(raw_level: Optional[str]) -> Optional[int]:
    """Convert the data-level attribute to an int, or None if absent or invalid."""
    if raw_level is None:
        return None
    try:
        return int(raw_level)
    except ValueError:
        return None


def parse_days(html: str) -> list[ContributionDay]:
    """Parse all contribution day cells from the calendar HTML."""
    soup = BeautifulSoup(html, "html.parser")

    # Map each cell id to its tooltip text (the count lives in the tooltip).
    tooltip_by_cell_id: dict[str, str] = {}
    for tooltip in soup.find_all("tool-tip"):
        target_id = tooltip.get("for")
        if target_id:
            tooltip_by_cell_id[target_id] = tooltip.get_text(" ", strip=True)

    # Day cells are the elements that carry a data-date attribute.
    cells = soup.find_all(attrs={"data-date": True})
    if not cells:
        raise ContributionError(
            "No contribution cells were found. GitHub may have changed its HTML, "
            "or the profile has no public calendar."
        )

    days_by_date: dict[date, ContributionDay] = {}
    unresolved_dates: list[str] = []

    for cell in cells:
        raw_date = cell.get("data-date", "")
        try:
            cell_date = date.fromisoformat(raw_date)
        except ValueError:
            raise ContributionError(f"Unexpected date format in calendar: {raw_date!r}")

        count: Optional[int] = None

        # Source 1: a data-count attribute (older GitHub layout).
        raw_count = cell.get("data-count")
        if raw_count is not None:
            try:
                count = int(raw_count)
            except ValueError:
                count = None

        # Source 2: the linked <tool-tip> element (current GitHub layout).
        if count is None:
            tooltip_text = tooltip_by_cell_id.get(cell.get("id", ""))
            if tooltip_text:
                count = parse_count_text(tooltip_text)

        # Source 3: text inside the cell itself (screen-reader span).
        if count is None:
            count = parse_count_text(cell.get_text(" ", strip=True))

        if count is None:
            unresolved_dates.append(raw_date)
            continue

        days_by_date[cell_date] = ContributionDay(
            day=cell_date,
            count=count,
            level=parse_level(cell.get("data-level")),
        )

    # Never guess a count: stop if any cell could not be read.
    if unresolved_dates:
        sample = ", ".join(unresolved_dates[:3])
        raise ContributionError(
            f"Could not read a contribution count for {len(unresolved_dates)} "
            f"day(s) (for example: {sample}). GitHub's HTML may have changed."
        )

    return [days_by_date[key] for key in sorted(days_by_date)]


# --------------------------------------------------------------------------
# Statistics
# --------------------------------------------------------------------------
def compute_longest_streak(days: list[ContributionDay]) -> dict:
    """Longest run of consecutive calendar days that each have contributions."""
    longest_length = 0
    longest_start: Optional[date] = None
    longest_end: Optional[date] = None

    run_length = 0
    run_start: Optional[date] = None
    previous_active: Optional[date] = None

    for item in days:
        if item.count > 0:
            is_continuation = (
                previous_active is not None and (item.day - previous_active).days == 1
            )
            if is_continuation:
                run_length += 1
            else:
                run_length = 1
                run_start = item.day
            previous_active = item.day

            if run_length > longest_length:
                longest_length = run_length
                longest_start = run_start
                longest_end = item.day
        else:
            run_length = 0
            run_start = None
            previous_active = None

    return {
        "length": longest_length,
        "start": longest_start.isoformat() if longest_start else None,
        "end": longest_end.isoformat() if longest_end else None,
    }


def compute_current_streak(days: list[ContributionDay]) -> dict:
    """Current streak, counted backwards from the last day in the calendar.

    If the last day has zero contributions, it is skipped (the day may not be
    over yet), so the streak is not broken until a full day is missed.
    """
    length = 0
    start: Optional[date] = None
    end: Optional[date] = None

    index = len(days) - 1
    if index >= 0 and days[index].count == 0:
        index -= 1

    expected_date: Optional[date] = None
    while index >= 0:
        item = days[index]
        if item.count == 0:
            break
        if expected_date is not None and item.day != expected_date:
            break
        length += 1
        start = item.day
        if end is None:
            end = item.day
        expected_date = item.day - timedelta(days=1)
        index -= 1

    return {
        "length": length,
        "start": start.isoformat() if start else None,
        "end": end.isoformat() if end else None,
    }


def compute_best_day(days: list[ContributionDay]) -> Optional[dict]:
    """Day with the most contributions (earliest wins ties). None if all zero."""
    best: Optional[ContributionDay] = None
    for item in days:
        if item.count > 0 and (best is None or item.count > best.count):
            best = item
    if best is None:
        return None
    return {"date": best.day.isoformat(), "count": best.count}


def compute_monthly_totals(days: list[ContributionDay]) -> dict[str, int]:
    """Total contributions per month, keyed 'YYYY-MM', in chronological order."""
    totals: dict[str, int] = {}
    for item in days:
        key = item.day.strftime("%Y-%m")
        totals[key] = totals.get(key, 0) + item.count
    return totals


def build_report(days: list[ContributionDay]) -> dict:
    """Assemble the final JSON-ready dictionary."""
    return {
        "username": USERNAME,
        "source": CONTRIBUTIONS_URL,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "range": {
            "start": days[0].day.isoformat(),
            "end": days[-1].day.isoformat(),
            "days_in_calendar": len(days),
        },
        "total_contributions": sum(item.count for item in days),
        "current_streak": compute_current_streak(days),
        "longest_streak": compute_longest_streak(days),
        "best_day": compute_best_day(days),
        "monthly_totals": compute_monthly_totals(days),
        "days": [
            {"date": item.day.isoformat(), "count": item.count, "level": item.level}
            for item in days
        ],
    }


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
def main() -> int:
    """Run the fetch, parse, and save workflow. Returns a process exit code."""
    print(f"Fetching contributions for '{USERNAME}' ...")
    try:
        html = fetch_html(CONTRIBUTIONS_URL)
        days = parse_days(html)
        report = build_report(days)

        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    except ContributionError as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"[ERROR] Could not write the output file: {error}", file=sys.stderr)
        return 1

    best = report["best_day"]
    best_text = f"{best['count']} on {best['date']}" if best else "none"

    print(f"[OK] Saved: {OUTPUT_PATH}")
    print(f"[OK] Range: {report['range']['start']} to {report['range']['end']}")
    print(f"[OK] Total contributions: {report['total_contributions']}")
    print(f"[OK] Current streak: {report['current_streak']['length']} day(s)")
    print(f"[OK] Longest streak: {report['longest_streak']['length']} day(s)")
    print(f"[OK] Best day: {best_text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())