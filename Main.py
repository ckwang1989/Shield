import sys
import os
#sys.path.insert(-1, '/usr/local/lib/python2.7/dist-packages')
import argparse

from module.ParserYahooFin.get_yahoo_fin import download_quotes as parser_day_info
from module.ParserETF.get_etf import Parser, get_etf_insert_idx, get_symbols
from module.XMLWriter.XMLGenerator import xml_writer
from module.General.lib import dict_to_json_file, json_file_to_dict
import finviz
import time

analysis_statement_status = 1  #0: don't care, 1: basic(volume & optionable), 2: all function in analysis_statement()

def analysis_statement(stock_name):
    stock_dict = finviz.get_stock(stock_name)
    if analysis_statement_status == 0:
        return True
    if not stock_dict['Optionable'] == 'Yes':
        #print ('unOptionable')
        return False
    if not 'M' in stock_dict['Avg Volume']:
        #print ('low Volume')
        return False
    if analysis_statement_status == 2:
        if '-' in stock_dict['ROE']:
            #print ('-roe')
            return False
        if float(stock_dict['ROE'][:-1]) < 10.0:
            #print ('roe')
            return False
        if '-' in stock_dict['EPS Q/Q']:
            #print (stock_name, 'EPS Q/Q')
            #print ('eps')
            return False
        if '-' in stock_dict['EPS next Q']:
            #print (stock_name, 'EPS next Q')
            #print ('eps2')
            return False
        if '-' in stock_dict['Sales Q/Q']:
            #print (stock_name, 'EPS next Q')
            #print ('eps2')
            return False

    return True


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
    parser.add_argument('--config_path', type=str)
    return parser.parse_args()

def main():
    param = get_args()
    obj = Parser(param)
    obj.parser_Login_Selenium()
    need_etf = []
    etfs = []
    d_all_etf = {}
    j_p='etf.json'
    wants = []

    with open('etf_symbol.txt', 'r') as f_r:
        for line in f_r.readlines():
            need_etf.append(line.strip())

    for etf_symbol in need_etf:
        count = 0
        etf_capital = None
        one_eft = obj.parser_moneydj_ETF_stock_holding(etf_symbol)
        while etf_capital == None and count < 3:
            etf_capital = obj.parser_moneydj_ETF_capital(etf_symbol)
            count += 1
        print (etf_symbol, etf_capital)
        etfs.insert(get_etf_insert_idx(etfs, etf_capital), {'etf_symbol': etf_symbol, 'capital': etf_capital, 'holding': one_eft})
    etf_symbols = get_symbols(etfs)
    print (etf_symbols)
    for stock in etf_symbols:
        if analysis_statement(stock['symbol'].replace('.', '-')):
            wants.append(f'{stock["symbol"]}-{stock["etf_symbol"]}')

    with open('stock_num.txt', 'w') as f_w:
        f_w.write('\n'.join(wants))


if __name__ == '__main__':
    main()