import praw
import csv
import time
import os

#Uses a praw.ini file
reddit = praw.Reddit("bot1", user_agent="pc:StonkScraper:v0.0.1 (by u/taseru2)")

#https://query1.finance.yahoo.com/v7/finance/chart/SPY

#Idea look into https://praw.readthedocs.io/en/latest/
#memestonktraders
'''

TODO: Change the file saving format to eliminate the 0s. It can be an implied ticker to cut down on storage space


'''

wsb_only = ["wallstreetbets"]

stock_subs = ["wallstreetbets","Stocks", "Stock_picks", "StockMarket", "investing", "dividends"]


def getTickers(csvFileName):
    tickers = []
    with open(csvFileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            line_count += 1
            tickers += [[row[0], 0]]
    return tickers

def generateSubmissionsHot(listOfSubreddits):
    toRet = []
    toRetBySub = {}
    for sub in listOfSubreddits:
        posts = reddit.subreddit(sub).hot()
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

def generateSubmissionsTop(listOfSubreddits, timeFrame):
    toRet = []
    toRetBySub = {}
    for sub in listOfSubreddits:
        posts = reddit.subreddit(sub).hot(timeFrame)
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

def saveResults(titles, symbols):
    filename = "stonk_scraper/static/stock_data/" + str(time.time()).split(".")[0] + ".csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(titles)
        csvwriter.writerows(symbols)

def saveResultsMulti(titles, subSymbols):
    filePath = "stonk_scraper/static/stock_data/subReddits/"
    currTime = str(time.time()).split(".")[0]
    for sub in subSymbols.keys():
        subs = os.listdir(filePath)
        if sub not in subs:
            os.mkdir(filePath + sub)
        filename = filePath + sub + "/" + currTime + ".csv"
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(titles)
            csvwriter.writerows(subSymbols[sub])

def saveStreamData(titles, subSymbols):
    filePath = "stonk_scraper/static/stock_data/streamData/"
    currTime = str(time.time()).split(".")[0]
    for sub in subSymbols.keys():
        subs = os.listdir(filePath)
        if sub not in subs:
            os.mkdir(filePath + sub)
        filename = filePath + sub + "/" + currTime + ".csv"
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(titles)
            csvwriter.writerows(subSymbols[sub])

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
    subreddit = reddit.subreddit(subReddits)
    timeStart = time.time()
    while True:
        numRequests = 0
        for submission in subreddit.stream.submissions():
            print("Here")
            numRequests += 1
            subName = submission.subreddit.display_name.lower()
            toRetBySub[subName] += [submission.title]
            toRetBySub[subName] += [submission.selftext]
            print(subName)
            #time.sleep(.25)
            for comment in submission.comments.list():
                try:
                    toRetBySub[subName] += [comment.body]
                except AttributeError as e:
                    continue
        
            print(time.time() - timeStart)
            if (time.time() - timeStart) > timeInSeconds:
                return toRetBySub

            #Hacky way to stop it from pausing
            if numRequests > 50:
                print("Broken")
                break

def main_test_stream():
    timeStart = time.time()
    timeBobba = time.time()
    submissions_by_sub = streamOfResults(stock_subs, 10)
    symbols = getTickers("tickers.csv")
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
        print(sub2)

        for entry in range(0,len(multiSubSymbols[sub2])):
            if entry >= 10:
                break
            print(str(multiSubSymbols[sub2][entry][0]) + ":" + str(multiSubSymbols[sub2][entry][1]))
    saveStreamData(["Ticker", "Instances"], multiSubSymbols)
def main():
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

        saveResults(["Ticker", "NumApps"], symbols)
        saveResultsMulti(["Ticker", "NumApps"], multiSubSymbols)
        timeEnd = time.time()

        print("Time for run: ")
        print(str((timeEnd-timeStart)/60))
        
        timeStart = timeEnd
        print("Done")
        if (time.time() - timeBobba) > (3600*3):
            return
        time.sleep(500)

main_test_stream()