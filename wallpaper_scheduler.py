#!/usr/bin/env python3
"""Select and apply a macOS wallpaper from a local time/calendar policy."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import Any


def parse_time(value: str) -> int:
    if value == "24:00":
        return 24 * 60
    hour, minute = (int(part) for part in value.split(":", 1))
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(f"invalid time: {value}")
    return hour * 60 + minute


def in_window(now: int, start: int, end: int) -> bool:
    if start == end:
        return True
    if start < end:
        return start <= now < end
    return now >= start or now < end


def select_wallpaper(config: dict[str, Any], current: dt.datetime) -> tuple[str, str]:
    date_key = current.date().isoformat()
    if date_key in config.get("holidays", []):
        day_type = "holiday"
    elif current.isoweekday() >= 6:
        day_type = "restday"
    else:
        day_type = "workday"

    minute = current.hour * 60 + current.minute
    for rule in config.get("rules", {}).get(day_type, []):
        if in_window(minute, parse_time(rule["start"]), parse_time(rule["end"])):
            return rule["wallpaper"], day_type
    return config["default_wallpaper"], day_type


def apply_wallpaper(path: str) -> None:
    image = Path(path).expanduser()
    if not image.exists():
        raise FileNotFoundError(f"wallpaper does not exist: {image}")
    script = f"tell application \"System Events\" to set picture of every desktop to POSIX file {json.dumps(str(image))}"
    subprocess.run(["osascript", "-e", script], check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--at", help="ISO datetime for deterministic testing")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    config = json.loads(args.config.expanduser().read_text())
    current = dt.datetime.fromisoformat(args.at) if args.at else dt.datetime.now()
    wallpaper, day_type = select_wallpaper(config, current)
    print(json.dumps({"date": current.isoformat(), "day_type": day_type, "wallpaper": wallpaper}, ensure_ascii=False))
    if not args.dry_run:
        apply_wallpaper(wallpaper)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
