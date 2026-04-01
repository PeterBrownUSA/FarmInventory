# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest `main` branch | ✅ |

## Reporting a Vulnerability

This project is a local-only tool for generating laser engraving labels.
It does not run a server, handle authentication, or process sensitive user data.

However, if you discover a security issue (e.g., in the web scraper or file
handling), please report it responsibly:

1. **Do not** open a public issue for security vulnerabilities
2. **Email** the maintainer directly (contact info on the repository profile)
3. Include a description of the vulnerability and steps to reproduce

You can expect an initial response within 7 days.

## Scope

The following components are in scope:

- `data/scrape_catalog.py` — Makes HTTP requests to external URLs
- `data/generate_labels.py` — Reads/writes CSV files
- `data/generate_svgs.py` — Generates SVG/XML files from user data

## Known Considerations

- The scraper (`scrape_catalog.py`) makes unauthenticated HTTP requests to
  the Trees of Antiquity Shopify store. It does not transmit any user data.
- SVG generation uses `html.escape()` to prevent XML injection from
  catalog data.
- All file operations are local — no data is sent to external services.
