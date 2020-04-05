import sys
sys.path.insert(-1, '/usr/local/lib/python2.7/dist-packages')

import time
import os
import json
#from Module import net_fn

from urllib import request
from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

import argparse

import copy



class Parser(object):
    # all_dict:
    # { '20112': {'eps': 0.7, 'free_cash': 0.8, .....}  \
    #    .........                                      \
    #   '20172': {'eps': 0.7, 'free_cash': 0.8, .....}  \
    #    .........                                      \
    # }
    def __init__(self, param):
        #super(XMLGenerator,self).__init__()
        self.driver = None
        self.stock_num = -1
        self.chrome_path = param.chrome_driver_path
        self.xml_bs_pth = param.xml_bs_pth
        self.account = param.account
        self.password = param.password
        self.dict_all = {'quar': {}, 'mth': {}, 'week': {}}
        #self.quar_report_dict = {}
        #self.mth_report_dict = {}
        #self.week_report_dict = {}
    '''
    @staticmethod
    def cancel_point(number_point):
        while(',' in number_point):
            number_point = number_point + '!'
            index = number_point.find(',')
            index_end = number_point.find('!')
            number_before = number_point[0:index].strip()
            number_after = number_point[(index+1):index_end].strip()
            number_point = number_before + number_after
        return (number_point)
    '''

    @staticmethod
    def cancel_point(number_point, sign = ','):
        while(sign in number_point):
            number_point = number_point + '!'
            index = number_point.find(sign)
            index_end = number_point.find('!')
            number_before = number_point[0:index].strip()
            number_after = number_point[(index+1):index_end].strip()
            number_point = number_before + number_after
        return (number_point)

    @staticmethod
    def is_value(str):
        '''
        is_value: return True if str is int or float, else return False
        '''
        try:
            float(str)
            return True
        except ValueError:
            return False


    def Init_Browser(self):
        '''
        Init_Browser: Install chrome driver if it's not exist
            Input: 
                self.chrome_path: setting in constructor
            Output:
                self.driver: the driver of chrome
        '''
        if os.path.exists(self.chrome_path):
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--window-size=1920x1080")
            chrome_options.add_argument("--mute-audio")
            self.driver = webdriver.Chrome(chrome_options=chrome_options, \
                executable_path=self.chrome_path)
        else:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def parser_Login_Selenium(self):
        '''
        parser_Login_Selenium: Login with Selenium
            Input:  
                account()
                password
            Output:
                N/A
        '''
#        account = self.account
#        password = self.password
        if self.driver == None:
            self.Init_Browser()
#        self.driver.get("https://statementdog.com/users/sign_in")
#        self.driver.find_element_by_id("user_email").send_keys(account)
#        self.driver.find_element_by_id("user_password").send_keys(password)
#        self.driver.find_element_by_class_name("submit-btn").click()

    def get_soup(self, url):
        'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date=20200401&selectType=ALL'
        '''
        get_soup: get soup from url onlt for quar
            Input:  
                url
            Output:
                soup
        '''
        print (url)
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 1)
        #wait.until(EC.presence_of_element_located((By.CLASS_NAME, \
        #    'sheet-interval-current-option-text')))
        #time.sleep(2)
        #temp = self.driver.find_element_by_xpath(\
        #    '//*[@class="sheet-ctrl-dropdown-menu sheet-interval-options-list"]/li[3]')
        #self.driver.execute_script("arguments[0].click();", temp)
        #time.sleep(2)
        soup = (BeautifulSoup(self.driver.page_source,"lxml"))
        return soup

    def get_soup_2(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'lxml')
        return soup

    def get_soup_3(self, url):
        r = requests.get(url)
        with open ("demo3.csv", "wb") as code:
            code.write(r.content)
        assert False
        self.driver.get(url)
        #self.driver.find_element_by_class_name('C(t) O(n):f Tsh($actionBlueTextShadow) Bd(n) Bgc(t) Fz(14px) Pos(r) T(-1px) Bd(n):f Bxsh(n):f Cur(p) W(190px)')

        self.driver.find_element_by_class_name('Fl(end) Mt(3px) Cur(p)').click()

        time.sleep(1)
        temp = self.driver.find_element_by_xpath(\
            '//*[@class="Pos(a) Px(20px) Pt(12px) Pb(20px) Mstart(40px) Z(10) \
            Bgc(#fff) Bd Bdc($c-fuji-grey-c) Bdrs(2px) Bxsh($boxShadow) W(195px)"]/li[7]')
        self.driver.execute_script("arguments[0].click();", temp)
        time.sleep(1)
        soup = (BeautifulSoup(self.driver.page_source,"lxml"))
        return soup

    # BWIBBU_d MI_INDEX
    def parser_general_TWSE(self, type, y=109, m=3, d=30):
        url = 'https://www.twse.com.tw/exchangeReport/{}?response=csv&date={}{}{}&type=ALL' \
            .format(typ, y+1911, '%02d'%m, '%02d'%d)
        soup = self.get_soup(url)

        submit_button = self.driver.find_element_by_link_text('CSV 下載')
        submit_button.click()

    def parser_STOCK_DAY_TWSE(self, type, y=109, m=3, d=30, stock_no=0000):
        url = 'https://www.twse.com.tw/exchangeReport/{}?response=csv&date={}{}{}&stockNo={}' \
            .format(typ, y+1911, '%02d'%m, '%02d'%d, stock_no)
        soup = self.get_soup(url)

        submit_button = self.driver.find_element_by_link_text('CSV 下載')
        submit_button.click()

    def parser_book_value(self, stock_num):
        url = 'https://statementdog.com/analysis/tpe/{}/nav'.format(stock_num)
        soup = self.get_soup(url)
        dataTable = soup.select('#dataTable')[0]
        date_list = dataTable.select('tr')[0].select('th')
        value_list = dataTable.select('tr')[1].select('td') #每股淨值
        assert len(date_list) == len(value_list), \
            'len of date_list{} and value_list{} is not equal in book value' \
            .format(len(date_list), len(value_list))
        for count in range(len(date_list)):
            date = date_list[count].text
            value = self.cancel_point(value_list[count].text)
            if self.is_value(date) and self.is_value(value):
                self.dict_all['quar'][date]['book_value'] = value
                #self.quar_report_dict[date]['book_value'] = value
            else:
                self.dict_all['quar'][date]['book_value'] = '-99999999'

    def parser_cash_flow(self, stock_num):
        url = 'https://statementdog.com/analysis/tpe/{}/cash-flow-statement'.format(stock_num)
        soup = self.get_soup(url)
        dataTable = soup.select('#dataTable')[0]
        date_list = dataTable.select('tr')[0].select('th')
        oper_cash_list = dataTable.select('tr')[3].select('td') #營業現金流
        free_cash_list = dataTable.select('tr')[7].select('td') #自由現金流
        assert len(date_list) == len(oper_cash_list) and \
            len(date_list) == len(free_cash_list), \
            'len of date_list:{} and oper_cash_list:{} and free_cash_list:{} is not equal in free cash' \
            .format(len(date_list), len(oper_cash_list), len(free_cash_list))
        for count in range(len(date_list)):
            date = date_list[count].text
            oper_cash_value = self.cancel_point(oper_cash_list[count].text)
            free_cash_value = self.cancel_point(free_cash_list[count].text)
            if self.is_value(date) and self.is_value(oper_cash_value) and self.is_value(free_cash_value):
                #self.quar_report_dict[date]['free_cash'] = free_cash_value + '000' #因為自由現金流單位是千
                #self.quar_report_dict[date]['oper_cash'] = oper_cash_value + '000'
                self.dict_all['quar'][date]['free_cash'] = free_cash_value + '000' #因為自由現金流單位是千
                self.dict_all['quar'][date]['oper_cash'] = oper_cash_value + '000'
            else:
                self.dict_all['quar'][date]['free_cash'] = '-99999999'
                self.dict_all['quar'][date]['oper_cash'] = '-99999999'

    def parser_profit_margin(self, stock_num):
        url = 'https://statementdog.com/analysis/tpe/{}/profit-margin'.format(stock_num)
        soup = self.get_soup(url)
        dataTable = soup.select('#dataTable')[0]
        date_list = dataTable.select('tr')[0].select('th')
        gross_profit_rate_list = dataTable.select('tr')[1].select('td') #毛利率
        oper_income_rate_list = dataTable.select('tr')[2].select('td') #營益率
        after_tax_income_rate_list = dataTable.select('tr')[4].select('td') #稅後淨利率
        assert len(date_list) == len(gross_profit_rate_list) and \
            len(date_list) == len(oper_income_rate_list) and \
            len(date_list) == len(after_tax_income_rate_list) and \
            'len of date_list:{} and gross_profit_rate_list:{} and \
            oper_income_rate_list:{} after_tax_income_rate_list:{} is not equal in profit margin' \
            .format(len(date_list), len(gross_profit_rate_list), len(oper_income_rate_list),  \
                len(after_tax_income_rate_list))
        for count in range(len(date_list)):
            date = date_list[count].text
            gross_profit_rate_val = self.cancel_point(gross_profit_rate_list[count].text)
            oper_income_rate_val = self.cancel_point(oper_income_rate_list[count].text)
            after_tax_income_rate_val = self.cancel_point(after_tax_income_rate_list[count].text)
            if self.is_value(date) and self.is_value(gross_profit_rate_val) and \
                self.is_value(oper_income_rate_val) and self.is_value(after_tax_income_rate_val):
                self.dict_all['quar'][date]['after_tax_income_rate'] = gross_profit_rate_val
                self.dict_all['quar'][date]['oper_income_rate'] = oper_income_rate_val
                self.dict_all['quar'][date]['after_tax_income_rate'] = after_tax_income_rate_val
                #self.quar_report_dict[date]['after_tax_income_rate'] = gross_profit_rate_val
                #self.quar_report_dict[date]['oper_income_rate'] = oper_income_rate_val
                #self.quar_report_dict[date]['after_tax_income_rate'] = after_tax_income_rate_val
            else:
                self.dict_all['quar'][date]['after_tax_income_rate'] = '-99999999'
                self.dict_all['quar'][date]['oper_income_rate'] = '-99999999'
                self.dict_all['quar'][date]['after_tax_income_rate'] = '-99999999'

    def parser_non_oper_income(self, stock_num): #業外收支佔稅前淨利比
        url = 'https://statementdog.com/analysis/tpe/{}/non-operating-income-to-profit-before-tax'.format(stock_num)
        soup = self.get_soup(url)
        dataTable = soup.select('#dataTable')[0]
        date_list = dataTable.select('tr')[0].select('th')
        value_list = dataTable.select('tr')[1].select('td') 
        assert len(date_list) == len(value_list), \
            'len of date_list{} and value_list{} is not equal in non oper income' \
            .format(len(date_list), len(value_list))
        for count in range(len(date_list)):
            date = date_list[count].text
            value = self.cancel_point(value_list[count].text)
            if self.is_value(date) and self.is_value(value):
                self.dict_all['quar'][date]['non_oper_income'] = value
                #self.quar_report_dict[date]['non_oper_income'] = value
            else:
                self.dict_all['quar'][date]['non_oper_income'] = '-99999999'

    def parser_roe(self, stock_num):
        url = 'https://statementdog.com/analysis/tpe/{}/roe-roa'.format(stock_num)
        soup = self.get_soup(url)
        dataTable = soup.select('#dataTable')[0]
        date_list = dataTable.select('tr')[0].select('th')
        value_list = dataTable.select('tr')[2].select('td')
        assert len(date_list) == len(value_list), \
            'len of date_list{} and value_list{} is not equal in ROE' \
            .format(len(date_list), len(value_list))
        for count in range(len(date_list)):
            date = date_list[count].text
            value = self.cancel_point(value_list[count].text)
            if self.is_value(date) and self.is_value(value):
                self.dict_all['quar'][date]['roe'] = value
                #self.quar_report_dict[date]['roe'] = value
            else:
                self.dict_all['quar'][date]['roe'] = '-99999999'

    def parser_oper_cash_flow_income_rate(self, stock_num):
        url = 'https://statementdog.com/analysis/tpe/{}/operating-cash-flow-to-net-income-ratio'.format(stock_num)
        soup = self.get_soup(url)
        dataTable = soup.select('#dataTable')[0]
        date_list = dataTable.select('tr')[0].select('th')
        value_list = dataTable.select('tr')[1].select('td')
        assert len(date_list) == len(value_list), \
            'len of date_list{} and value_list{} is not equal in oper cash flow income rate' \
            .format(len(date_list), len(value_list))
        for count in range(len(date_list)):
            date = date_list[count].text
            value = self.cancel_point(value_list[count].text)
            if self.is_value(date) and self.is_value(value):
                self.dict_all['quar'][date]['oper_cash_flow_income_rate'] = value
                #self.quar_report_dict[date]['oper_cash_flow_income_rate'] = value
            else:
                self.dict_all['quar'][date]['oper_cash_flow_income_rate'] = '-99999999'

    def parser_turnover_days(self, stock_num): #營運週轉天數
        url = 'https://statementdog.com/analysis/tpe/{}/turnover-days'.format(stock_num)
        soup = self.get_soup(url)
        dataTable = soup.select('#dataTable')[0]
        date_list = dataTable.select('tr')[0].select('th')
        receivable_list = dataTable.select('tr')[1].select('td') # 應週帳款（天數） receivable
        in_stock_list = dataTable.select('tr')[2].select('td') # 存貨（天數）  in stock
        oper_turnover_list = dataTable.select('tr')[3].select('td') # 營運週轉（天數）  oper turnover
        assert len(date_list) == len(receivable_list) and \
            len(date_list) == len(in_stock_list) and \
            len(date_list) == len(oper_turnover_list) and \
            'len of date_list:{} and receivable_list:{} and \
            in_stock_list:{} oper_turnover_list:{} is not equal in turnover days' \
            .format(len(date_list), len(receivable_list), len(in_stock_list),  \
                len(oper_turnover_list))
        for count in range(len(date_list)):
            date = date_list[count].text
            receivable_val = self.cancel_point(receivable_list[count].text)
            in_stock_val = self.cancel_point(in_stock_list[count].text)
            oper_turnover_val = self.cancel_point(oper_turnover_list[count].text)
            if self.is_value(date) and self.is_value(receivable_val) and \
                self.is_value(in_stock_val) and self.is_value(oper_turnover_val):
                self.dict_all['quar'][date]['receivable_days'] = receivable_val
                self.dict_all['quar'][date]['in_stock_days'] = in_stock_val
                self.dict_all['quar'][date]['oper_turnover_days'] = oper_turnover_val
                #self.quar_report_dict[date]['receivable_days'] = receivable_val
                #self.quar_report_dict[date]['in_stock_days'] = in_stock_val
                #self.quar_report_dict[date]['oper_turnover_days'] = oper_turnover_val
            else:
                self.dict_all['quar'][date]['receivable_days'] = '-99999999'
                self.dict_all['quar'][date]['in_stock_days'] = '-99999999'
                self.dict_all['quar'][date]['oper_turnover_days'] = '-99999999'

    def parser_mth_revenue_growth_rate(self, stock_num):
        url = 'https://statementdog.com/analysis/tpe/{}/monthly-revenue-growth-rate'.format(stock_num)
        soup = self.get_soup(url)
        dataTable = soup.select('#dataTable')[0]
        date_list = dataTable.select('tr')[0].select('th')
        value_list = dataTable.select('tr')[1].select('td')
        assert len(date_list) == len(value_list), \
            'len of date_list{} and value_list{} is not equal in monthly revenue growth rate' \
            .format(len(date_list), len(value_list))
        for count in range(len(date_list)):
            date = date_list[count].text
            value = self.cancel_point(value_list[count].text)
            if self.is_value(date) and self.is_value(value):
                self.dict_all['mth'][date]['mth_revenue_growth_rate'] = value
                #self.mth_report_dict[date]['mth_revenue_growth_rate'] = value
            else:
                self.dict_all['mth'][date]['mth_revenue_growth_rate'] = '-99999999'

    def parser_average_dividend_yield(self, stock_num):
        url = 'https://statementdog.com/analysis/tpe/{}/average-dividend-yield'.format(stock_num)
        soup = self.get_soup(url)
        dataTable = soup.select('#dataTable')[0]
        date_list = dataTable.select('tr')[0].select('th')
        value_list = dataTable.select('tr')[1].select('td')
        assert len(date_list) == len(value_list), \
            'len of date_list{} and value_list{} is not equal in average dividend yield' \
            .format(len(date_list), len(value_list))
        for count in range(len(date_list)):
            date = date_list[count].text
            value = self.cancel_point(value_list[count].text)
            if self.is_value(date) and self.is_value(value):
                self.dict_all['mth'][date]['average_dividend_yield'] = value
                #self.mth_report_dict[date]['average_dividend_yield'] = value
            else:
                self.dict_all['mth'][date]['average_dividend_yield'] = '-99999999'

    def parser_price_earnings_ratio(self, stock_num): #本益比
        url = 'https://statementdog.com/analysis/tpe/{}/pe'.format(stock_num)
        soup = self.get_soup(url)
        dataTable = soup.select('#dataTable')[0]
        date_list = dataTable.select('tr')[0].select('th')
        value_list = dataTable.select('tr')[1].select('td')
        assert len(date_list) == len(value_list), \
            'len of date_list{} and value_list{} is not equal in price earnings ratio' \
            .format(len(date_list), len(value_list))
        for count in range(len(date_list)):
            date = date_list[count].text
            value = self.cancel_point(value_list[count].text)
            if self.is_value(date) and self.is_value(value):
                self.dict_all['mth'][date] = copy.deepcopy({'price_earnings_ratio': value})
                #self.mth_report_dict[date] = copy.deepcopy({'price_earnings_ratio': value})
            else:
                self.dict_all['mth'][date] = copy.deepcopy({'price_earnings_ratio': '-99999999'})
                

    def parser_stock_holders(self, stock_num):
        url = 'http://norway.twsthr.info/StockHolders.aspx?stock={}'.format(stock_num)
        soup = self.get_soup_2(url)
        dataTable = soup.select('#Details')[0]
        for tr in dataTable.select('tr'):
            temp_list = tr.select('td')
            if len(temp_list) < 5 or not self.is_value(self.cancel_point(temp_list[2].text, '-')):
                continue
            date = temp_list[2].text.strip()
            avg_amount = self.cancel_point(temp_list[5].text) # 平均張數/人
            more_than_400 = temp_list[7].text # >400張大股東持有百分比
            self.dict_all['week'][self.cancel_point(date, '-')] = \
                copy.deepcopy({'avg_amount': avg_amount})
            self.dict_all['week'][self.cancel_point(date, '-')]['more_than_400'] = \
                more_than_400
            #self.week_report_dict[self.cancel_point(date, '-')] = \
            #    copy.deepcopy({'avg_amount': avg_amount})
            #self.week_report_dict[self.cancel_point(date, '-')]['more_than_400'] = \
            #    more_than_400

    def clear(self):
        self.dict_all = {'quar': {}, 'mth': {}, 'week': {}}

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml_bs_pth', type=str, required=False, \
        default= '/Users/Wiz/Desktop/Shield/data')
    parser.add_argument('--chrome_driver_path', type=str, required=False, \
        default= '/Users/Wiz/.wdm/chromedriver/2.46/mac64/chromedriver')
    parser.add_argument('--account', type=str, required=True, \
        default= '---')
    parser.add_argument('--password', type=str, required=True, \
        default= '---')
    return parser.parse_args()

if __name__ == '__main__':
    param = get_args()
    obj = Parser(param)
    obj.parser_Login_Selenium()
    for stock_num in [2002]:
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

        pass

    print (obj.week_report_dict, obj.quar_report_dict, obj.mth_report_dict)
        
