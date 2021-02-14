"""
Let our app know of views for each page.
Referenced from EECS 485's setup for Python/flask.
Colin Boerger
"""

import stonk_scraper
import helpers
from stonk_scraper.views.index import show_index


from stonk_scraper.views.api import api_stock
