"""
Fake Passports package initializer.
Referenced from EECS 485 setup for Python/flask.
Jason Kim, Fall 2019
"""

import flask

import helpers



app = flask.Flask(__name__)
# Read settings from config module
app.config.from_object('stonk_scraper.config')
# Overlay settings read from file specified by environment variable.
app.config.from_envvar('STONK_SCRAPER_SETTINGS', silent=True)
# Tell the app about our server-side functions.
import stonk_scraper.views
import stonk_scraper.model 