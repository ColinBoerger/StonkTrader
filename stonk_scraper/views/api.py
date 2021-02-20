import flask
import stonk_scraper
import os
import csv
import time
from helpers import *


@stonk_scraper.app.route("/stock/<ticker>/subs/")
def api_stock_subs(ticker, method='GET'):
	global stock_lookup_subs

	to_ret = {}
	to_ret["hot"] = []
	to_ret["top"] = [] 
	ticker = ticker.upper()
	for sub in stock_lookup_subs["top"]:
		mentions = 0
		if ticker in stock_lookup_subs["top"][sub].keys():
			mentions = stock_lookup_subs["top"][sub][ticker]
		to_ret["top"] += [[sub, str(mentions)]]
	for sub in stock_lookup_subs["hot"]:
		mentions = 0
		if ticker in stock_lookup_subs["hot"][sub].keys():
			mentions = stock_lookup_subs["hot"][sub][ticker]
		to_ret["hot"] += [[sub, str(mentions)]]

	return flask.jsonify(to_ret)

@stonk_scraper.app.route("/lastUpdate")
def api_time_since_update(method="GET"):
    global time_at_last_update
    
    if(time_at_last_update == 0):
        print("PANICK")
    print(time_at_last_update)
    time_since = time.time() - time_at_last_update
    print(time_since)
    to_ret = {}

    to_ret["timeInMinutes"] = int(time_since/60)
    return flask.jsonify(to_ret)

@stonk_scraper.app.route("/stock/<ticker>")
def api_stock(ticker, method='GET'):
	global stock_lookup_hot
	global stock_lookup_top
	global names

	if len(names.keys()) < 1:
		getNames("tickers.csv")
	to_ret = {}
	ticker = ticker.upper()
	if ticker in stock_lookup_hot.keys():
		to_ret[ticker + "hot"] = stock_lookup_hot[ticker]
		to_ret["name"] = names[ticker]

	else: 
		#print(names)
		print(stock_lookup_hot)
		to_ret[ticker + "hot"] = 0
		if ticker in names.keys():
			to_ret["name"] = names[ticker]
		else:
			to_ret["name"] = "No name known"
	if ticker in stock_lookup_top.keys():
		to_ret[ticker + "top"] = stock_lookup_top[ticker]
	else: 
		to_ret[ticker + "top"] = 0
	return flask.jsonify(to_ret)

@stonk_scraper.app.route("/stock/supportedSubs/")
def api_supported_subs(method='GET'):
	global time_at_last_update
	print("Time right before")
	print(time_at_last_update)
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

@stonk_scraper.app.route("/subs/<subName>/time/<timeInSeconds>")
def api_sub_time_data(subName,timeInSeconds, method='GET'):
	#TODO: Finish this function
	try:
		files = os.listdir("stonk_scraper/static/stock_data/streamData/" + subName)
	except Exception as e:
		to_ret = {}
		to_ret["Error"] = "Unsuppotred sub reddit" 


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