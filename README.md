# 🌳 Farm Botanical Label System

Permanent laser-engraved metal labels for fruit trees and plants.

## Status: ✅ Labels Ready to Engrave

**93 labels** generated across 3 planting years (2024–2026).

## Quick Start

1. **Read the full guide:** [`docs/PROJECT_GUIDE.md`](docs/PROJECT_GUIDE.md)
2. **Labels are ready:** `output/labels_batch.csv` and `output/svg/` — import into xTool Creative Space
3. Follow the **XCS Batch Engraving Workflow** below
4. **Run a test card first** — see the test grid procedure in the full guide

## To Add Future Trees

1. Add rows to `data/my_trees.csv` (one row per physical plant)
2. Run: `python3 data/generate_labels.py`
3. Run: `python3 data/generate_svgs.py`
4. New `output/labels_batch.csv` and `output/svg/` files will be generated

## Equipment

- **Engraver:** xTool M1 (5W or 10W diode module)
- **Material:** xTool Black Metal Business Cards (86mm × 54mm, anodized aluminum)
- **Software:** [xTool Creative Space (XCS)](https://www.xtool.com/pages/software)

## Label Fields

| Field | Example |
|-------|---------|
| Name | Gravenstein |
| Type | Apple |
| Bloom Period | Mid-season |
| Harvest Period | Late August |
| Fertility | Needs pollinator |
| Use | Fresh eating, Cider |
| Origin | Denmark, 1600s |
| Year Planted | 2024 |
| Footer | Planted by: Peter Brown & Robyn Seely |

---

## XCS Batch Engraving Workflow

This is the step-by-step process to go from `labels_batch.csv` to engraved cards.

### Step 1: Create the Label Template in XCS

1. Open **xTool Creative Space (XCS)**
2. Set the canvas/work area to **86mm × 54mm** (landscape)
3. Add **9 text elements** to the canvas — one for each label field
4. Arrange them following this layout:

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│              << VARIETY NAME >>                           │
│                  (Type)                                   │
│                                                          │
│ ──────────────────────────────────────────────────────── │
│                                                          │
│               Bloom: __________                          │
│              Harvest: __________                         │
│            Fertility: __________                         │
│                 Use: __________                          │
│              Origin: __________                          │
│                                                          │
│ ──────────────────────────────────────────────────────── │
│                                                          │
│              Planted: 2026                               │
│    Planted by: Peter Brown & Robyn Seely                 │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Typography:**

| Element | Font Size | Style | Alignment |
|---------|-----------|-------|-----------|
| Variety Name | 4.5mm (~13pt) | Bold | Center |
| Type | 3.2mm (~9pt) | Italic | Center |
| Detail fields | 2.8mm (~8pt) | Regular | Center |
| Planted year | 2.8mm (~8pt) | Bold | Center |
| Footer | 2.5mm (~7pt) | Regular | Center |

### Step 2: Enable Batch Processing & Import CSV

1. In XCS, go to **Top menu → Processing → Batch Processing**
   (may also appear as "Variable Data" or "Data Processing" depending on XCS version)
2. Click **Import CSV** (or **Import Data**)
3. Select `output/labels_batch.csv`
4. XCS will show the CSV columns: `Name, Type, Bloom_Period, Harvest_Period,
   Fertility, Use, Origin, Year_Planted, Footer`

### Step 3: Map CSV Columns to Text Elements

1. **Click each text element** on the canvas
2. In the properties panel, find the **Variable/Data binding** option
3. **Bind each text element to its matching CSV column:**

   | Canvas Text Element | Bind To CSV Column |
   |--------------------|--------------------|
   | Variety name (large) | `Name` |
   | Type field | `Type` |
   | Bloom field | `Bloom_Period` |
   | Harvest field | `Harvest_Period` |
   | Fertility field | `Fertility` |
   | Use field | `Use` |
   | Origin field | `Origin` |
   | Year planted field | `Year_Planted` |
   | Footer text | `Footer` |

4. For **field labels** like "Type:", "Bloom:", etc. — these are static text
   on the template. Only the **values** are bound to CSV columns.
   Use XCS text concatenation or place two text boxes side by side:
   - Static: `"Type: "` (not bound)
   - Variable: bound to `Type` column

### Step 4: Preview & Verify

1. XCS will show a **preview of each label** (93 total)
2. Use the **navigation arrows** to scroll through all labels
3. Check that:
   - Text fits within the card boundaries (no clipping)
   - Font sizes are legible
   - Long variety names like "Rhode Island Greening Apple" don't overflow
4. If text overflows, reduce font size or abbreviate field labels

### Step 5: Configure Laser Settings

Set the **engraving parameters** for all text elements:

**10W Module (recommended):**
| Setting | Value |
|---------|-------|
| Power | 80% |
| Speed | 1000 mm/min |
| Passes | 1 |
| Lines per cm | 300 LPI |

**5W Module:**
| Setting | Value |
|---------|-------|
| Power | 100% |
| Speed | 600 mm/min |
| Passes | 1 |
| Lines per cm | 300 LPI |

> ⚠️ **Run a test card first!** Engrave one label on a spare card to verify
> settings produce a bright white mark before committing to all 93 cards.

### Step 6: Engrave

1. Clean card with isopropyl alcohol
2. Place card in xTool M1 — secure with painter's tape or card jig
3. **Focus the laser** (auto-focus or manual)
4. Click **Start** / **Send to Device**
5. For batch mode: XCS will prompt you to swap cards between each label
6. After engraving, wipe gently with a soft cloth to remove dust

### Tips

- **Save your XCS template** — you can re-import a new CSV anytime
  without rebuilding the layout
- Cards may curl slightly from heat — press flat under a book while cooling
- Do **not** use air assist at full blast (prevents debris scatter on small cards)
- Process cards in batches of 10-15 to manage workflow

---

## File Structure

```
FarmInventory/
├── README.md                      ← This file
├── data/
│   ├── master_catalog.csv         ← 432 variety reference (botanical data)
│   ├── my_trees.csv               ← Your inventory (1 row = 1 plant)
│   ├── generate_labels.py         ← Joins inventory + catalog → labels CSV
│   ├── generate_svgs.py           ← Generates individual SVG files per label
│   ├── scrape_catalog.py          ← Refreshes catalog from Trees of Antiquity
│   └── inventory_template.csv     ← Blank template for reference
├── output/
│   ├── labels_batch.csv           ← 93 labels ready for XCS (CSV)
│   └── svg/                       ← 93 individual SVG files (one per card)
└── docs/
    └── PROJECT_GUIDE.md           ← Full documentation
```

### SVG Workflow (Alternative to CSV Batch)

If XCS does not support CSV batch import, use the individual SVG files:

1. Open any SVG from `output/svg/` in XCS (e.g., `001_Chandler_Walnut.svg`)
2. Each file is pre-sized to 86mm × 54mm — the exact card dimensions
3. All text is centered with appropriate font sizes
4. Set laser settings (see above), engrave, then open the next SVG

---

## Using This Codebase for Your Own Inventory

You can fork or clone this repo and adapt it for your own farm or garden. Here's how:

### Prerequisites

- **Python 3.6+** (no external packages required — stdlib only)
- **xTool Creative Space (XCS)** for engraving
- **xTool M1** (or compatible laser engraver)
- **Black anodized aluminum business cards** (86mm × 54mm)

### Step 1: Clone the Repository

```bash
git clone https://github.com/PeterBrownUSA/FarmInventory.git
cd FarmInventory
```

### Step 2: Customize the Footer

Edit `data/generate_labels.py` and change the `FOOTER` constant (line 23):

```python
FOOTER = "Planted by: Your Name Here"
```

### Step 3: Refresh the Catalog (Optional)

The included `data/master_catalog.csv` contains 432 varieties from [Trees of Antiquity](https://www.treesofantiquity.com). To refresh it:

```bash
python3 data/scrape_catalog.py
```

This re-scrapes all collections via the Shopify JSON API and overwrites `data/master_catalog.csv`. No API key is required.

If your trees come from a different nursery, you can replace `master_catalog.csv` entirely. Just keep the same column headers:

```
Name,Type,Bloom_Period,Harvest_Period,Fertility,Use,Origin,Source_URL
```

### Step 4: Build Your Inventory

Edit `data/my_trees.csv` — add one row per physical plant you own:

```csv
ID,Catalog_Name,Year_Planted,Source,Location,Notes
1,Gravenstein,2024,Trees of Antiquity,Orchard Row A,
2,Gravenstein,2025,Trees of Antiquity,Orchard Row B,Second tree
3,Bartlett Pear,2024,Local nursery,,Gift from neighbor
```

| Column | Description |
|--------|-------------|
| `ID` | Unique number (sequential) |
| `Catalog_Name` | Must match a `Name` in `master_catalog.csv` (partial match supported) |
| `Year_Planted` | Year the tree went in the ground |
| `Source` | Where you purchased it |
| `Location` | Optional — where on your property |
| `Notes` | Optional — any notes |

> **Tip:** You can have multiple rows for the same variety (e.g., two Gravenstein trees planted in different years). Each row produces its own label.

### Step 5: Add Custom Varieties

If you own trees **not** in the catalog, you have two options:

**Option A:** Add the variety directly to `data/master_catalog.csv`:
```csv
My Local Apple,Apple,Midseason,Late,Self-fertile,Fresh eating,Oregon 1990s,
```

**Option B:** Add an override in `data/generate_labels.py` in the `OVERRIDES` dict:
```python
OVERRIDES = {
    "my local apple": {"Origin": "Oregon, 1990s", "Bloom_Period": "Midseason"},
    ...
}
```

Overrides always take precedence for the `Origin` field and fill in any missing fields from the catalog.

### Step 6: Generate Labels

```bash
# Generate the CSV (used for XCS batch import)
python3 data/generate_labels.py

# Generate individual SVG files (one per card)
python3 data/generate_svgs.py
```

Output:
- `output/labels_batch.csv` — all labels in CSV format
- `output/svg/` — one SVG file per label (86mm × 54mm each)

### Step 7: Engrave

Open the SVG files in xTool Creative Space and engrave using the laser settings documented above. See the **XCS Batch Engraving Workflow** section for full details.

### Customizing the SVG Layout

To adjust fonts, spacing, or layout, edit `data/generate_svgs.py`. Key variables at the top of the file:

```python
CARD_W = 86        # Card width in mm
CARD_H = 54        # Card height in mm
MARGIN = 3         # Margin from edges in mm
FONT_NAME = 4.5    # Variety name font size (mm)
FONT_TYPE = 3.2    # Type line font size (mm)
FONT_DETAIL = 2.8  # Detail fields font size (mm)
FONT_FOOTER = 2.5  # Footer font size (mm)
```

The `LAYOUT` dict controls vertical positioning (Y coordinates in mm from top). Adjust these to rebalance spacing between fields.

### 💡 Tip: Automate with GitHub Copilot CLI

If you're using [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli), you can skip the manual inventory entry entirely. Simply paste your nursery order receipt (email confirmation, invoice text, or screenshot text) into a Copilot CLI session and ask it to:

1. **Parse the receipt** — extract variety names, quantities, and purchase year
2. **Match against the catalog** — look up each variety in `master_catalog.csv` and resolve name differences
3. **Expand bundles** — identify collection/bundle products and break them into individual varieties
4. **Research missing data** — for varieties not in the catalog, look up botanical details (bloom period, origin, fertility, etc.)
5. **Populate `my_trees.csv`** — append new rows with correct IDs, catalog names, and planting year
6. **Regenerate labels** — run both generation scripts automatically

Example prompt:
```
Here are the trees I purchased in 2025 and planted in 2026:

  Bramley Seedling × 1  $56.95
  Lapins Cherry × 2     $52.95/ea
  Orchard Starter Bundle × 1  $235.95

Please add these to my_trees.csv, match them against the catalog,
expand any bundles, and regenerate the labels.
```

This is how the original inventory for this project was built — three years of purchase receipts were processed in a single session.
