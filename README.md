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
│            << VARIETY NAME >>                            │
│            (Large, bold, centered — 5-6mm)               │
│                                                          │
│   Type: _______________    Origin: __________________    │
│                                                          │
│   Bloom: ______________    Harvest: _________________    │
│                                                          │
│   Fertility: ________________________________________    │
│                                                          │
│   Use: ______________________________________________    │
│                                                          │
│   Year Planted: _____                                    │
│                                                          │
│            Planted by: Peter Brown & Robyn Seely           │
│            (Small, centered — 2-2.5mm)                   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Typography recommendations:**

| Element | Font Size | Alignment |
|---------|-----------|-----------|
| Variety Name | 5–6mm (~14-16pt) Bold | Center |
| Field labels + values | 2.5–3mm (~7-8pt) | Left |
| Footer | 2–2.5mm (~6-7pt) Italic | Center |

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
