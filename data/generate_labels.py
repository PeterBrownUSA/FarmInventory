#!/usr/bin/env python3
"""
Generate labels_batch.csv by joining:
  - data/my_trees.csv        (inventory — one row per physical plant)
  - data/master_catalog.csv  (reference — botanical data per variety)

Usage:
    python3 data/generate_labels.py

Output:
    output/labels_batch.csv  (one row per label, ready for XCS batch import)
"""

import csv
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(BASE_DIR, "data", "master_catalog.csv")
INVENTORY_PATH = os.path.join(BASE_DIR, "data", "my_trees.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "output", "labels_batch.csv")

FOOTER = "Planted by: Peter Brown & Robyn Seely"

# ── Manual overrides for varieties with incomplete catalog data ──
# Keys are lowercase catalog names; values fill in missing fields only.
OVERRIDES = {
    # Cherries — Summerland Research Station, BC
    "lapins":                   {"Origin": "British Columbia, 1984", "Bloom_Period": "Midseason"},
    "stella":                   {"Origin": "British Columbia, 1968"},
    "van":                      {"Origin": "British Columbia, 1944"},
    "black tartarian":          {"Origin": "Russia, 1794"},
    "black pearl":              {"Origin": "British Columbia, 2000s", "Fertility": "Self-fertile"},
    "skeena":                   {"Origin": "British Columbia, 1996", "Bloom_Period": "Midseason"},
    # Stone fruit
    "frost":                    {"Origin": "California, 1960s", "Bloom_Period": "Late"},
    "baby crawford":            {"Origin": "Ohio, 1870s", "Bloom_Period": "Midseason"},
    "george iv":                {"Origin": "New York, 1820s", "Bloom_Period": "Midseason"},
    "o'henry":                  {"Origin": "California, 1950s", "Bloom_Period": "Midseason"},
    "rio oso gem":              {"Origin": "California, 1926", "Bloom_Period": "Midseason"},
    "independence":             {"Origin": "California, 1960s", "Bloom_Period": "Midseason"},
    "goldmine":                 {"Origin": "New Zealand, 1890s", "Bloom_Period": "Early"},
    "snow queen":               {"Origin": "California, 1983", "Bloom_Period": "Early"},
    "puget gold":               {"Origin": "Washington, 1980s"},
    "blenheim":                 {"Origin": "England, 1815"},
    "elephant heart":           {"Origin": "California, 1920s"},
    "santa rosa":               {"Origin": "Santa Rosa, California, 1906"},
    # Apples — catalog origins with standardized formatting
    "christmas pink":           {"Origin": "Ettersburg, California, 1900s"},
    "mountain rose":            {"Origin": "Oregon, 1950s"},
    "pink parfait":             {"Origin": "California, 1900s"},
    "pink pearl":               {"Origin": "California, 1944"},
    "strawberry parfait":       {"Origin": "New Jersey, 1900s"},
    "winekist apple":           {"Origin": "Dakotas, 1949"},
    "rhode island greening":    {"Origin": "Rhode Island, 1650s"},
    "dolgo crab":               {"Origin": "South Dakota, 1897"},
    "jonathan":                 {"Origin": "New York, 1700s"},
    "white pearmain":           {"Origin": "England, 1200s"},
    "bramley seedling":         {"Origin": "England, 1809"},
    "glockenapfel":             {"Origin": "Switzerland, 1500s"},
    "cox orange pippin":        {"Origin": "England, 1830"},
    "winterstein":              {"Origin": "California, 1898"},
    "court pendu plat":         {"Origin": "France, 1613"},
    "knobbed russet":           {"Origin": "England, 1819"},
    "white transparent":        {"Origin": "Russia, 1850"},
    "duchess of oldenburg":     {"Origin": "Russia, 1700"},
    "belle de boskoop":         {"Origin": "Holland, 1856"},
    "niedwetzkyana":            {"Origin": "Kyrgyzstan, 1800s"},
    "ashmead's kernel apple":   {"Origin": "England, 1700s"},
    "foxwhelp":                 {"Origin": "England, 1664"},
    "hewes virginia crab":      {"Origin": "Virginia, 1817"},
    "harrison":                 {"Origin": "New Jersey, 1817"},
    "tremblett's bitter":       {"Origin": "England, 1800s"},
    "redstreak":                {"Origin": "England, 1600s"},
    "brown's cider":            {"Origin": "England, 1900s"},
    # Walnuts
    "chandler walnut":          {"Origin": "California, 1979"},
    "hartley walnut":           {"Origin": "Napa County, California, 1892"},
    "manregion english walnut": {"Origin": "Oregon, 1900s"},
    # Berries
    "marionberry":              {"Origin": "Oregon, 1956", "Bloom_Period": "Spring"},
    "loganberry":               {"Origin": "Santa Cruz, California, 1881", "Bloom_Period": "Spring"},
    "heritage red raspberries": {"Origin": "New York, 1969", "Bloom_Period": "Spring & fall"},
    "fall gold raspberries":    {"Origin": "New Hampshire, 1967", "Bloom_Period": "Spring & fall"},
    "chandler":                 {"Origin": "New Jersey, 1994", "Bloom_Period": "Midseason"},
    "sunshine":                 {"Origin": "Michigan, 2006", "Bloom_Period": "Midseason"},
    "jersey":                   {"Origin": "New Jersey, 1928", "Bloom_Period": "Midseason"},
    # Grapes
    "interlaken":               {"Origin": "New York, 1940s", "Bloom_Period": "Early"},
    "concord":                  {"Origin": "Concord, Massachusetts, 1849", "Bloom_Period": "Midseason"},
    "niagara":                  {"Origin": "Niagara County, New York, 1868", "Bloom_Period": "Midseason"},
    # Pears
    "white doyenne":            {"Origin": "Italy, 1550"},
    "beurre hardy":             {"Origin": "France, 1820"},
    # Other
    "black pakistan":            {"Origin": "Pakistan, ancient", "Bloom_Period": "Spring", "Harvest_Period": "Mid to late summer"},
    "kashmir":                  {"Origin": "Kashmir, India"},
    "grenada":                  {"Origin": "California"},
    "goji":                     {"Bloom_Period": "Late spring", "Harvest_Period": "Late summer", "Fertility": "Self-fertile", "Use": "Fresh eating; Dried; Medicinal", "Origin": "China, ancient"},
    "peter's honey":            {"Origin": "Sicily, Italy"},
    "smyrna":                   {"Origin": "Turkey, 1887"},
    "honan red":                {"Origin": "China, 1800s"},
    "black mulberry bush":      {"Origin": "Western Asia, ancient", "Bloom_Period": "Spring", "Harvest_Period": "Midsummer"},
    "crandall black currant":   {"Origin": "South Dakota, 1900s", "Bloom_Period": "Early spring", "Harvest_Period": "Midsummer"},
    "issai hardy kiwi":         {"Origin": "Japan", "Bloom_Period": "Late spring"},
    "jenny fuzzy kiwi":         {"Origin": "New Zealand", "Bloom_Period": "Late spring"},
    "eversweet":                {"Origin": "California"},
    "shanxi":                   {"Origin": "China, 1800s"},
    "sugarcane":                {"Origin": "China, 1800s"},
}

# ── Display-name overrides (catalog name -> prettier label name) ──
DISPLAY_NAMES = {
    "lapins":                   "Lapins Cherry",
    "black tartarian":          "Black Tartarian Cherry",
    "black pearl":              "Black Pearl Cherry",
    "stella":                   "Stella Cherry",
    "van":                      "Van Cherry",
    "puget gold":               "Puget Gold Apricot",
    "frost":                    "Frost Peach",
    "baby crawford":            "Baby Crawford Peach",
    "george iv":                "George IV Peach",
    "independence":             "Independence Nectarine",
    "goldmine":                 "Goldmine Nectarine",
    "snow queen":               "Snow Queen Nectarine",
    "bramley seedling":         "Bramley Seedling Apple",
    "rhode island greening":    "Rhode Island Greening Apple",
    "glockenapfel":             "Glockenapfel Apple",
    "cox orange pippin":        "Cox Orange Pippin Apple",
    "winterstein":              "Winterstein Apple",
    "dolgo crab":               "Dolgo Crab Apple",
    "court pendu plat":         "Court Pendu Plat Apple",
    "christmas pink":           "Christmas Pink Apple",
    "mountain rose":            "Mountain Rose Apple",
    "pink parfait":             "Pink Parfait Apple",
    "pink pearl":               "Pink Pearl Apple",
    "strawberry parfait":       "Strawberry Parfait Apple",
    "winekist apple":           "Winekist Apple",
    "kashmir":                  "Kashmir Pomegranate",
    "grenada":                  "Grenada Pomegranate",
    "goji":                     "Goji Berry",
    "black pakistan":            "Black Pakistan Mulberry",
    "peter's honey":            "Peter's Honey Fig",
    "heritage red raspberries": "Heritage Red Raspberry",
    "fall gold raspberries":    "Fall Gold Raspberry",
    "sunshine":                 "Sunshine Blueberry",
    "jersey":                   "Jersey Blueberry",
    "chandler":                 "Chandler Blueberry",
    # 2023 purchase additions
    "skeena":                   "Skeena Cherry",
    "knobbed russet":           "Knobbed Russet Apple",
    "niedwetzkyana":            "Niedwetzkyana Apple",
    "white transparent":        "White Transparent Apple",
    "duchess of oldenburg":     "Duchess of Oldenburg Apple",
    "belle de boskoop":         "Belle de Boskoop Apple",
    "smyrna":                   "Smyrna Quince",
    "interlaken":               "Interlaken Grape",
    "elephant heart":           "Elephant Heart Plum",
    "jonathan":                 "Jonathan Apple",
    "blenheim":                 "Blenheim Apricot",
    "santa rosa":               "Santa Rosa Plum",
    "rio oso gem":              "Rio Oso Gem Peach",
    "white pearmain":           "White Pearmain Apple",
    "black mulberry bush":      "Black Mulberry",
    "issai hardy kiwi":         "Issai Hardy Kiwi",
    "crandall black currant":   "Crandall Black Currant",
    # 2024 purchase additions
    "ashmead's kernel apple":   "Ashmead's Kernel Apple",
    "foxwhelp":                 "Foxwhelp Apple",
    "hewes virginia crab":      "Hewes Virginia Crab Apple",
    "harrison":                 "Harrison Apple",
    "tremblett's bitter":       "Tremblett's Bitter Apple",
    "redstreak":                "Redstreak Apple",
    "o'henry":                  "O'Henry Peach",
    "brown's cider":            "Brown's Cider Apple",
    "honan red":                "Honan Red Persimmon",
    "jenny fuzzy kiwi":         "Jenny Fuzzy Kiwi",
    "eversweet":                "Eversweet Pomegranate",
    "concord":                  "Concord Grape",
    "niagara":                  "Niagara Grape",
    "white doyenne":            "White Doyenne Pear",
    "beurre hardy":             "Beurre Hardy Pear",
}

# Type display overrides (catalog type -> label type)
TYPE_MAP = {
    "Elderberry/Feijoa": "Feijoa",
    "Nut Tree": "Walnut",
}


def load_catalog():
    """Load master_catalog.csv into a dict keyed by lowercase name."""
    catalog = {}
    with open(CATALOG_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            catalog[row["Name"].lower().strip()] = row
    return catalog


def lookup(catalog, name):
    """Find a variety in the catalog by exact then partial match."""
    key = name.lower().strip()
    if key in catalog:
        return catalog[key]
    for k, v in catalog.items():
        if key in k or k in key:
            return v
    return None


def generate():
    catalog = load_catalog()

    # Read inventory
    inventory = []
    with open(INVENTORY_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            inventory.append(row)

    labels = []
    unmatched = []

    for tree in inventory:
        cat_name = tree["Catalog_Name"].strip()
        year = tree["Year_Planted"].strip()
        match = lookup(catalog, cat_name)

        if match:
            label = {
                "Name": DISPLAY_NAMES.get(cat_name.lower(), cat_name),
                "Type": TYPE_MAP.get(match.get("Type", ""), match.get("Type", "")),
                "Bloom_Period": match.get("Bloom_Period", ""),
                "Harvest_Period": match.get("Harvest_Period", ""),
                "Fertility": match.get("Fertility", ""),
                "Use": match.get("Use", ""),
                "Origin": match.get("Origin", ""),
                "Year_Planted": year,
                "Footer": FOOTER,
            }
        else:
            unmatched.append(cat_name)
            label = {
                "Name": DISPLAY_NAMES.get(cat_name.lower(), cat_name),
                "Type": "",
                "Bloom_Period": "",
                "Harvest_Period": "",
                "Fertility": "",
                "Use": "",
                "Origin": "",
                "Year_Planted": year,
                "Footer": FOOTER,
            }

        # Apply overrides — always replace Origin, fill missing for others
        override_key = cat_name.lower().strip()
        if override_key in OVERRIDES:
            for field, val in OVERRIDES[override_key].items():
                if field == "Origin" or not label.get(field):
                    label[field] = val

        labels.append(label)

    # Write output
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    out_headers = ["Name", "Type", "Bloom_Period", "Harvest_Period",
                   "Fertility", "Use", "Origin", "Year_Planted", "Footer"]
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_headers)
        writer.writeheader()
        writer.writerows(labels)

    # ── Report ──
    print("Generated %d labels -> %s" % (len(labels), OUTPUT_PATH))
    print("  Source: %d rows from %s" % (len(inventory), INVENTORY_PATH))
    print("  Catalog: %d varieties in %s" % (len(catalog), CATALOG_PATH))
    if unmatched:
        print("\n  WARNING - %d unmatched (no catalog entry):" % len(unmatched))
        for u in unmatched:
            print("    - %s" % u)
    print()

    # Summary table
    fmt = "%-4s %-30s %-12s %-14s %-14s %-24s %s"
    print(fmt % ("ID", "Name", "Type", "Bloom", "Harvest", "Fertility", "Origin"))
    print("-" * 130)
    for tree, label in zip(inventory, labels):
        print(fmt % (
            tree["ID"],
            label["Name"][:30],
            label["Type"][:12],
            (label["Bloom_Period"] or "?")[:14],
            (label["Harvest_Period"] or "?")[:14],
            (label["Fertility"] or "?")[:24],
            (label["Origin"] or "?")[:30],
        ))

    # Type counts
    type_counts = {}
    for l in labels:
        t = l["Type"] or "Unknown"
        type_counts[t] = type_counts.get(t, 0) + 1
    print("\nLabels by type:")
    for t in sorted(type_counts):
        print("  %-15s %3d" % (t, type_counts[t]))
    print("  %-15s %3d" % ("TOTAL", len(labels)))

    # Data completeness check
    missing = []
    for i, l in enumerate(labels):
        for f in out_headers[:-1]:  # skip Footer
            if not l.get(f):
                missing.append("  Row %d (%s): %s" % (i + 1, l["Name"], f))
    if missing:
        print("\nWARNING - incomplete fields:")
        for m in missing:
            print(m)
    else:
        print("\nAll labels have complete data.")


if __name__ == "__main__":
    generate()
