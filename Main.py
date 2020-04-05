import sys
import os
#sys.path.insert(-1, '/usr/local/lib/python2.7/dist-packages')
import argparse

from module.ParserYahooFin.get_yahoo_fin import download_quotes as parser_day_info
from module.ParserTWSE.get_twse import Parser
from module.XMLWriter.XMLGenerator import xml_writer
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

    with open('stock_num_twse.txt', 'r') as f_r:
        for line in f_r.readlines():
            stock_num_list.append(line.strip()[0:4])
    if True:
        stock_num = 2002
#    for stock_num in stock_num_list:
        #if stock_num in finish_stock_num_list:
        #    continue
        print ('right now is {}, still have {} stock unfinish'.format(stock_num, len(stock_num_list) - count))
        for stock_no in stock_num_list:
            for typ in ['STOCK_DAY']:
                for y in range(99, 109+1):
                    for m in range(1, 12+1):
#                        for d in range(1, 31+1):
                            try:
#                            if 1:
                                obj.parser_STOCK_DAY_TWSE(typ, y, m, stock_no)
                                # obj.parser_general_TWSE(typ, y, m, d)
                            except:
                                print (y, m)
                            time.sleep(3)
        #    try:
        #        parser_day_info('{}.TW'.format(stock_num))
        #    except:
        #        parser_day_info('{}.TWO'.format(stock_num))
        #    xml_writer(obj.dict_all, obj.xml_bs_pth, stock_num)
        #except:
        #    print ('{} has something wrong'.format(stock_num))


#def main():
#	param = get_args()
#	boss = Boss(get_stock_name_list())
#	boss.load_config(param.config_path)
#	boss.hire_worker()
#	boss.assign_task()

if __name__ == '__main__':
    main()