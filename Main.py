import sys
import os
sys.path.insert(-1, '/usr/local/lib/python2.7/dist-packages')
import argparse

from module.ParserYahooFin.get_yahoo_fin import download_quotes as parser_day_info
from module.ParserStatement.get_statement import Parser
from module.XMLWriter.XMLGenerator import xml_writer
#import initial



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml_bs_pth', type=str, required=False, \
        default= 'data')
    parser.add_argument('--chrome_driver_path', type=str, required=False, \
        default= '/usr/local/share/chromedriver')
    parser.add_argument('--account', type=str, required=True, \
        default= '---')
    parser.add_argument('--password', type=str, required=True, \
        default= '---')
    return parser.parse_args()

if __name__ == '__main__':
    param = get_args()
    obj = Parser(param)
    obj.parser_Login_Selenium()
    stock_num_list = []
    finish_stock_num_list = os.listdir('data')
    count = len(finish_stock_num_list)

    with open('stock_num.txt', 'r') as f_r:
        for line in f_r.readlines():
            stock_num_list.append(line.strip()[0:4])

    for stock_num in stock_num_list:
        if stock_num in finish_stock_num_list:
            continue
        print ('right now is {}, still have {} stock unfinish'.format(stock_num, len(stock_num_list) - count))
        try:
            obj.parser_eps(stock_num)
            obj.parser_book_value(stock_num)
            obj.parser_cash_flow(stock_num)
            obj.parser_profit_margin(stock_num)
            obj.parser_non_oper_income(stock_num)
            obj.parser_roe(stock_num)
            obj.parser_oper_cash_flow_income_rate(stock_num)
            obj.parser_turnover_days(stock_num)

            obj.parser_price_earnings_ratio(stock_num)
            obj.parser_mth_revenue_growth_rate(stock_num)
            obj.parser_average_dividend_yield(stock_num)

            obj.parser_stock_holders(stock_num)
            try:
                parser_day_info('{}.TW'.format(stock_num))
            except:
                parser_day_info('{}.TWO'.format(stock_num))
            xml_writer(obj.dict_all, obj.xml_bs_pth, stock_num)
        except:
            print ('{} has something wrong'.format(stock_num))
        obj.clear()
        count += 1

    #print (obj.week_report_dict, obj.quar_report_dict, obj.mth_report_dict)
        