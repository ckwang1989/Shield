import sys
import os
sys.path.insert(-1, '/usr/local/lib/python2.7/dist-packages')
import argparse

from module.ParserYahooFin.get_yahoo_fin import download_quotes as parser_day_info
from module.ParserStatement.get_statement import Parser
from module.XMLWriter.XMLGenerator import xml_writer

import time
import copy
import pickle

def check_folder(p):
    if not os.path.exists(p):
        os.makedirs(p)

def save_pickle(p, result):
    with open(p, 'wb') as handle:
        pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_pickle(p):
    with open(p, 'rb') as f:
        result = pickle.load(f)
    return result

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
    check_folder(os.path.join(os.getcwd(), param.xml_bs_pth))
    obj = Parser(param)
    obj.parser_Login_Selenium()
    stock_num_list = []
    finish_stock_num_list = os.listdir(os.path.join(os.getcwd(), param.xml_bs_pth))
    count = len(finish_stock_num_list)

    pe_threshold = 14
    volume_threshold = 500
    top_N = 30
    result_p = f'result/{time.strftime("%Y-%m-%d", time.localtime())}'
    result_pickle_p = f'result/{time.strftime("%Y-%m-%d", time.localtime())}.pkl'
    check_folder(result_p)
#    stock_num = 2002
#    time.sleep(2)
#    obj.parser_K_screenshot(stock_num, f'{result_p}/{stock_num}.png')
#    assert False
    result_topN = {'foreign_inv_volume': {}, 'inv_trust_volume': {}, 'foreign_inv_volume_price': {}, 'inv_trust_volume_price': {}, \
                    'foreign_inv_volume/totalvolume': {}, 'inv_trust_volume/totalvolume': {}, 'foreign_inv_volume_price/share': {}, 'inv_trust_volume_price/share': {}}

    with open('stock_num.txt', 'r', encoding="utf-8") as f_r:
        for line in f_r.readlines():
            stock_num_list.append(line.strip()[0:4])

    for i_stock_num, stock_num in enumerate(stock_num_list):
        print(stock_num)
        if i_stock_num and i_stock_num % 100 == 0:
            print('i_stock_num: ', i_stock_num, ' result_topN: ', result_topN)
#        try:  
        if True: 
            price, pe, volume, share_capital = obj.parser_price(stock_num)
            if price == 0 and pe == 0 and volume == 0: continue
            result_shareholder = obj.parser_investment_trust(stock_num, 0)
            if result_shareholder == {}: continue
            if result_shareholder['foreign_inv_volume'] <= 0 and result_shareholder['inv_trust_volume'] <= 0: continue
            for typ in ['foreign_inv_volume', 'inv_trust_volume']:
                if len(result_topN[typ].keys()) < top_N:
                    if result_shareholder[f'{typ}'] not in result_topN[f'{typ}'].keys():
                        result_topN[f'{typ}'][result_shareholder[f'{typ}']] = [stock_num]
                    else:
                        result_topN[f'{typ}'][result_shareholder[f'{typ}']].append(stock_num)
                    
                    if (result_shareholder[f'{typ}'] * price) not in result_topN[f'{typ}_price'].keys():
                        result_topN[f'{typ}_price'][result_shareholder[f'{typ}'] * price] = [stock_num]
                    else:
                        result_topN[f'{typ}_price'][result_shareholder[f'{typ}'] * price].append(stock_num)

                    if (result_shareholder[f'{typ}'] / float(volume)) not in result_topN[f'{typ}/totalvolume'].keys():
                        result_topN[f'{typ}/totalvolume'][result_shareholder[f'{typ}'] / float(volume)] = [stock_num]
                    else:
                        result_topN[f'{typ}/totalvolume'][result_shareholder[f'{typ}'] / float(volume)].append(stock_num)

                    if (result_shareholder[f'{typ}'] * price / float(share_capital)) not in result_topN[f'{typ}_price/share'].keys():
                        result_topN[f'{typ}_price/share'][result_shareholder[f'{typ}'] * price / float(share_capital)] = [stock_num]
                    else:
                        result_topN[f'{typ}_price/share'][result_shareholder[f'{typ}'] * price / float(share_capital)].append(stock_num)

                else:
                    volume_min = sorted(result_topN[f'{typ}'])[0]
                    if result_shareholder[f'{typ}'] > volume_min:
                        result_topN[f'{typ}'].pop(volume_min)
                        if result_shareholder[f'{typ}'] not in result_topN[f'{typ}'].keys():
                            result_topN[f'{typ}'][result_shareholder[f'{typ}']] = [stock_num]
                        else:
                            result_topN[f'{typ}'][result_shareholder[f'{typ}']].append(stock_num)

                    volume_price_min = sorted(result_topN[f'{typ}_price'])[0]
                    if (result_shareholder[f'{typ}'] * price) > volume_price_min:
                        result_topN[f'{typ}_price'].pop(volume_price_min)
                        if (result_shareholder[f'{typ}'] * price) not in result_topN[f'{typ}_price'].keys():
                            result_topN[f'{typ}_price'][result_shareholder[f'{typ}'] * price] = [stock_num]
                        else:
                            result_topN[f'{typ}_price'][result_shareholder[f'{typ}'] * price].append(stock_num)
                    
                    divide_totalvolume_min = sorted(result_topN[f'{typ}/totalvolume'])[0]
                    if (result_shareholder[f'{typ}'] / float(volume)) > divide_totalvolume_min:
                        result_topN[f'{typ}/totalvolume'].pop(divide_totalvolume_min)
                        if (result_shareholder[f'{typ}'] / float(volume)) not in result_topN[f'{typ}/totalvolume'].keys():
                            result_topN[f'{typ}/totalvolume'][result_shareholder[f'{typ}'] / float(volume)] = [stock_num]
                        else:
                            result_topN[f'{typ}/totalvolume'][result_shareholder[f'{typ}'] / float(volume)].append(stock_num)

                    volume_price_divshare_min = sorted(result_topN[f'{typ}_price/share'])[0]
                    if (result_shareholder[f'{typ}'] * price / float(share_capital)) > volume_price_divshare_min:
                        result_topN[f'{typ}_price/share'].pop(volume_price_divshare_min)
                        if (result_shareholder[f'{typ}'] * price / float(share_capital)) not in result_topN[f'{typ}_price/share'].keys():
                            result_topN[f'{typ}_price/share'][result_shareholder[f'{typ}'] * price / float(share_capital)] = [stock_num]
                        else:
                            result_topN[f'{typ}_price/share'][result_shareholder[f'{typ}'] * price / float(share_capital)].append(stock_num)

#        except:
#            print(i_stock_num, stock_num, 'fail')
    save_pickle(result_pickle_p, result_topN)
    result_topN = load_pickle(result_pickle_p)

    symbols = []
    for typ in result_topN.keys():
        for k in result_topN[typ].keys():
            symbols.extend(result_topN[typ][k])
        
    for stock_num in sorted(list(set(symbols))):
        ranks = []
        for k in result_topN.keys():
            keys = result_topN[k]
            values = [b for a in list(sorted(keys.keys(), reverse = True)) for b in keys[a]]
            if stock_num in values:
                rank = values.index(stock_num)
            else:
                rank = -1
            ranks.append(str(rank))
        obj.parser_K_screenshot(stock_num, f'{result_p}/{stock_num}.png', ranks)


if __name__ == '__main__':
    main()