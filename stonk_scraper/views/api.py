import flask
import stonk_scraper
import os
from helpers import *

@stonk_scraper.app.route("/stock/<ticker>")

def api_stock(ticker, method='GET'):
	global stock_lookup
	to_ret = {}
	ticker = ticker.upper()
	if ticker in stock_lookup.keys():
		to_ret[ticker] = stock_lookup[ticker]
	else: 
		to_ret[ticker] = 0
	return flask.jsonify(to_ret)

@stonk_scraper.app.route("/stock/supportedSubs/")
def api_supported_subs(method='GET'):
	files = os.listdir("stonk_scraper/static/stock_data/streamData")
	to_ret = {}
	to_ret["supportedSubs"] =  files
	return flask.jsonify(to_ret)

@stonk_scraper.app.route("/subs/<subName>")
def api_sub_data(subName, method='GET'):
	global stream_data
	#global stock_lookup

	try:
		files = os.listdir("stonk_scraper/static/stock_data/streamData/" + subName)
	except Exception as e:
		to_ret = {}
		to_ret["Error"] = "Unsuppotred sub reddit" 
	data = []
	if len(stream_data[subName]) > 10:
		data = stream_data[subName][0:10]
	else:
		data = stream_data[subName]
	to_ret = {}
	to_ret["data"] = data
	
	return flask.jsonify(to_ret)
