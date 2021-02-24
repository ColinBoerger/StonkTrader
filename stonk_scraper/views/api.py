import flask
import stonk_scraper
import os
import csv
import time, calendar
from helpers import *
from datetime import datetime, timedelta
import pytz 
  
# get the standard UTC time  


@stonk_scraper.app.route("/stock/<ticker>/subs/")
def api_stock_subs(ticker, method='GET'):

    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    #@TODO add database
    resHot = cursor.execute("SELECT * from mentions as m where m.ticker = ? and m.scan in (Select scanId from scans where type=? ORDER BY created DESC limit 1)", [ticker, "MULTI-HOT"])
    resHot = resHot.fetchall()
    

    cursor = database.cursor()
    resTop = cursor.execute("SELECT * from mentions as m where m.ticker = ? and m.scan in (Select scanId from scans where type=? ORDER BY created DESC limit 1)", [ticker, "MULTI-TOP"])
    resTop = resTop.fetchall()
    
    #database.close()
    to_ret = {}
    to_ret["hot"] = []
    to_ret["top"] = [] 
    for i in range(0, len(resHot)):
        to_ret["hot"] += [[resHot[i]["subReddit"], resHot[i]["numMentions"]]]
    for i in range(0, len(resTop)):
        to_ret["top"] += [[resTop[i]["subReddit"], resTop[i]["numMentions"]]]

    return flask.jsonify(to_ret)

@stonk_scraper.app.route("/lastUpdate")
def api_time_since_update(method="GET"):
    
    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    res = cursor.execute("SELECT created from scans where type=? ORDER BY created DESC limit 1",["STREAM"])
    timeStamp = res.fetchone()["created"]
    
    p = '%Y-%m-%d %H:%M:%S'
    time_at_last_update = datetime.strptime(timeStamp, p).timestamp()

    UTC = pytz.utc 
    curr_time = datetime.now(UTC)

    time_since = (float(curr_time.strftime('%s')) - time_at_last_update)

    to_ret = {}

    to_ret["timeInMinutes"] = int(time_since/60)
    return flask.jsonify(to_ret)

@stonk_scraper.app.route("/stock/<ticker>")
def api_stock(ticker, method='GET'):
    to_ret = {}
    ticker = ticker.upper()
    
    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    cursor.execute("SELECT m.numMentions, m.ticker, st.companyName from stocks as st, mentions as m where m.ticker = ? and m.ticker = st.ticker and m.scan in (Select scanId from scans where type=? ORDER BY created DESC limit 1)", [ticker, "HOT"])
    res = cursor.fetchone()
    if res == None:
        to_ret[ticker + "hot"] = 0
        to_ret["name"] = "Not supported"
        to_ret[ticker + "top"] = "Not supported"
        #database.close()
        return flask.jsonify(to_ret)
    
    to_ret[ticker + "hot"] = res["numMentions"]
    to_ret["name"] = res["companyName"]
    cursor = database.cursor()
    
    cursor.execute("SELECT m.numMentions, m.ticker, st.companyName from stocks as st, mentions as m where m.ticker = ? and m.ticker = st.ticker and m.scan in (Select scanId from scans where type=? ORDER BY created DESC limit 1)", [ticker, "TOP"])
    res = cursor.fetchone()
    to_ret[ticker + "top"] = res["numMentions"]
    #database.close()
    return flask.jsonify(to_ret)

@stonk_scraper.app.route("/stock/<ticker>/time/<timeInSeconds>")
def api_stock(ticker, timeInSeconds method='GET'):
    to_ret = {}
    ticker = ticker.upper()
    
    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    cursor.execute("SELECT m.numMentions, m.ticker, st.companyName from stocks as st, mentions as m where m.ticker = ? and m.ticker = st.ticker and m.scan in (Select scanId from scans where type=? ORDER BY created DESC limit 1)", [ticker, "HOT"])
    res = cursor.fetchone()
    if res == None:
        to_ret[ticker + "hot"] = 0
        to_ret["name"] = "Not supported"
        to_ret[ticker + "top"] = "Not supported"
        #database.close()
        return flask.jsonify(to_ret)
    
    to_ret[ticker + "hot"] = res["numMentions"]
    to_ret["name"] = res["companyName"]
    cursor = database.cursor()
    
    cursor.execute("SELECT m.numMentions, m.ticker, st.companyName from stocks as st, mentions as m where m.ticker = ? and m.ticker = st.ticker and m.scan in (Select scanId from scans where type=? ORDER BY created DESC limit 1)", [ticker, "TOP"])
    res = cursor.fetchone()
    to_ret[ticker + "top"] = res["numMentions"]
    #database.close()
    return flask.jsonify(to_ret)

@stonk_scraper.app.route("/stock/supportedSubs/")
def api_supported_subs(method='GET'):
    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    
    cursor.execute("SELECT DISTINCT subReddit from mentions")
    res = cursor.fetchall()
    to_ret = {}
    subs = []
    for r in res:
        if r["subReddit"] != None:
            subs += [r["subReddit"]]
    to_ret["supportedSubs"] =  subs
    #database.close()
    return flask.jsonify(to_ret)

@stonk_scraper.app.route("/subs/<subName>")
def api_sub_data(subName, method='GET'):   

    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    

    res1 = cursor.execute("SELECT m.ticker, m.numMentions, s.companyName  from mentions as m, stocks as s  where s.ticker=m.ticker AND m.subReddit=? and m.scan in (Select scanId from scans where type=? ORDER BY created DESC limit 1)",[subName, "STREAM"])
    res = res1.fetchall()
    #@TODO error checking if sub isn't supported
    data = res[0:10]

    for d in range(0, len(data)): 
        data[d] = [res[d]["ticker"], res[d]["numMentions"], res[d]["companyName"]]
    to_ret = {}
    to_ret["data"] = data
    ##database.close()
    return flask.jsonify(to_ret)

@stonk_scraper.app.route("/subs/<subName>/time/<timeInSeconds>")
def api_sub_time_data(subName,timeInSeconds, method='GET'):
    #TODO: Returns the data mentions from the stream
    UTC = pytz.utc 
    time_offset_seconds = 0
    try:
        time_offset_seconds = int(timeInSeconds)
    except Exception as e:
        return "Finish Me"
    curr_time = datetime.now(UTC) - timedelta(seconds=int(timeInSeconds))
    print(curr_time)

    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    subName = subName.lower()

    res1 = cursor.execute("SELECT *  from scans  where type=? AND created >= ?",["STREAM",curr_time])
    res = res1.fetchall()
    #print(res)
    #print(subName)
    mentions = cursor.execute("SELECT * from mentions where subReddit=? and scan in (SELECT scanId from scans where type=? AND created >= ?)",[subName,"STREAM", curr_time])
    mentions = mentions.fetchall()
    print(mentions)
    results = {}
    for mention in mentions:
        scan = mention["scan"]
        ticker = mention["ticker"] 
        numMentions = mention["numMentions"]
        if scan not in results.keys():
            results[scan] = {}
        if numMentions != 0:
            results[scan][ticker] = numMentions
        #TODO: Add a timestamp for the scan
    #database.close()
    return flask.jsonify(results)

@stonk_scraper.app.route("/subs/<subName>/time/<timeInSeconds>/hot")
def api_hot_sub_time_data(subName,timeInSeconds, method='GET'):
    #TODO: Returns the data mentions from the stream
    UTC = pytz.utc 
    time_offset_seconds = 0
    try:
        time_offset_seconds = int(timeInSeconds)
    except Exception as e:
        return "Finish Me"
    curr_time = datetime.now(UTC) - timedelta(seconds=int(timeInSeconds))
    print(curr_time)

    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    
    subName = subName.lower()

    res1 = cursor.execute("SELECT *  from scans  where type=? AND created >= ?",["STREAM",curr_time])
    res = res1.fetchall()
    #print(res)
    #print(subName)
    mentions = cursor.execute("SELECT * from mentions where subReddit=? and scan in (SELECT scanId from scans where type=? AND created >= ?)",[subName,"MULTI-HOT", curr_time])
    mentions = mentions.fetchall()
    print(mentions)
    results = {}
    for mention in mentions:
        scan = mention["scan"]
        ticker = mention["ticker"] 
        numMentions = mention["numMentions"]
        if scan not in results.keys():
            results[scan] = {}
        if numMentions != 0:
            results[scan][ticker] = numMentions
        #TODO: Add a timestamp for the scan
    #database.close()
    return flask.jsonify(results)

@stonk_scraper.app.route("/subs/<subName>/time/<timeInSeconds>/top")
def api_hot_sub_time_data(subName,timeInSeconds, method='GET'):
    #TODO: Returns the data mentions from the stream
    UTC = pytz.utc 
    time_offset_seconds = 0
    try:
        time_offset_seconds = int(timeInSeconds)
    except Exception as e:
        return "Finish Me"
    curr_time = datetime.now(UTC) - timedelta(seconds=int(timeInSeconds))
    print(curr_time)

    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    
    subName = subName.lower()

    res1 = cursor.execute("SELECT *  from scans  where type=? AND created >= ?",["STREAM",curr_time])
    res = res1.fetchall()
    #print(res)
    #print(subName)
    mentions = cursor.execute("SELECT * from mentions where subReddit=? and scan in (SELECT scanId from scans where type=? AND created >= ?)",[subName,"MULTI-TOP", curr_time])
    mentions = mentions.fetchall()
    print(mentions)
    results = {}
    for mention in mentions:
        scan = mention["scan"]
        ticker = mention["ticker"] 
        numMentions = mention["numMentions"]
        if scan not in results.keys():
            results[scan] = {}
        if numMentions != 0:
            results[scan][ticker] = numMentions
        #TODO: Add a timestamp for the scan
    #database.close()
    return flask.jsonify(results)