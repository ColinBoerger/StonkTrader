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
    database = stonk_scraper.model.get_db()
    cursor = database.cursor()

    cursor.execute("SELECT * from mentions where scan in (Select scanId from scans where type=? ORDER BY created DESC limit 1)",["HOT"])
    test = cursor.fetchall()
    
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
    context = {}
    return flask.render_template("individual_stock.html", **context)

@stonk_scraper.app.route('/custom_searches', methods=['GET', 'POST'])
def show_custom_searches():
    context = {}
    return flask.render_template("custom_searches.html", **context)


@stonk_scraper.app.route('/stock/<ticker>/page', methods=['GET'])
def show_stock_page(ticker):
    context = {}
    context["ticker"] = ticker
    return flask.render_template("stock_page.html", **context)

@stonk_scraper.app.route('/scan/<number>/page', methods=['GET'])
def show_scan_page(number):
    return "Implement me"
    #context = {}
    #return flask.render_template("scan_page.html", **context)
