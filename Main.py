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
import pickle

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

def to_excel(outputs, excel_p='result.xlsx'):
#        input:
#            outputs: [{'k1': v1, 'k2': v2....}, {'k1': v1, 'k2': v2....} ...]
#        output:
#            excel_file

    df = pd.DataFrame(outputs)
    df.to_excel(excel_p)

def dump_pickle(p, content):
    with open(p, 'wb') as handle:
        pickle.dump(content, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_pickle(p):
    with open(p, 'rb') as handle:
        b = pickle.load(handle)
    return b

param = get_args()

class Trader():
    def __init__(self, param):
        self.parser = Parser(param)
        self.parser.parser_Login_Selenium()

trader = Trader(param)
#results = trader.parser.parser_finviz_screener()
#dump_pickle('fizviz_screener.pkl', results)
outputs = load_pickle('fizviz_screener.pkl')
print (outputs)
to_excel(outputs, excel_p='result.xlsx')


