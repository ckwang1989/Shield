import sys
import os
sys.path.insert(-1, '/usr/local/lib/python2.7/dist-packages')
import argparse

from module.ParserYahooFin.get_yahoo_fin import download_quotes as parser_day_info
from module.ParserStatement.get_statement import Parser
from module.XMLWriter.XMLGenerator import xml_writer

import multiprocessing
from multiprocessing import Process
from multiprocessing import queues

import copy

import finviz

import pandas as pd

class Trader(object):
    def __init__(self):
        self.obj = Parser(param)
        self.obj.parser_Login_Selenium()

    def analysis_statement(self, stock_name):
        stock_dict = finviz.get_stock(stock_name)
        print (stock_dict)
        if stock_dict['Optionable'] != 'Yes':
            return False

    def analysis_document(self, workers_num, stock_queues):
        while not stock_queues.empty():
            stock = stock_queues.get()

            d,typ = self.obj.parser_earning(stock)

            p = f'earning/{stock}_{typ}.csv'
            self.out_csv(d, p)

    def analysis_document_single(self, stock):
        d,typ = self.obj.parser_earning(stock)

    def out_csv(self, d, p):
        df = pd.DataFrame(d, columns= list(d.keys()))
        df.to_csv(p)

class Boss(object):
    def __init__(self, stock_name_list):
        self.num_worker = 1
        self.stock_queues = queues.Queue(len(stock_name_list), ctx=multiprocessing)
        for stock_name in stock_name_list:
            self.stock_queues.put(stock_name)
        self.workers = []

    def assign_task(self):
        for i in range(self.num_worker):
            p = Process(target=Trader().analysis_document, args=(i, self.stock_queues,))
            p.start()
            p.join(timeout=0.5)
        #self.workers[0].analysis_document(0, self.stock_queues)

        print ('assign task finish!')




def get_stock_name_list():
    from finviz.screener import Screener

    filters = ['geo_usa', 'sh_avgvol_o1000', 'sh_opt_option']  # Shows companies in NASDAQ which are in the S&P500
    # Get the first 50 results sorted by price ascending
    stock_list = Screener(filters=filters)

#    # Export the screener results to .csv
#    stock_list.to_csv()

#    # Create a SQLite database
#    stock_list.to_sqlite()

    stock_name_list = []
    for stock_dict in stock_list.data:
        stock_name_list.append(stock_dict['Ticker'])
    print (stock_name_list)
    return stock_name_list

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml_bs_pth', type=str, \
        default= 'data')
    parser.add_argument('--chrome_driver_path', type=str, \
        default= '/usr/local/share/chromedriver')
    parser.add_argument('--account', type=str, required=True, \
        default= '---')
    parser.add_argument('--password', type=str, required=True, \
        default= '---')
    return parser.parse_args()


param = get_args()
if not os.path.exists('earning'):
    os.makedirs('earning')

# multi-process
boss = Boss(get_stock_name_list())
boss.assign_task()

# single-process
'''
t = Trader()
for s in get_stock_name_list():
    print (s)
    p = f'earning/{s}_{typ}.csv'
    d, typ = t.analysis_document_single(s):
    t.out_csv(d, p)
    '''