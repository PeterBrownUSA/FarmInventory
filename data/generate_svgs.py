#!/usr/bin/env python3
"""
Generate individual SVG label files for xTool Creative Space.
Each SVG is one 86mm × 54mm card layout ready for laser engraving.

Reads: output/labels_batch.csv
Outputs: output/svg/<NNN>_<variety_name>.svg
"""

import csv
import os
import re
import html

# Max characters for Use field before abbreviating
MAX_USE_LEN = 45

# Abbreviation map for common Use terms
USE_ABBREV = {
    "Cooking/Sauce": "Cook",
    "Eating Fresh": "Fresh",
    "Sweet Cider": "Cider",
    "Hard Cider": "Hard Cider",
}


def shorten_use(use_str):
    """Abbreviate Use field if it exceeds MAX_USE_LEN."""
    if len(use_str) <= MAX_USE_LEN:
        return use_str
    parts = [p.strip() for p in use_str.split(";")]
    shortened = [USE_ABBREV.get(p, p) for p in parts]
    result = "; ".join(shortened)
    return result

# Card dimensions in mm
CARD_W = 86
CARD_H = 54
MARGIN = 3  # mm from edge

# Font sizes in mm (converted to SVG units)
FONT_NAME = 4.5
FONT_TYPE = 3.2
FONT_DETAIL = 2.8
FONT_FOOTER = 2.5

# Vertical positions (Y in mm from top)
LAYOUT = {
    "name":      7,
    "type":     12.5,
    "bloom":    19,
    "harvest":  24,
    "fertility": 29,
    "use":      34,
    "origin":   39,
    "year":     46,
    "footer":   51,
}

# Horizontal positions
LEFT = MARGIN
CENTER_X = CARD_W / 2


def sanitize_filename(name):
    """Create a safe filename from a variety name."""
    s = re.sub(r'[^\w\s-]', '', name)
    s = re.sub(r'\s+', '_', s.strip())
    return s


def escape(text):
    """Escape text for SVG XML."""
    return html.escape(str(text), quote=True)


def generate_svg(row, index):
    """Generate SVG content for one label."""
    name = row.get("Name", "")
    tree_type = row.get("Type", "")
    bloom = row.get("Bloom_Period", "")
    harvest = row.get("Harvest_Period", "")
    fertility = row.get("Fertility", "")
    use = shorten_use(row.get("Use", ""))
    origin = row.get("Origin", "")
    year = row.get("Year_Planted", "")
    footer = row.get("Footer", "")

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{CARD_W}mm" height="{CARD_H}mm"
     viewBox="0 0 {CARD_W} {CARD_H}">

  <!-- Card boundary (not engraved — for alignment only) -->
  <rect x="0" y="0" width="{CARD_W}" height="{CARD_H}"
        fill="none" stroke="#cccccc" stroke-width="0.1" />

  <!-- Variety Name (large, centered) -->
  <text x="{CENTER_X}" y="{LAYOUT['name']}"
        font-family="Arial, Helvetica, sans-serif"
        font-size="{FONT_NAME}" font-weight="bold"
        text-anchor="middle" fill="black">{escape(name)}</text>

  <!-- Type (centered, below name) -->
  <text x="{CENTER_X}" y="{LAYOUT['type']}"
        font-family="Arial, Helvetica, sans-serif"
        font-size="{FONT_TYPE}" font-style="italic"
        text-anchor="middle" fill="black">{escape(tree_type)}</text>

  <!-- Separator line -->
  <line x1="{MARGIN}" y1="15" x2="{CARD_W - MARGIN}" y2="15"
        stroke="black" stroke-width="0.2" />

  <!-- Detail fields (centered) -->
  <text x="{CENTER_X}" y="{LAYOUT['bloom']}"
        font-family="Arial, Helvetica, sans-serif"
        font-size="{FONT_DETAIL}" text-anchor="middle" fill="black">Bloom: {escape(bloom)}</text>

  <text x="{CENTER_X}" y="{LAYOUT['harvest']}"
        font-family="Arial, Helvetica, sans-serif"
        font-size="{FONT_DETAIL}" text-anchor="middle" fill="black">Harvest: {escape(harvest)}</text>

  <text x="{CENTER_X}" y="{LAYOUT['fertility']}"
        font-family="Arial, Helvetica, sans-serif"
        font-size="{FONT_DETAIL}" text-anchor="middle" fill="black">Fertility: {escape(fertility)}</text>

  <text x="{CENTER_X}" y="{LAYOUT['use']}"
        font-family="Arial, Helvetica, sans-serif"
        font-size="{FONT_DETAIL}" text-anchor="middle" fill="black">Use: {escape(use)}</text>

  <text x="{CENTER_X}" y="{LAYOUT['origin']}"
        font-family="Arial, Helvetica, sans-serif"
        font-size="{FONT_DETAIL}" text-anchor="middle" fill="black">Origin: {escape(origin)}</text>

  <!-- Separator line -->
  <line x1="{MARGIN}" y1="42" x2="{CARD_W - MARGIN}" y2="42"
        stroke="black" stroke-width="0.2" />

  <!-- Year Planted (centered) -->
  <text x="{CENTER_X}" y="{LAYOUT['year']}"
        font-family="Arial, Helvetica, sans-serif"
        font-size="{FONT_DETAIL}" font-weight="bold"
        text-anchor="middle" fill="black">Planted: {escape(year)}</text>

  <!-- Footer (centered) -->
  <text x="{CENTER_X}" y="{LAYOUT['footer']}"
        font-family="Arial, Helvetica, sans-serif"
        font-size="{FONT_FOOTER}"
        text-anchor="middle" fill="black">{escape(footer)}</text>

</svg>'''
    return svg


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    csv_path = os.path.join(project_dir, "output", "labels_batch.csv")
    svg_dir = os.path.join(project_dir, "output", "svg")

    os.makedirs(svg_dir, exist_ok=True)

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Read {len(rows)} labels from {csv_path}")

    for i, row in enumerate(rows, start=1):
        name = row.get("Name", f"label_{i}")
        filename = f"{i:03d}_{sanitize_filename(name)}.svg"
        filepath = os.path.join(svg_dir, filename)

        svg_content = generate_svg(row, i)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg_content)

    print(f"Generated {len(rows)} SVG files in {svg_dir}/")
    print(f"Each file is {CARD_W}mm × {CARD_H}mm — open individually in XCS")


if __name__ == "__main__":
    main()
