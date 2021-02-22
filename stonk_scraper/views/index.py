"""
Colin Boerger
"""

import flask
import stonk_scraper
import csv
import os
import time
from helpers import * 

@stonk_scraper.app.route('/', methods=['GET', 'POST'])
def show_index():
    global stock_data_hot
    global stock_data_top
    global time_at_last_update
    database = stonk_scraper.model.get_db()
    cursor = database.cursor()
    res = cursor.execute("SELECT * from stocks").fetchall()
    #print(res)

    if time.time() - time_at_last_update > (15):      
        load_data()
        time_at_last_update = time.time()
        print("Time:")
        print(time_at_last_update)
    cursor.execute("SELECT * from mentions where scan in (Select scanId from scans where type=? ORDER BY created DESC limit 1)",["HOT"])
    #cursor.execute("Select * from scans ") #where type=? ORDER BY created DESC",["HOT"])
    test = cursor.fetchall()
    #print(test)
    to_show_hot = test[0:10]
    #to_show_hot = stock_data_hot[0:10]
    
    cursor.execute("SELECT * from mentions where scan in (Select scanId from scans where type=? ORDER BY created DESC limit 1)",["TOP"])
    test = cursor.fetchall()
    to_show_top = test[0:10] # stock_data_top[0:10]
    context = {}
    for i in range(0,10):
        to_show_hot[i] = [to_show_hot[i]["ticker"], to_show_hot[i]["numMentions"]]
        to_show_top[i] = [to_show_top[i]["ticker"], to_show_top[i]["numMentions"]]
    context["stocks_hot"] = to_show_hot
    context["stocks_top"] = to_show_top
    return flask.render_template('index.html', **context)

@stonk_scraper.app.route('/individual_stocks', methods=['GET', 'POST'])
def show_individual_stocks():
    global time_at_last_update

    if time.time() - time_at_last_update > (15):
        print("Updating")      
        load_data()
        time_at_last_update = time.time()
    print("Time" + str(time_at_last_update))
    context = {}
    return flask.render_template("individual_stock.html", **context)

@stonk_scraper.app.route('/custom_searches', methods=['GET', 'POST'])
def show_custom_searches():
    global time_at_last_update

    if time.time() - time_at_last_update > (15):      
        load_data()
        time_at_last_update = time.time()
    context = {}
    return flask.render_template("custom_searches.html", **context)


@stonk_scraper.app.route('/stock/<ticker>/page', methods=['GET'])
def show_stock_page():
    global time_at_last_update
    if time.time() - time_at_last_update > (15):      
        load_data()
        time_at_last_update = time.time()
    return "Implement me"

#@TODO make it upload to a database
def load_stock_data_sub():
    global stock_lookup_subs

    folders = os.listdir("stonk_scraper/static/stock_data/top/subreddits")
    stock_lookup_subs["top"] = {}
    stock_lookup_subs["hot"] = {}
    for folder in folders:
        files = os.listdir("stonk_scraper/static/stock_data/top/subreddits/" + folder)
        index = 0
        file_time = -1
        file_name = ""
        for i in range(0,len(files)):
            if "csv" not in files[i]:
                continue
            file_time_to_comp = int(files[i].split(".")[0])
            if file_time_to_comp > file_time:
                file_name = "stonk_scraper/static/stock_data/top/subreddits/" + folder + "/" + files[i]
                index = i
                file_time = file_time_to_comp
        tickers = {}
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                    continue
                line_count += 1
                tickers[row[0]] = row[1]
        stock_lookup_subs["top"][folder] = tickers

        files = os.listdir("stonk_scraper/static/stock_data/hot/subreddits/" + folder)
        index = 0
        file_time = -1
        file_name = ""
        for i in range(0,len(files)):
            if "csv" not in files[i]:
                continue
            file_time_to_comp = int(files[i].split(".")[0])
            if file_time_to_comp > file_time:
                file_name = "stonk_scraper/static/stock_data/hot/subreddits/" + folder + "/" + files[i]
                index = i
                file_time = file_time_to_comp
        tickers = {}
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                    continue
                line_count += 1
                tickers[row[0]] = row[1]
        stock_lookup_subs["hot"][folder] = tickers

def load_stream_data():
    global stream_data
    global stock_lookup

    folders = os.listdir("stonk_scraper/static/stock_data/streamData/")
    for folder in folders:
        files = os.listdir("stonk_scraper/static/stock_data/streamData/" + folder)
        index = 0
        file_time = -1
        file_name = ""
        for i in range(0,len(files)):
            if "csv" not in files[i]:
                continue
            file_time_to_comp = int(files[i].split(".")[0])
            if file_time_to_comp > file_time:
                file_name = "stonk_scraper/static/stock_data/streamData/" + folder + "/" + files[i]
                index = i
                file_time = file_time_to_comp
        tickers = []
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                    continue
                line_count += 1
                tickers += [[row[0], row[1]]]
        stream_data[folder] = tickers

def load_data():
    
    #print(time_at_last_update)
    load_stock_data_hot()
    load_stock_data_top()
    load_stream_data()
    load_stock_data_sub()

#Add a way to only get new data if time has passed
def load_stock_data_hot():
    global stock_data_hot
    global stock_lookup_hot


    files = os.listdir("stonk_scraper/static/stock_data/hot/")
    index = 0
    file_time = -1
    file_name = ""
    for i in range(0,len(files)):
        if "csv" not in files[i]:
            continue
        file_time_to_comp = int(files[i].split(".")[0])
        if file_time_to_comp > file_time:
            file_name = "stonk_scraper/static/stock_data/hot/" + files[i]
            index = i
            file_time = file_time_to_comp
    tickers = []
    print(file_name)
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            line_count += 1
            tickers += [[row[0], row[1]]]
            stock_lookup_hot[row[0]] = row[1]
    stock_data_hot = tickers

def load_stock_data_top():
    global stock_data_top
    global stock_lookup_top


    files = os.listdir("stonk_scraper/static/stock_data/top/")
    index = 0
    file_time = -1
    file_name = ""
    for i in range(0,len(files)):
        if "csv" not in files[i]:
            continue
        file_time_to_comp = int(files[i].split(".")[0])
        if file_time_to_comp > file_time:
            file_name = "stonk_scraper/static/stock_data/top/" + files[i]
            index = i
            file_time = file_time_to_comp
    tickers = []
    print(file_name)
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            line_count += 1
            tickers += [[row[0], row[1]]]
            stock_lookup_top[row[0]] = row[1]
    stock_data_top = tickers