# Contributing to Farm Botanical Label System

Thank you for your interest in contributing! This project helps farmers and
gardeners create permanent laser-engraved metal labels for their plants.

## How to Contribute

### Reporting Bugs

1. Check [existing issues](https://github.com/PeterBrownUSA/FarmInventory/issues) first
2. Open a new issue using the **Bug Report** template
3. Include: Python version, OS, steps to reproduce, expected vs actual behavior

### Suggesting Features

1. Open a new issue using the **Feature Request** template
2. Describe the use case and how it would help your workflow

### Submitting Code Changes

1. **Fork** the repository
2. **Create a branch** for your change: `git checkout -b feature/your-feature-name`
3. **Make your changes** — follow the existing code style
4. **Test your changes:**
   ```bash
   python3 data/generate_labels.py
   python3 data/generate_svgs.py
   ```
5. **Commit** with a clear message describing what and why
6. **Open a Pull Request** against `main`

### Adding New Varieties to the Catalog

If you've found varieties missing from the Trees of Antiquity catalog:

1. Add the variety to `data/master_catalog.csv` with all 8 columns filled
2. If botanical data needs correction, add an entry to the `OVERRIDES` dict
   in `data/generate_labels.py`
3. Test by adding a sample row to `data/my_trees.csv` and regenerating labels

### Improving Botanical Data

We welcome corrections to bloom periods, origins, fertility info, etc.
Please cite your source (nursery catalog, pomological reference, etc.)
in the PR description.

## Code Style

- Python 3.6+ compatible (stdlib only — no external packages)
- Use docstrings for all functions
- Comment non-obvious logic
- Keep the existing file structure

## Questions?

Open an issue or start a discussion on the repository. We're happy to help!
