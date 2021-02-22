import flask
import stonk_scraper
import os
import csv
import time, calendar
from helpers import *
from datetime import datetime
import pytz 
  
# get the standard UTC time  


@stonk_scraper.app.route("/stock/<ticker>/subs/")
def api_stock_subs(ticker, method='GET'):
    global stock_lookup_subs

    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    #@TODO add database

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
    
    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    res = cursor.execute("Select created from scans where type=? ORDER BY created DESC limit 1",["STREAM"])
    timeStamp = res.fetchone()["created"]
    print(timeStamp)
    p = '%Y-%m-%d %H:%M:%S'
    time_at_last_update = datetime.strptime(timeStamp, p).timestamp()
    print(time_at_last_update)
    if(time_at_last_update == 0):
        print("PANICK")
    print(calendar.timegm(time.gmtime()))
    UTC = pytz.utc 
    curr_time = datetime.now(UTC)
    print(curr_time)
    p = '%Y-%m-%d %H:%M:%S'
    #curr_time =  datetime.strptime(calendar.timegm(time.gmtime()), p).timestamp()
    print("Heck")
    time_since = (float(curr_time.strftime('%s')) - time_at_last_update)

    print(time_since)
    to_ret = {}

    to_ret["timeInMinutes"] = int(time_since/60)
    return flask.jsonify(to_ret)

@stonk_scraper.app.route("/stock/<ticker>")
def api_stock(ticker, method='GET'):
    global stock_lookup_hot
    global stock_lookup_top
    global names

    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    #@TODO add database
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
    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    #@TODO add database
    
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

    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    #global stock_lookup

    res1 = cursor.execute("SELECT m.ticker, m.numMentions, s.companyName  from mentions as m, stocks as s  where s.ticker=m.ticker AND m.subReddit=? and m.scan in (Select scanId from scans where type=? ORDER BY created DESC limit 1)",[subName, "STREAM"])
    res = res1.fetchall()
    
    data = res[0:10]
    print(data)
    '''
    if len(stream_data[subName]) > 10:
        data = stream_data[subName][0:10]
    else:
        data = stream_data[subName]
    print(data)
    '''
    for d in range(0, len(data)): 
        data[d] = [res[d]["ticker"], res[d]["numMentions"], res[d]["companyName"]]
    to_ret = {}
    to_ret["data"] = data
    
    return flask.jsonify(to_ret)

@stonk_scraper.app.route("/subs/<subName>/time/<timeInSeconds>")
def api_sub_time_data(subName,timeInSeconds, method='GET'):
    #TODO: Finish this function
    return "FINISH ME"


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