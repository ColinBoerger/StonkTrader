import flask
import stonk_scraper
import os
import csv
from helpers import stock_lookup, names, stream_data

@stonk_scraper.app.route("/stock/<ticker>")
def api_stock(ticker, method='GET'):
	global stock_lookup
	global names
	if len(names.keys()) < 1:
		getNames("tickers.csv")
	to_ret = {}
	ticker = ticker.upper()
	if ticker in stock_lookup.keys():
		to_ret[ticker] = stock_lookup[ticker]
		to_ret["name"] = names[ticker]

	else: 
		#print(names)
		print(stock_lookup)
		to_ret[ticker] = 0
		if ticker in names.keys():
			to_ret["name"] = names[ticker]
		else:
			to_ret["name"] = "No name known"
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
	global names
	if len(names.keys()) < 1:
		getNames("tickers.csv")
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
	print(data)
	for d in range(0, len(data)): 
		data[d] = [data[d][0], data[d][1], names[data[d][0]]]
	to_ret = {}
	to_ret["data"] = data
	print(data)
	
	return flask.jsonify(to_ret)

def getNames(csvFileName):
    global names
    names = {}
    with open(csvFileName) as csv_file:
        print("Heck")
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            line_count += 1
            names[row[0]] = row[1]