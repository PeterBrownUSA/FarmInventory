# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2026-04-01

### Added

- **Catalog scraper** (`scrape_catalog.py`) — fetches 432 varieties from Trees of Antiquity via Shopify JSON API
- **Label generator** (`generate_labels.py`) — joins inventory + catalog to produce label CSV with 9 fields per label
- **SVG generator** (`generate_svgs.py`) — creates individual 86mm × 54mm SVG files for xTool Creative Space
- **Personal inventory** (`my_trees.csv`) — 93 plants across 3 planting years (2024, 2025, 2026)
- **Master catalog** (`master_catalog.csv`) — 432 heirloom varieties with botanical data
- **Project documentation** (`PROJECT_GUIDE.md`) — full guide including laser settings, layout, and test procedures
- **README** with XCS batch workflow, SVG workflow, and "use for your own inventory" guide
- Origin data standardized to "Location, Year" format for all 93 labels
- Use field auto-abbreviation for labels exceeding card width
- Bundle expansion for 3 collection products (Pink & Red Fleshed, Orchard Starter, Cider Tree Blend)
- Manual overrides system for correcting/enriching incomplete catalog data
- Flexible name matching (exact + partial/substring) for catalog lookups
- Comprehensive code documentation with docstrings and inline comments
