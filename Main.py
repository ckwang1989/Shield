import sys
import os
#sys.path.insert(-1, '/usr/local/lib/python2.7/dist-packages')
import argparse

from module.ParserYahooFin.get_yahoo_fin import download_quotes as parser_day_info
from module.ParserETF.get_etf import Parser
from module.XMLWriter.XMLGenerator import xml_writer
from module.General.lib import dict_to_json_file, json_file_to_dict
#import initial
import time



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
    stock_num_list = []
    finish_stock_num_list = os.listdir('data')
    count = len(finish_stock_num_list)
    d_all_etf = {}
    j_p='etf.json'

    with open('etf_symbol.txt', 'r') as f_r:
        for line in f_r.readlines():
            stock_num_list.append(line.strip())

    for stock_no in stock_num_list:
        d_one_eft = obj.parser_moneydj_ETF_stock_holding(stock_no)
        etf_capital = obj.parser_moneydj_ETF_capital(stock_no)
        d_all_etf[stock_no] = {'capital': etf_capital, 'holding': d_one_eft}

    dict_to_json_file(d_all_etf, j_p)
    d = json_file_to_dict(j_p)


if __name__ == '__main__':
    main()