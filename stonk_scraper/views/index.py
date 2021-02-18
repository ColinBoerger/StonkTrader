"""
Colin Boerger
"""

import flask
import stonk_scraper
import csv
import os
import time
from helpers import stream_data, stock_lookup, time_at_last_update, names, stock_data
'''
global stock_data
global stock_lookup
global time_at_last_update

stock_data = []

stock_lookup = {}

time_at_last_update = 0  
'''

@stonk_scraper.app.route('/', methods=['GET', 'POST'])
def show_index():
    global stream_data
    global stock_lookup
    global time_at_last_update
    global names
    global stock_data
    load_stock_data()
    load_stream_data()
    to_show = stock_data[0:10]
    context = {}
    context["stocks"] = to_show
    return flask.render_template('index.html', **context)

@stonk_scraper.app.route('/individual_stocks', methods=['GET', 'POST'])
def show_individual_stocks():
    global stream_data
    global stock_lookup
    global time_at_last_update
    global names
    global stock_data
    #TODO show the stock trending overtime
    load_stock_data()
    context = {}
    return flask.render_template("individual_stock.html", **context)

@stonk_scraper.app.route('/custom_searches', methods=['GET', 'POST'])
def show_custom_searches():
    global stream_data
    global stock_lookup
    global time_at_last_update
    global names
    global stock_data
    #TODO show the stock trending overtime
    load_stream_data()
    context = {}
    return flask.render_template("custom_searches.html", **context)




def load_stream_data():
    global stream_data
    global stock_lookup
    global time_at_last_update
    
    time_at_last_update = time.time()
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



#Add a way to only get new data if time has passed
def load_stock_data():
    global stock_data
    global stock_lookup
    global time_at_last_update

    if time.time() - time_at_last_update < (60*15):
        print("No change")
        return
    time_at_last_update = time.time()

    files = os.listdir("stonk_scraper/static/stock_data")
    index = 0
    file_time = -1
    file_name = ""
    for i in range(0,len(files)):
        if "csv" not in files[i]:
            continue
        file_time_to_comp = int(files[i].split(".")[0])
        if file_time_to_comp > file_time:
            file_name = "stonk_scraper/static/stock_data/" + files[i]
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
            stock_lookup[row[0]] = row[1]
    stock_data = tickers
    load_stream_data()