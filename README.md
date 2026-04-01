# 🌳 Farm Botanical Label System

Permanent laser-engraved metal labels for fruit trees and plants.

## Status: ✅ Labels Ready to Engrave

**53 labels** generated for 44 unique varieties (2025 purchase, planted 2026).

## Quick Start

1. **Read the full guide:** [`docs/PROJECT_GUIDE.md`](docs/PROJECT_GUIDE.md)
2. **Labels are ready:** `output/labels_batch.csv` — import into xTool Creative Space
3. **Design your template** in XCS (86mm × 54mm card, landscape layout)
4. **Batch import** the CSV and map columns to text fields
5. **Run a test card first** — see the test grid procedure in the guide
6. **Engrave all 53 labels**

## To Add Future Trees

1. Edit `data/generate_labels.py` — add entries to the `inventory` list
2. Run: `python3 data/generate_labels.py`
3. New `output/labels_batch.csv` will be generated

## Equipment

- **Engraver:** xTool M1 (5W or 10W diode module)
- **Material:** xTool Black Metal Business Cards (86mm × 54mm, anodized aluminum)
- **Software:** xTool Creative Space (XCS)

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
