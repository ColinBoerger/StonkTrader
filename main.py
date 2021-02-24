import praw
import csv
import time
import os
import sqlite3
from multiprocessing import Process
#Uses a praw.ini file
reddit1 = praw.Reddit("bot1", user_agent="pc:StonkScraper:v0.0.1 (by u/taseru2)")
reddit2 = praw.Reddit("bot2", user_agent="pc:StonkScraper:v0.0.1 (by u/taseru2)")

#https://query1.finance.yahoo.com/v7/finance/chart/SPY

#Idea look into https://praw.readthedocs.io/en/latest/
#memestonktraders
'''



'''
wsb_only = ["wallstreetbets"]

stock_subs = ["wallstreetbets","stocks", "stock_picks", "stockmarket", "investing", "dividends"]


def getTickers(csvFileName):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    print("Opened database successfully")
    #@TODO Insert all information into the 
    tickers = []
    names = []
    c.execute("Select * from stocks")
    res = c.fetchall()
    if len(res) > 0:
        for row in res:
            tickers += [[row[0], 0]]
        conn.commit()
        conn.close()
        return tickers
    with open(csvFileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            line_count += 1
            tickers += [[row[0], 0]]
            names += [(row[0], row[1])]
        c.executemany('INSERT INTO stocks VALUES (?,?)',names)
    conn.commit()
    conn.close()
    return tickers

def generateSubmissionsHot(listOfSubreddits):
    toRet = []
    toRetBySub = {}
    for sub in listOfSubreddits:
        posts = reddit2.subreddit(sub).hot(limit=10)
        toRetBySub[sub] = []
        for p in posts:
            toRet += [p.selftext]
            toRet += [p.title] 
            toRetBySub[sub] += [p.selftext]
            toRetBySub[sub] += [p.title]
            for comment in p.comments.list():
                try:
                    toRet += [comment.body]
                    toRetBySub[sub] += [comment.body]
                except AttributeError as e:
                    continue
    return [toRet, toRetBySub]

def generateSubmissionsTop(listOfSubreddits):
    toRet = []
    toRetBySub = {}
    for sub in listOfSubreddits:
        posts = reddit2.subreddit(sub).top(limit=10)
        toRetBySub[sub] = []
        for p in posts:
            toRet += [p.selftext]
            toRet += [p.title]
            toRetBySub[sub] += [p.selftext]
            toRetBySub[sub] += [p.title]
            for comment in p.comments.list():
                try:
                    toRet += [comment.body]
                    toRetBySub[sub] += [comment.body]
                except AttributeError as e:
                    continue
    return [toRet, toRetBySub]

def findInstancesNoDuplicates(ticker, listOfSubmissions):
    toRet  = 0
    #This prevents tickers that are just letters from being overrepresented
    ticker = " " + ticker + " "
    ticker_dollar_sign = "$" + ticker + " "

    #TODO: refine this to add more fine tuned sting matching possibly using regex
    for sub in listOfSubmissions:
        if ticker in sub or ticker_dollar_sign in sub:
            toRet += 1
    return toRet

def saveResults(titles, symbols, hotOrTop, filePath):
    #@TODO I think I can delete this code and for total I can just sum the subs
    conn = sqlite3.connect('test.db')
    print("Opened database successfully")
    c = conn.cursor()
    c.execute("INSERT INTO scans(type) VALUES (?)", [hotOrTop])
    c = conn.cursor()
    c.execute("SELECT scanID, created FROM scans ORDER BY created DESC limit 1")
    currScan = c.fetchone()
    filename = filePath + str(time.time()).split(".")[0] + ".csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(titles)
        csvwriter.writerows(symbols)
    toWrite = []
    for sys in symbols:
        entry = (sys[0], sys[1],currScan[0])
        toWrite += [entry]
    c.executemany("INSERT INTO mentions VALUES (?,?,NULL,?)", toWrite)
    print(hotOrTop + " Printed")
    conn.commit()
    conn.close()

def saveResultsMulti(titles, subSymbols,hotOrTop, filePath):
    conn = sqlite3.connect('test.db')
    print("Opened database successfully")
    currTime = str(time.time()).split(".")[0]
    c = conn.cursor()
    c.execute("INSERT INTO scans(type) VALUES (?)", ["MULTI-"+hotOrTop])
    conn.commit()
    c = conn.cursor()

    c.execute("SELECT scanID, created FROM scans where type=? ORDER BY created DESC limit 1", ["MULTI-"+hotOrTop])
    currScan = c.fetchone()
    print("CurrScan: " + str(currScan))
    toWrite = []
    for sub in subSymbols.keys():
        for row in subSymbols[sub]:
            entry = (row[0],row[1],sub,currScan[0])
            toWrite += [entry]
        subs = os.listdir(filePath + "subreddits/")
        # if sub not in subs:
        #     os.mkdir(filePath + "subreddits/" + sub)
        filename = filePath + "subreddits/" + sub + "/" + currTime + ".csv"
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(titles)
            csvwriter.writerows(subSymbols[sub])
    #print(toWrite)
    c.executemany("INSERT INTO mentions VALUES (?,?,?,?)", toWrite)
    conn.commit()
    conn.close()

def saveStreamData(titles, subSymbols):
    conn = sqlite3.connect('test.db')
    print("Opened database successfully")
    c = conn.cursor()
    c.execute("INSERT INTO scans(type) VALUES (?)", ["STREAM"])
    conn.commit()
    c = conn.cursor()

    c.execute("SELECT scanID, created FROM scans ORDER BY created DESC limit 1")
    currScan = c.fetchone()
    toWrite = []
    filePath = "stonk_scraper/static/stock_data/streamData/"
    currTime = str(time.time()).split(".")[0]
    for sub in subSymbols.keys():
        for row in subSymbols[sub]:
            entry = (row[0],row[1],sub,currScan[0])
            toWrite += [entry]
        subs = os.listdir(filePath)
        if sub not in subs:
            os.mkdir(filePath + sub)
        filename = filePath + sub + "/" + currTime + ".csv"
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(titles)
            csvwriter.writerows(subSymbols[sub])
    c.executemany("INSERT INTO mentions VALUES (?,?,?,?)", toWrite)
    conn.commit()
    conn.close()

def getResultsDaily(listOfSubreddits):
    print("Implement me")


#Note I deleted the stocks DD CEO and ! because the amount of false positives

def streamOfResults(listOfSubreddits, timeInSeconds):
    #TODO: Figure out how to get around the throttling of our requests. We are only getting requests passed out and then it stops collecting data
    subReddits = ""
    toRetBySub = {}
    for s in range(0,len(listOfSubreddits)):
        toRetBySub[listOfSubreddits[s].lower()] = []
        if s < (len(listOfSubreddits) - 1):        
            subReddits += listOfSubreddits[s] + "+";
        else:
            subReddits += listOfSubreddits[s]
    print(subReddits)
    subreddit = reddit1.subreddit(subReddits)
    timeStart = time.time()
    while True:
        numRequests = 0
        for submission in subreddit.stream.submissions():
            #print("Here")
            numRequests += 1
            subName = submission.subreddit.display_name.lower()
            toRetBySub[subName] += [submission.title]
            toRetBySub[subName] += [submission.selftext]
            #print(subName)
            #time.sleep(.25)
            for comment in submission.comments.list():
                try:
                    toRetBySub[subName] += [comment.body]
                except AttributeError as e:
                    continue
        
            #print(time.time() - timeStart)
            if (time.time() - timeStart) > timeInSeconds:
                return toRetBySub

            #Hacky way to stop it from pausing
            if numRequests > 50:
                #print("Broken")
                break

def main_test_stream():
    symbols = getTickers("tickers.csv")
    print("Here")
    while True:
        submissions_by_sub = streamOfResults(stock_subs, 3600)
        multiSubSymbols = {}
        for sub in submissions_by_sub.keys():
            multiSubSymbols[sub] = []

        for i in range(0,len(symbols)):
            for sub1 in submissions_by_sub.keys():
                numInstances =  findInstancesNoDuplicates(symbols[i][0], submissions_by_sub[sub1])
                if numInstances > 0:
                    multiSubSymbols[sub1] +=  [[symbols[i][0], numInstances]]
        for sub2 in submissions_by_sub:
            multiSubSymbols[sub2].sort(reverse=True,key=lambda a: a[1])
            #print(sub2)

            for entry in range(0,len(multiSubSymbols[sub2])):
                if entry >= 10:
                    break
            #print(str(multiSubSymbols[sub2][entry][0]) + ":" + str(multiSubSymbols[sub2][entry][1]))
        saveStreamData(["Ticker", "Instances"], multiSubSymbols)
def main_get_results():
    timeStart = time.time()
    timeBobba = time.time()
    symbols = getTickers("tickers.csv")
    
    while True:
        multiSubSymbols = {}
        results = generateSubmissionsHot(stock_subs)
        submissions_total = results[0]
        submissions_by_sub = results[1]
        for sub in submissions_by_sub.keys():
            multiSubSymbols[sub] = []

        for i in range(0,len(symbols)):
            symbols[i][1] = findInstancesNoDuplicates(symbols[i][0], submissions_total)
            for sub in submissions_by_sub.keys():
                numInstances = findInstancesNoDuplicates(symbols[i][0], submissions_by_sub[sub])
                if numInstances > 0:
                    multiSubSymbols[sub] +=  [[symbols[i][0], numInstances]]

        symbols.sort(reverse=True,key=lambda a: a[1])
        for sub in submissions_by_sub:
            multiSubSymbols[sub].sort(reverse=True,key=lambda a: a[1])

        saveResults(["Ticker", "NumApps"], symbols,"HOT", "stonk_scraper/static/stock_data/hot/")
        saveResultsMulti(["Ticker", "NumApps"], multiSubSymbols,"HOT", "stonk_scraper/static/stock_data/hot/")
#TODO: Break this up into another function that runs concurrently
        print("HOT Saved")
        multiSubSymbols = {}
        results = generateSubmissionsTop(stock_subs)
        submissions_total = results[0]
        submissions_by_sub = results[1]
        for sub in submissions_by_sub.keys():
            multiSubSymbols[sub] = []

        for i in range(0,len(symbols)):
            symbols[i][1] = findInstancesNoDuplicates(symbols[i][0], submissions_total)
            for sub in submissions_by_sub.keys():
                numInstances = findInstancesNoDuplicates(symbols[i][0], submissions_by_sub[sub])
                if numInstances > 0:
                    multiSubSymbols[sub] +=  [[symbols[i][0], numInstances]]

        symbols.sort(reverse=True,key=lambda a: a[1])
        for sub in submissions_by_sub:
            multiSubSymbols[sub].sort(reverse=True,key=lambda a: a[1])

        saveResults(["Ticker", "NumApps"], symbols, "TOP", "stonk_scraper/static/stock_data/top/")
        saveResultsMulti(["Ticker", "NumApps"], multiSubSymbols, "TOP", "stonk_scraper/static/stock_data/top/")
        print("TOP Saved")
        timeEnd = time.time()

        #print("Time for run: ")
        #print(str((timeEnd-timeStart)/60))
        
        timeStart = timeEnd
        print("Recheck results")
        #if (time.time() - timeBobba) > (3600*3):
         #   print("Ended")
         #   exit()
        #time.sleep(3600*4)
print("start")
#p = Process(target=main_test_stream, args=())
#p.start()
main_get_results()