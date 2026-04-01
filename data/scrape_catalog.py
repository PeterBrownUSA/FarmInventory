#!/usr/bin/env python3
"""
Trees of Antiquity Catalog Scraper
Parses Shopify JSON API to extract botanical data for label engraving.
"""

import json
import csv
import re
import sys
import time
from urllib.request import urlopen, Request
from html.parser import HTMLParser

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

BASE_URL = "https://www.treesofantiquity.com/collections/{}/products.json?limit=250"
FOOTER = "Planted by: Peter Brown & Robyn Seely"


class HTMLStripper(HTMLParser):
    """Strip HTML tags and return plain text."""
    def __init__(self):
        super().__init__()
        self.result = []
    def handle_data(self, data):
        self.result.append(data)
    def get_text(self):
        return ''.join(self.result)


def strip_html(html_str):
    """Remove HTML tags from a string."""
    s = HTMLStripper()
    s.feed(html_str or "")
    return s.get_text()


def extract_from_tags(tags):
    """Extract structured data from Shopify product tags."""
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
    """Extract structured data from product description HTML."""
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
    """Remove tree-type suffixes from variety names for label use."""
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
    """Fetch all products from a collection and parse botanical data."""
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
        
        # Extract data from tags (primary) and body (fallback)
        tag_data = extract_from_tags(tags)
        body_data = extract_from_body(body_html)
        
        # Merge: prefer tag data, fall back to body
        bloom = tag_data["bloom_period"] or body_data.get("bloom_period", "")
        harvest = tag_data["harvest_period"] or body_data.get("harvest_period", "")
        pollination = tag_data["pollination"] or body_data.get("pollination", "")
        origin = body_data.get("origin", "") or tag_data["origin"]  # body has more detail for origin
        uses_list = tag_data["uses"] if tag_data["uses"] else [body_data.get("uses", "")]
        uses = "; ".join([u for u in uses_list if u])
        
        # Clean up pollination for label brevity
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
    print("=" * 60)
    print("Trees of Antiquity — Full Catalog Scraper")
    print("=" * 60)
    print()
    
    all_varieties = []
    
    for slug, tree_type in COLLECTIONS:
        varieties = fetch_collection(slug, tree_type)
        all_varieties.extend(varieties)
        time.sleep(0.5)  # Be polite to the server
    
    # Deduplicate by name + type
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
    
    # Write master inventory CSV
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
    
    # Also write a summary by type
    type_counts = {}
    for v in unique:
        type_counts[v["type"]] = type_counts.get(v["type"], 0) + 1
    
    print("\nVarieties by category:")
    for t in sorted(type_counts.keys()):
        print(f"  {t:20s} {type_counts[t]:3d}")
    
    print(f"\nTotal: {len(unique)} varieties")
    print(f"\nDone! Open {csv_path} in Excel/Google Sheets to mark your inventory.")


if __name__ == "__main__":
    main()
