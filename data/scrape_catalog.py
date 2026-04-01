#!/usr/bin/env python3
"""
scrape_catalog.py — Trees of Antiquity Catalog Scraper
======================================================

Fetches the full product catalog from Trees of Antiquity's Shopify
store via their public JSON API. Extracts botanical data (bloom period,
harvest period, fertility, origin, uses) from product tags and HTML
descriptions, then writes a clean CSV for use as a reference database.

  INPUT:
    Shopify JSON API at treesofantiquity.com (no API key required)

  OUTPUT:
    data/master_catalog.csv — One row per unique variety with columns:
      Name, Type, Bloom_Period, Harvest_Period, Fertility, Use, Origin,
      Year_Planted, Footer, Owned, Source_URL

  DATA EXTRACTION STRATEGY:
    Shopify products have two data sources:
    1. TAGS — Structured key-value pairs (e.g., "Bloom Period_Midseason")
       Best for: bloom period, harvest, pollination, uses
    2. BODY HTML — Free-text product description
       Best for: origin (more detailed than tags), bloom/harvest fallback

    The scraper uses tags as primary source, falling back to body HTML
    parsing via regex when tag data is missing. Origin always prefers
    the body HTML (more specific location info).

  RATE LIMITING:
    0.5 second delay between collection requests to be respectful.

Usage:
    python3 data/scrape_catalog.py

Dependencies:
    Python 3.6+ (stdlib only — json, csv, re, urllib, html.parser, time)

Note:
    After scraping, you may need to add OVERRIDES in generate_labels.py
    for any varieties with incomplete data. The scraper does its best
    but some product pages lack structured tags.
"""

import json
import csv
import re
import sys
import time
from urllib.request import urlopen, Request
from html.parser import HTMLParser

# ══════════════════════════════════════════════════════════════════════
# COLLECTION DEFINITIONS
# ══════════════════════════════════════════════════════════════════════
# Each tuple is (shopify_collection_slug, display_type_name).
# The slug is used in the API URL; the type name is written to the CSV.
# Order doesn't matter — all collections are fetched and merged.
# ══════════════════════════════════════════════════════════════════════
COLLECTIONS = [
    ("apple-trees", "Apple"),
    ("apricot-trees", "Apricot"),
    ("cherry-trees", "Cherry"),
    ("fig-trees", "Fig"),
    ("jujube-trees", "Jujube"),
    ("mulberry-tree", "Mulberry"),
    ("nectarine-tree", "Nectarine"),
    ("pear-trees", "Pear"),
    ("persimmon-trees", "Persimmon"),
    ("plum-trees", "Plum"),
    ("pluots", "Pluot"),
    ("pomegranate-bush", "Pomegranate"),
    ("quince-trees", "Quince"),
    ("peach-trees", "Peach"),
    ("grapes", "Grape"),
    ("nut-trees", "Nut Tree"),
    ("smaller-1-year-fruit-trees", "Elderberry/Feijoa"),
    ("medlar", "Medlar"),
    ("berries-small-fruit", "Berry"),
    ("assortment-small-berries", "Blueberry"),
]

# Shopify JSON API URL template — {slug} is replaced with collection slug.
# The ?limit=250 parameter fetches all products in one request (max allowed).
BASE_URL = "https://www.treesofantiquity.com/collections/{}/products.json?limit=250"

# Footer text included in the CSV (used by older versions of the pipeline)
FOOTER = "Planted by: Peter Brown & Robyn Seely"


class HTMLStripper(HTMLParser):
    """
    Simple HTML tag stripper that extracts plain text from HTML.

    Used to clean Shopify product body_html fields, which contain
    formatted descriptions with <p>, <strong>, <br> tags, etc.
    """
    def __init__(self):
        super().__init__()
        self.result = []

    def handle_data(self, data):
        self.result.append(data)

    def get_text(self):
        return ''.join(self.result)


def strip_html(html_str):
    """
    Remove all HTML tags from a string, returning plain text.

    Args:
        html_str: HTML string (may be None)

    Returns:
        Plain text with tags removed
    """
    s = HTMLStripper()
    s.feed(html_str or "")
    return s.get_text()


def extract_from_tags(tags):
    """
    Extract botanical data from Shopify product tags.

    Shopify tags use a prefix convention:
      - "Bloom Period_Midseason"  → bloom_period = "Midseason"
      - "Harvest_Late"            → harvest_period = "Late"
      - "Pollination_Self-Fertile"→ pollination = "Self-Fertile"
      - "Origin Date_1800s"       → origin = "1800s"
      - "Uses_Eating Fresh"       → uses = ["Eating Fresh"]

    Multiple "Uses_" tags are collected into a list.

    Args:
        tags: List of tag strings from the Shopify product JSON

    Returns:
        dict with keys: bloom_period, harvest_period, pollination, origin, uses
    """
    data = {
        "bloom_period": "",
        "harvest_period": "",
        "pollination": "",
        "origin": "",
        "uses": [],
    }
    for tag in tags:
        tag_lower = tag.lower()
        if tag.startswith("Bloom Period_"):
            data["bloom_period"] = tag.split("_", 1)[1].strip()
        elif tag.startswith("Harvest_"):
            data["harvest_period"] = tag.split("_", 1)[1].strip()
        elif tag.startswith("Pollination_"):
            data["pollination"] = tag.split("_", 1)[1].strip()
        elif tag.startswith("Origin Date_"):
            data["origin"] = tag.split("_", 1)[1].strip()
        elif tag.startswith("Uses_"):
            use = tag.split("_", 1)[1].strip()
            if use not in data["uses"]:
                data["uses"].append(use)
    return data


def extract_from_body(body_html):
    """
    Extract botanical data from the product description HTML.

    This is the fallback data source when tags are missing or incomplete.
    Uses regex patterns to find labeled fields in the plain text, e.g.:
      "Origin Date: England 1809"
      "Bloom Period: Late"
      "Pollination Requirement: Self-Fertile"

    Patterns are designed to stop at the next field label or line break
    to avoid capturing too much text.

    Args:
        body_html: Raw HTML string from Shopify product body_html

    Returns:
        dict with any found keys: bloom_period, harvest_period,
        pollination, origin, uses
    """
    text = strip_html(body_html or "")
    data = {}

    patterns = {
        "bloom_period": [
            r"Bloom Period:\s*(.+?)(?:\n|$|Pollination|Origin|Storage|Harvest|Uses|Disease)",
            r"Bloom:\s*(.+?)(?:\n|$|Pollination|Origin|Storage|Harvest|Uses|Disease)",
        ],
        "harvest_period": [
            r"Harvest Period:\s*(.+?)(?:\n|$|Bloom|Pollination|Origin|Storage|Uses|Disease|Low)",
        ],
        "pollination": [
            r"Pollination Requirement:\s*(.+?)(?:\n|$|Origin|Storage|Bloom|Harvest|Disease)",
        ],
        "origin": [
            r"Origin Date:\s*(.+?)(?:\n|$|Storage|Rootstock|Bloom|Harvest|Disease|Pollination)",
            r"Origin:\s*(.+?)(?:\n|$|Storage|Rootstock|Bloom|Harvest|Disease|Pollination)",
        ],
        "uses": [
            r"Uses:\s*(.+?)(?:\n|$|Harvest|Bloom|Pollination|Origin|Storage|Disease|Low)",
        ],
    }

    for field, pats in patterns.items():
        for pat in pats:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                val = m.group(1).strip().rstrip('.')
                # Clean up common artifacts
                val = re.sub(r'\s+', ' ', val)
                data[field] = val
                break

    return data


def clean_variety_name(title, tree_type):
    """
    Remove tree-type suffixes from product titles for cleaner label names.

    Shopify product titles often include the type (e.g., "Bramley Seedling Apple Tree").
    This strips common suffixes to get just the variety name.

    Args:
        title: Full product title from Shopify
        tree_type: The collection type (e.g., "Apple", "Cherry")

    Returns:
        Cleaned variety name (e.g., "Bramley Seedling")
    """
    # Remove common suffixes like "Apple Tree", "Pear Tree", etc.
    suffixes = [
        f" {tree_type} Tree", f" {tree_type}", " Tree", " Bush", " Vine",
        " tree", " bush", " vine"
    ]
    name = title
    for suffix in suffixes:
        if name.endswith(suffix):
            name = name[:-len(suffix)]
            break
    return name.strip()


def fetch_collection(slug, tree_type):
    """
    Fetch all products from one Shopify collection and parse botanical data.

    Makes an HTTP GET request to the Shopify JSON API, then for each product:
      1. Extracts data from tags (primary source)
      2. Extracts data from body HTML (fallback source)
      3. Merges both sources (tags preferred, body as fallback)
      4. Normalizes the pollination field into a fertility label
      5. Cleans the variety name

    Args:
        slug: Shopify collection slug (e.g., "apple-trees")
        tree_type: Display name for this collection (e.g., "Apple")

    Returns:
        List of dicts, each containing parsed variety data
    """
    url = BASE_URL.format(slug)
    print(f"  Fetching: {slug} ({tree_type})...", end=" ", flush=True)
    
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (botanical-label-project)"})
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"ERROR: {e}")
        return []
    
    products = data.get("products", [])
    print(f"{len(products)} varieties found")

    results = []
    for product in products:
        title = product.get("title", "")
        tags = product.get("tags", [])
        body_html = product.get("body_html", "")

        # ── Extract data from both sources ──
        tag_data = extract_from_tags(tags)
        body_data = extract_from_body(body_html)

        # ── Merge: prefer tags for most fields, body for origin ──
        # Body HTML typically has more detailed origin info (includes location)
        # while tags only have the date portion.
        bloom = tag_data["bloom_period"] or body_data.get("bloom_period", "")
        harvest = tag_data["harvest_period"] or body_data.get("harvest_period", "")
        pollination = tag_data["pollination"] or body_data.get("pollination", "")
        origin = body_data.get("origin", "") or tag_data["origin"]
        uses_list = tag_data["uses"] if tag_data["uses"] else [body_data.get("uses", "")]
        uses = "; ".join([u for u in uses_list if u])

        # ── Normalize pollination into a clean fertility label ──
        # Converts various pollination descriptions into one of three categories
        poll_lower = pollination.lower()
        if "self-fertile" in poll_lower or "self fertile" in poll_lower or "self fruitful" in poll_lower:
            fertility = "Self-fertile"
        elif "none" in poll_lower or "sterile" in poll_lower:
            fertility = "Needs pollinator (triploid)"
        elif "requires" in poll_lower or "required" in poll_lower:
            fertility = "Needs pollinator"
        else:
            fertility = pollination if pollination else ""
        
        # Clean variety name
        name = clean_variety_name(title, tree_type)
        
        results.append({
            "name": name,
            "type": tree_type,
            "bloom_period": bloom,
            "harvest_period": harvest,
            "fertility": fertility,
            "use": uses,
            "origin": origin,
            "year_planted": "",
            "footer": FOOTER,
            "source_url": f"https://www.treesofantiquity.com/products/{product.get('handle', '')}",
        })
    
    return results


def main():
    """
    Main entry point — scrapes all collections and writes master_catalog.csv.

    Steps:
      1. Iterate through all defined collections
      2. Fetch and parse each collection's products via JSON API
      3. Deduplicate by (name, type) — some varieties appear in multiple collections
      4. Write the deduplicated catalog to CSV, sorted by type then name
      5. Print a summary report with variety counts by category
    """
    print("=" * 60)
    print("Trees of Antiquity — Full Catalog Scraper")
    print("=" * 60)
    print()
    
    all_varieties = []
    
    # ── Fetch each collection sequentially with rate limiting ──
    for slug, tree_type in COLLECTIONS:
        varieties = fetch_collection(slug, tree_type)
        all_varieties.extend(varieties)
        time.sleep(0.5)  # Rate limit: 0.5s between requests
    
    # ── Deduplicate varieties that appear in multiple collections ──
    # Some products are listed in more than one collection (e.g., a crab apple
    # might appear in both "apple-trees" and "smaller-1-year-fruit-trees").
    seen = set()
    unique = []
    for v in all_varieties:
        key = (v["name"].lower(), v["type"].lower())
        if key not in seen:
            seen.add(key)
            unique.append(v)
    
    print(f"\n{'=' * 60}")
    print(f"Total unique varieties: {len(unique)}")
    print(f"{'=' * 60}\n")
    
    # ── Write the master catalog CSV ──
    # Note: This CSV includes Year_Planted, Footer, and Owned columns for
    # historical compatibility, but the current pipeline ignores them.
    # The active schema uses my_trees.csv for ownership/planting data.
    csv_path = "/Users/peterbrown/developer/Trees/data/master_catalog.csv"
    headers = [
        "Name", "Type", "Bloom_Period", "Harvest_Period", "Fertility",
        "Use", "Origin", "Year_Planted", "Footer", "Owned", "Source_URL"
    ]
    
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for v in sorted(unique, key=lambda x: (x["type"], x["name"])):
            writer.writerow([
                v["name"],
                v["type"],
                v["bloom_period"],
                v["harvest_period"],
                v["fertility"],
                v["use"],
                v["origin"],
                v["year_planted"],
                v["footer"],
                "",  # Owned — user fills in YES
                v["source_url"],
            ])
    
    print(f"✅ Master catalog written to: {csv_path}")
    
    # ── Print summary by fruit type ──
    type_counts = {}
    for v in unique:
        type_counts[v["type"]] = type_counts.get(v["type"], 0) + 1
    
    print("\nVarieties by category:")
    for t in sorted(type_counts.keys()):
        print(f"  {t:20s} {type_counts[t]:3d}")
    
    print(f"\nTotal: {len(unique)} varieties")
    print(f"\nDone! The catalog can now be used by generate_labels.py.")
    print(f"If any varieties have missing data, add OVERRIDES in generate_labels.py.")


if __name__ == "__main__":
    main()
