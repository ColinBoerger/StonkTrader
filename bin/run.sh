#!/bin/bash
set -Eeuxo pipefail

# Set environment variables
export FLASK_DEBUG=True
export FLASK_APP=stonk_scraper
export STONK_SCRAPER_SETTINGS=config.py

# Run Flask dev server on port 8000.
flask run --host 127.0.0.1 --port 8001
