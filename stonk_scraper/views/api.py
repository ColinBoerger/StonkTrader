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
    global stock_lookup_subs

    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    #@TODO add database
    resHot = cursor.execute("SELECT * from mentions as m where m.ticker = ? and m.scan in (Select scanId from scans where type=? ORDER BY created DESC limit 1)", [ticker, "MULTI-HOT"])
    #resHot = cursor.execute("SELECT scanId from scans where type=? ORDER BY created DESC limit 1", ["MULTI-HOT"])
    #resHot = cursor.execute("SELECT * from mentions as m where m.ticker = ? and m.scan = ? ", [ticker, 272])
    resHot = resHot.fetchall()
    print(resHot)

    cursor = database.cursor()
    resTop = cursor.execute("SELECT * from mentions as m where m.ticker = ? and m.scan in (Select scanId from scans where type=? ORDER BY created DESC limit 1)", [ticker, "MULTI-TOP"])
    resTop = resTop.fetchall()
    print(resTop)
    
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
    to_ret = {}
    ticker = ticker.upper()
    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    #@TODO add database
    cursor.execute("SELECT m.numMentions, m.ticker, st.companyName from stocks as st, mentions as m where m.ticker = ? and m.ticker = st.ticker and m.scan in (Select scanId from scans where type=? ORDER BY created DESC limit 1)", [ticker, "HOT"])
    res = cursor.fetchone()
    print(res)
    to_ret[ticker + "hot"] = res["numMentions"]
    to_ret["name"] = res["companyName"]
    cursor = database.cursor()
    #@TODO add database
    cursor.execute("SELECT m.numMentions, m.ticker, st.companyName from stocks as st, mentions as m where m.ticker = ? and m.ticker = st.ticker and m.scan in (Select scanId from scans where type=? ORDER BY created DESC limit 1)", [ticker, "TOP"])
    res = cursor.fetchone()
    to_ret[ticker + "top"] = res["numMentions"]

    return flask.jsonify(to_ret)

@stonk_scraper.app.route("/stock/supportedSubs/")
def api_supported_subs(method='GET'):
    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    #@TODO add database
    cursor.execute("SELECT DISTINCT subReddit from mentions")
    res = cursor.fetchall()
    to_ret = {}
    subs = []
    for r in res:
        if r["subReddit"] != None:
            subs += [r["subReddit"]]
    to_ret["supportedSubs"] =  subs
    return flask.jsonify(to_ret)

@stonk_scraper.app.route("/subs/<subName>")
def api_sub_data(subName, method='GET'):
    global stream_data
    global names
    
    if len(names.keys()) < 1:
        getNames("tickers.csv")

    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    

    res1 = cursor.execute("SELECT m.ticker, m.numMentions, s.companyName  from mentions as m, stocks as s  where s.ticker=m.ticker AND m.subReddit=? and m.scan in (Select scanId from scans where type=? ORDER BY created DESC limit 1)",[subName, "STREAM"])
    res = res1.fetchall()
    
    data = res[0:10]

    for d in range(0, len(data)): 
        data[d] = [res[d]["ticker"], res[d]["numMentions"], res[d]["companyName"]]
    to_ret = {}
    to_ret["data"] = data
    
    return flask.jsonify(to_ret)

@stonk_scraper.app.route("/subs/<subName>/time/<timeInSeconds>")
def api_sub_time_data(subName,timeInSeconds, method='GET'):
    #TODO: Finish this function
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
    

    res1 = cursor.execute("SELECT *  from scans  where created >= ?",[curr_time])
    res = res1.fetchall()
    print(res)
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