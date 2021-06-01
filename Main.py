import sys
import os
sys.path.insert(-1, '/usr/local/lib/python2.7/dist-packages')
import argparse
import time
from datetime import date

from module.ParserYahooFin.get_yahoo_fin import download_quotes as parser_day_info
from module.ParserStatement.get_statement import Parser
from module.XMLWriter.XMLGenerator import xml_writer

d = date.today()

def check_folder(p):
    if not os.path.exists(p):
        os.makedirs(p)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sav_bs_pth', type=str, \
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
    #t-100061512
    param = get_args()
    check_folder(param.sav_bs_pth)

    obj = Parser(param)
    obj.parser_Login_Selenium()
    stock_num_list = []
    finish_stock_num_list = os.listdir(param.sav_bs_pth)
    count = len(finish_stock_num_list)

    with open('stock_num.txt', 'r',encoding="utf-8") as f_r:
        for line in f_r.readlines():
            stock_num_list.append(line.strip()[0:4])

    haven_pkls = set([p[:-4] for p in os.listdir(param.sav_bs_pth)])

    for stock_num in sorted(list(set(stock_num_list)-haven_pkls)):
        time.sleep(1.5)
        update_to_date = obj.parser_eps(stock_num)
        time.sleep(1.5)
        if not update_to_date:
            obj.parser_book_value(stock_num)
            time.sleep(1.5)
            obj.parser_cash_flow(stock_num)
            time.sleep(1.5)
            obj.parser_profit_margin(stock_num)
            time.sleep(1.5)
            obj.parser_non_oper_income(stock_num)
            time.sleep(1.5)
            obj.parser_roe(stock_num)
            time.sleep(1.5)
            obj.parser_oper_cash_flow_income_rate(stock_num)
            time.sleep(1.5)
            obj.parser_turnover_days(stock_num)
            time.sleep(1.5)
            obj.parser_price_earnings_ratio(stock_num)
            time.sleep(1.5)
            obj.parser_average_dividend_yield(stock_num)
            time.sleep(1.5)
            obj.parser_stock_holders(stock_num)
        obj.save(os.path.join(param.sav_bs_pth, stock_num+'.pkl'))
        obj.clear()
        count += 1

#def main():
#	param = get_args()
#	boss = Boss(get_stock_name_list())
#	boss.load_config(param.config_path)
#	boss.hire_worker()
#	boss.assign_task()

if __name__ == '__main__':
    main()