# 🌳 Botanical Label Engraving System

## Project Overview

A permanent botanical labeling system for Peter Brown & Robyn Seely's farm.
Labels are laser-engraved on **xTool Black Metal Business Cards (Anodized Aluminum)**
using an **xTool M1** laser engraver.

**Primary Data Source:** [Trees of Antiquity](https://www.treesofantiquity.com/collections)

---

## Project Phases

| Phase | Description | Status |
|-------|-------------|--------|
| **Phase 1** | Build Knowledge Base from Trees of Antiquity catalog | ✅ Complete — 427 varieties scraped |
| **Phase 2** | Inventory Management — populate & verify data | ✅ Complete — 44 varieties, 53 labels |
| **Phase 3** | CSV Generation for xTool Creative Space batch import | ✅ Complete — `output/labels_batch.csv` |
| **Phase 4** | Design Layout & M1 Laser Settings | ✅ Documented below |

---

## Phase 1: The Knowledge Base

### Trees of Antiquity — Collection Categories (20 found)

| # | Category | Type | Collection URL |
|---|----------|------|----------------|
| 1 | **Apple Trees** | Fruit Tree | [Link](https://www.treesofantiquity.com/collections/apple-trees) |
| 2 | **Apricot Trees** | Fruit Tree | [Link](https://www.treesofantiquity.com/collections/apricot-trees) |
| 3 | **Cherry Trees** | Fruit Tree | [Link](https://www.treesofantiquity.com/collections/cherry-trees) |
| 4 | **Fig Trees** | Fruit Tree | [Link](https://www.treesofantiquity.com/collections/fig-trees) |
| 5 | **Jujube Trees** | Fruit Tree | [Link](https://www.treesofantiquity.com/collections/jujube-trees) |
| 6 | **Mulberry Tree** | Fruit Tree | [Link](https://www.treesofantiquity.com/collections/mulberry-tree) |
| 7 | **Nectarine Tree** | Fruit Tree | [Link](https://www.treesofantiquity.com/collections/nectarine-tree) |
| 8 | **Pear Trees** | Fruit Tree | [Link](https://www.treesofantiquity.com/collections/pear-trees) |
| 9 | **Persimmon Trees** | Fruit Tree | [Link](https://www.treesofantiquity.com/collections/persimmon-trees) |
| 10 | **Plum Trees** | Fruit Tree | [Link](https://www.treesofantiquity.com/collections/plum-trees) |
| 11 | **Pluot Trees** | Fruit Tree | [Link](https://www.treesofantiquity.com/collections/pluots) |
| 12 | **Pomegranate Bush** | Fruit Bush | [Link](https://www.treesofantiquity.com/collections/pomegranate-bush) |
| 13 | **Quince Trees** | Fruit Tree | [Link](https://www.treesofantiquity.com/collections/quince-trees) |
| 14 | **Peach Trees** | Fruit Tree | [Link](https://www.treesofantiquity.com/collections/peach-trees) |
| 15 | **Grape Vines** | Vine | [Link](https://www.treesofantiquity.com/collections/grapes) |
| 16 | **Nut Trees** | Nut Tree | [Link](https://www.treesofantiquity.com/collections/nut-trees) |
| 17 | **Elderberries & Feijoa** | Fruit Bush | [Link](https://www.treesofantiquity.com/collections/smaller-1-year-fruit-trees) |
| 18 | **Medlar** | Fruit Tree | [Link](https://www.treesofantiquity.com/collections/medlar) |
| 19 | **Berries & Small Fruits** | Berry | [Link](https://www.treesofantiquity.com/collections/berries-small-fruit) |
| 20 | **Blueberries** | Berry | [Link](https://www.treesofantiquity.com/collections/assortment-small-berries) |

> **Note:** Gift Cards, Tree Starter Kits, and Bundle deals were excluded (not plant varieties).

---

## Phase 2: Inventory Management

### Data Architecture

The system uses **two separate files** with a join-based workflow:

```
master_catalog.csv  (REFERENCE — 427 varieties, read-only)
    └── Name, Type, Bloom_Period, Harvest_Period, Fertility, Use, Origin, Source_URL

my_trees.csv  (INVENTORY — one row per physical plant you own)
    └── ID, Catalog_Name, Year_Planted, Source, Location, Notes
              ↑
              joins to master_catalog.csv on Name

generate_labels.py  (GENERATOR — joins the two → labels_batch.csv)
    └── Reads my_trees.csv + master_catalog.csv → output/labels_batch.csv
```

**Why two files?** The catalog is a shared reference. Your inventory tracks individual
plants — you can own two of the same variety planted in different years and they each
get their own row and their own label.

### Label Data Schema (9 output fields per label)

| Field | Description | Example |
|-------|-------------|---------|
| **Name** | Variety name | Gravenstein |
| **Type** | Category (Apple, Pear, etc.) | Apple |
| **Bloom Period** | Flowering time | Mid-season |
| **Harvest Period** | When fruit is ready | Late August |
| **Fertility** | Pollination needs | Self-fertile / Needs pollinator |
| **Use** | Culinary purpose | Fresh eating, Cider, Cooking |
| **Origin** | Location and year of origin | Germany, 1600s |
| **Year Planted** | When you planted it | 2024 |
| **Footer** | Fixed text (same on all labels) | Planted by: Peter Brown & Robyn Seely |

### How to Add New Trees

1. **Open `data/my_trees.csv`** in Excel or Google Sheets
2. **Add a new row** for each physical plant:
   - `ID` — next sequential number
   - `Catalog_Name` — exact name from `master_catalog.csv` (this is the join key)
   - `Year_Planted` — when you planted it
   - `Source` — nursery name (e.g., "Trees of Antiquity")
   - `Location` — optional (row, zone, or area on your farm)
   - `Notes` — optional free text
3. **For non-ToA varieties:** Add the variety to `master_catalog.csv` first, then
   reference it by name in `my_trees.csv`
4. **Regenerate labels:** `python3 data/generate_labels.py`
5. The new `output/labels_batch.csv` will include all your trees

---

## Current Inventory Summary (2025 Purchase → 2026 Planting)

**44 unique varieties · 53 physical labels** (some varieties ×2)

| Type | Unique | Labels | Varieties |
|------|--------|--------|-----------|
| Apple | 13 | 13 | Bramley Seedling, Rhode Island Greening, Glockenapfel, Cox Orange Pippin, Winterstein, Dolgo Crab, Court Pendu Plat, Christmas Pink, Mountain Rose, Pink Parfait, Pink Pearl, Strawberry Parfait, Winekist |
| Cherry | 5 | 6 | Lapins, Black Tartarian(×2), Black Pearl, Stella, Van |
| Berry | 4 | 9 | Marionberry(×2), Loganberry(×2), Heritage Red Raspberry(×2), Fall Gold Raspberry(×2), Goji Berry |
| Blueberry | 3 | 6 | Sunshine(×2), Jersey(×2), Chandler(×2) |
| Walnut | 3 | 4 | Chandler(×2), Hartley, Manregion English |
| Peach | 3 | 3 | Frost, Baby Crawford, George IV |
| Nectarine | 3 | 3 | Independence, Goldmine, Snow Queen |
| Pomegranate | 2 | 2 | Kashmir, Grenada |
| Jujube | 2 | 2 | Shanxi, Sugarcane |
| Feijoa | 2 | 2 | Kakariki, Takaka |
| Apricot | 1 | 1 | Puget Gold |
| Fig | 1 | 1 | Peter's Honey |
| Mulberry | 1 | 1 | Black Pakistan |

> The "Pink & Red Fleshed Collective" bundle was expanded into its 6 individual
> apple varieties (Christmas Pink through Winekist) — each gets its own label.

---

## Phase 3: CSV for xTool Creative Space (XCS)

### How to Import into XCS Batch Processing

1. **Open xTool Creative Space (XCS)**
2. **Design your label template** (see Phase 4 layout guide)
3. Go to **Processing → Batch Processing** (or "Data Processing")
4. Click **Import CSV**
5. Select the generated `output/labels_batch.csv` file
6. **Map the CSV columns** to text fields in your design:
   - Each column header maps to a variable placeholder in your template
   - XCS will generate one label per row in the CSV
7. Preview the batch — verify all 9 fields render correctly
8. **Send to Device** to begin engraving

### CSV Format

The output CSV will have these exact headers:

```
Name,Type,Bloom_Period,Harvest_Period,Fertility,Use,Origin,Year_Planted,Footer
```

- One row = one physical metal label
- All text is pre-formatted and ready for direct engraving
- The `Footer` column will contain the fixed text on every row

---

## Phase 4: Design & Production

### Card Dimensions

- **Card size:** 86mm × 54mm (standard business card)
- **Safe margin:** 3mm from all edges
- **Printable area:** 80mm × 48mm

### Suggested Label Layout (Portrait Orientation Not Recommended — Use Landscape)

```
┌──────────────────────────────────────────────────────────┐
│  ┌─────────────────────────────────────────────────────┐ │
│  │           << VARIETY NAME >>                        │ │
│  │           (Large, bold, centered — 5-6mm tall)      │ │
│  ├─────────────────────────────────────────────────────┤ │
│  │  Type: Apple              Origin: New Jersey, 1817  │ │
│  ├─────────────────────────────────────────────────────┤ │
│  │  Bloom: Mid-season        Harvest: Late September   │ │
│  ├─────────────────────────────────────────────────────┤ │
│  │  Fertility: Self-fertile                            │ │
│  ├─────────────────────────────────────────────────────┤ │
│  │  Use: Fresh eating, Cider, Cooking                  │ │
│  ├─────────────────────────────────────────────────────┤ │
│  │  Year Planted: 2024                                 │ │
│  ├─────────────────────────────────────────────────────┤ │
│  │  Planted by: Peter Brown & Robyn Seely              │ │
│  │  (Small footer text, centered — 2-3mm tall)         │ │
│  └─────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

### Typography Recommendations for Legibility

| Element | Font Size | Weight | Alignment |
|---------|-----------|--------|-----------|
| Variety Name | 5–6mm (≈14-16pt) | Bold | Center |
| Field Labels | 2.5–3mm (≈7-8pt) | Regular | Left |
| Field Values | 2.5–3mm (≈7-8pt) | Bold | Left |
| Footer | 2–2.5mm (≈6-7pt) | Italic | Center |

### xTool M1 Laser Settings for Black Anodized Aluminum

Engraving on anodized aluminum removes the black anodic layer to reveal bright
white/silver aluminum underneath. This produces a high-contrast, permanent mark.

#### For the 10W Diode Laser Module

| Parameter | Recommended Setting | Notes |
|-----------|-------------------|-------|
| **Power** | 70–100% | Start at 80%, increase if mark is faint |
| **Speed** | 800–2000 mm/min | Lower speed = brighter/deeper mark |
| **Passes** | 1 | Single pass is usually sufficient |
| **Lines per cm (LPI)** | 300–355 | Higher = smoother fill, slower engrave |
| **Mode** | Line fill (default) | Standard raster engraving |
| **Focus** | Auto-focus or manual | Ensure card sits flat; use tape if needed |

**Recommended Starting Point (10W):** Power 80%, Speed 1000 mm/min, 1 pass, 300 LPI

#### For the 5W Diode Laser Module

| Parameter | Recommended Setting | Notes |
|-----------|-------------------|-------|
| **Power** | 100% | 5W needs full power for clean marks |
| **Speed** | 400–800 mm/min | Slower than 10W to compensate for lower power |
| **Passes** | 1–2 | May need 2 passes for bright white |
| **Lines per cm (LPI)** | 300–355 | Same resolution as 10W |
| **Mode** | Line fill (default) | Standard raster engraving |
| **Focus** | Auto-focus or manual | Same as above |

**Recommended Starting Point (5W):** Power 100%, Speed 600 mm/min, 1 pass, 300 LPI

#### Test Procedure (IMPORTANT — Do This First!)

1. **Create a test grid** in XCS with a matrix of settings:
   - Rows: Power levels (60%, 70%, 80%, 90%, 100%)
   - Columns: Speed levels (600, 800, 1000, 1500, 2000 mm/min)
2. Engrave the grid on a **spare black metal card**
3. Compare results under good lighting — look for:
   - ✅ Bright white mark with clean edges
   - ❌ Too faint (increase power or decrease speed)
   - ❌ Melting/warping edges (decrease power or increase speed)
4. Record your optimal settings and use them for all labels

#### Material Handling Tips

- **Clean cards** with isopropyl alcohol before engraving
- **Secure cards** with painter's tape or the xTool card jig
- Cards may curl slightly from heat — press flat under a book while cooling
- **Do not use air assist** at full blast — gentle air flow only (prevents debris scatter)
- After engraving, gently wipe with a soft cloth to remove dust/residue

---

## File Structure

```
Trees/
├── README.md                         ← Quick-start summary
├── data/
│   ├── master_catalog.csv            ← Reference: 427 ToA varieties (botanical data only)
│   ├── my_trees.csv                  ← Inventory: your physical plants (1 row = 1 plant)
│   ├── inventory_template.csv        ← Blank template (for reference)
│   ├── scrape_catalog.py             ← Scraper: refreshes master_catalog.csv from ToA
│   └── generate_labels.py            ← Generator: joins my_trees + catalog → labels CSV
├── output/
│   └── labels_batch.csv              ← ✅ 53 labels ready for XCS batch import
└── docs/
    └── PROJECT_GUIDE.md              ← This file (full instructions)
```

### Workflow to Generate Labels

**For the 2025/2026 inventory, labels are already generated.** To engrave:

1. Open **xTool Creative Space (XCS)**
2. Design your label template matching the layout above (86mm × 54mm)
3. Go to **Processing → Batch Processing**
4. Import `output/labels_batch.csv`
5. Map each CSV column to its corresponding text field in your template
6. Preview all 53 labels, then **Send to Device**

**To add future trees or regenerate labels:**

1. Edit `data/my_trees.csv` — add one row per new physical plant
   (use the catalog name as `Catalog_Name` to join against `master_catalog.csv`)
2. Run: `python3 data/generate_labels.py`
3. New `output/labels_batch.csv` will be created with all your trees

---

## Security Notes

- No credentials, API keys, or personal data beyond names are stored
- All data is local to this machine — nothing is sent to third-party services
- The CSV output contains only botanical and label data
- Source data is publicly available from treesofantiquity.com

---

## Quick Reference

- **xTool Creative Space:** https://www.xtool.com/pages/software
- **Trees of Antiquity:** https://www.treesofantiquity.com/collections
- **Card Specs:** 86mm × 54mm, black anodized aluminum
- **Engraver:** xTool M1 (5W or 10W diode laser)
