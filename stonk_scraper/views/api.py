import flask
import stonk_scraper
from helpers import *

@stonk_scraper.app.route("/stock/<ticker>")

def api_stock(ticker, method='GET'):
	global stock_lookup
	to_ret = {}
	ticker = ticker.upper()
	if ticker in stock_lookup.keys():
		to_ret[ticker] = stock_lookup[ticker]
	else: 
		to_ret["error"] = "ticker not supported"
	return flask.jsonify(to_ret)
