import flask
import stonk_scraper
import csv
import os
import time
import zipfile


def zip_stock_data():
    filename = "stonk_scraper/static/database.zip"
    statbuf = os.stat(filename)
    timeEdited = statbuf.st_mtime
    print((time.time() - timeEdited) )
    if (time.time() - timeEdited) > 60*1:
        my_zipfile = zipfile.ZipFile("stonk_scraper/static/database.zip", mode='w', compression=zipfile.ZIP_DEFLATED)
        my_zipfile.write('test1.db')
        my_zipfile.close()

