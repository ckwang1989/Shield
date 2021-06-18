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

from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager

import argparse

import copy

from selenium.webdriver.support.ui import Select
import pyautogui

from PIL import Image

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
        self.pyautogui = pyautogui.screenshot()
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
        account = self.account
        password = self.password
        if self.driver == None:
            self.Init_Browser()
        self.driver.get("https://statementdog.com/users/sign_in")
        self.driver.find_element_by_id("user_email").send_keys(account)
        self.driver.find_element_by_id("user_password").send_keys(password)
        self.driver.find_element_by_class_name("submit-btn").click()

    def get_soup(self, url):
        '''
        get_soup: get soup from url onlt for quar
            Input:  
                url
            Output:
                soup
        '''
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 1)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, \
            'sheet-interval-current-option-text')))
        time.sleep(2)
        temp = self.driver.find_element_by_xpath(\
            '//*[@id="report_title"]/table/tbody/tr/td[1]/ul/li[4]')
        self.driver.execute_script("arguments[0].click();", temp)

        s1 = Select(self.driver.find_element_by_xpath(\
            '//*[@id="report_title"]/table/tbody/tr/td[1]/div[2]/div[1]/select[1]'))
        s1.select_by_value('2001')
        
        self.driver.find_element_by_xpath('//*[@id="report_title"]/table/tbody/tr/td[1]/div[2]/div[3]/div').click()
        #self.driver.execute_script("arguments[0].click();", temp)

        time.sleep(2)
        soup = (BeautifulSoup(self.driver.page_source,"lxml"))
        return soup
#//*[@id="report_title"]/table/tbody/tr/td[1]/div[2]/div[1]/select[1]/option[1]
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

    def get_soup_4(self, url):
        self.driver.get(url)
#        wait = WebDriverWait(self.driver, 1)
        time.sleep(1)

    def get_soup_5(self, url):
        # https://stackoverflow.com/questions/52433411/python-selenium-move-by-offset-doesnt-work
        self.driver.get(url)
        time.sleep(3)
        self.driver.execute_script('window.scrollBy(0, 1000)')
        time.sleep(2)

    def parser_eps(self, stock_num):
        self.stock_num = stock_num
        url = 'https://statementdog.com/analysis/tpe/{}/eps'.format(stock_num)
        soup = self.get_soup(url)
        dataTable = soup.select('#dataTable')[0]
        date_list = dataTable.select('tr')[0].select('th')
        value_list = dataTable.select('tr')[1].select('td') #每股盈餘
        assert len(date_list) == len(value_list), \
            'len of date_list{} and value_list{} is not equal in eps' \
            .format(len(date_list), len(value_list))
        for count in range(len(date_list)):
            date = date_list[count].text
            value = self.cancel_point(value_list[count].text)
            if self.is_value(date) and self.is_value(value):
                self.dict_all['quar'][date] = copy.deepcopy({'eps': value})
                #self.quar_report_dict[date] = copy.deepcopy({'eps': value})
            else:
                self.dict_all['quar'][date] = copy.deepcopy({'eps': '-99999999'})

    def parser_price(self, stock_num):
        url = 'http://jsjustweb.jihsun.com.tw/z/zc/zca/zca_{}.djhtm'.format(stock_num)
        soup = self.get_soup_2(url)
        table = soup.find_all("table", class_="t01")
        if len(table) == 0: 
            return 0, 0, 0
        else:
            table = table[0]
        volumes = []

        table_tr_row1 = table.find_all("tr")[1]
        tmp = self.cancel_point(table_tr_row1.find_all("td")[1].text)
        price = float(tmp) if self.is_value(tmp) else -1

        table_tr_row3 = table.find_all("tr")[3]
        tmp = self.cancel_point(table_tr_row3.find_all("td")[1].text)
        pe = float(tmp) if self.is_value(tmp) else -1

        tmp = self.cancel_point(table_tr_row3.find_all("td")[7].text)
        volume = float(tmp) if self.is_value(tmp) else -1
        return price, pe, volume

    def parser_investment_trust(self, stock_num, i=0):
        # 日期	外資	投信	自營商	單日合計	外資	投信	自營商	單日合計	外資	三大法人
        url = 'http://jsjustweb.jihsun.com.tw/z/zc/zcl/zcl_{}.djhtm'.format(stock_num)
        soup = self.get_soup_2(url)
        table = soup.find_all("table", class_="t01")
        if len(table) == 0:
            return {}
        table = table[0]
#        if len(table.find_all("tr")) <= 7+i:
#            return {}
        table_tr = table.find_all("tr")[7+i]
        
        date = table_tr.find_all("td")[0].text
        if not self.is_value(self.cancel_point(table_tr.find_all("td")[1].text)):
            return {}
        foreign_inv_volume = int(self.cancel_point(table_tr.find_all("td")[1].text))
        inv_trust_volume = int(self.cancel_point(table_tr.find_all("td")[2].text))
        foreign_inv_volume_total = int(self.cancel_point(table_tr.find_all("td")[5].text))
        inv_trust_volume_total = int(self.cancel_point(table_tr.find_all("td")[6].text))
        
        institutional_invest_volume_total = int(self.cancel_point(table_tr.find_all("td")[8].text))
        institutional_invest_volume_percent = float(table_tr.find_all("td")[10].text[:-1])
        
        all_volume = 0 if institutional_invest_volume_percent == 0 else institutional_invest_volume_total / institutional_invest_volume_percent
        inv_trust_volume_percent = 0 if all_volume == 0 else inv_trust_volume_total / all_volume
        return {'date': date, \
            'foreign_inv_volume': foreign_inv_volume, \
            'inv_trust_volume': inv_trust_volume, \
            'foreign_inv_volume_total': foreign_inv_volume_total, \
            'institutional_invest_volume_total': institutional_invest_volume_total, \
            'inv_trust_volume_total': inv_trust_volume_total, \
            'institutional_invest_volume_percent': institutional_invest_volume_percent, \
            'all_volume': all_volume, \
            'inv_trust_volume_percent': inv_trust_volume_percent}
    
    def parser_K_directly(self):
        # https://weikaiwei.com/finance/python-stock-crawler/
        import requests
        import pandas as pd

        dates = [20200201, 20200101, 20191201]
        stockNo = 2330
        url_template = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date={}&stockNo={}"

        for date in dates :
            url = url_template.format(date, stockNo)
            file_name = "{}_{}.csv".format(stockNo, date)
            
            data = pd.read_html(requests.get(url).text)[0]
            data.columns = data.columns.droplevel(0)
            data.to_csv(file_name, index=False)
        input('w')

    def parser_K_screenshot(self, stock_num, p):
        def center_crop(im_ori, w, h, ratios):
            x1_new, y1_new, x2_new, y2_new = int(w*ratios[0]), int(h*ratios[1]), int(w*ratios[2]), int(h*ratios[3])
            return im_ori.crop((x1_new, y1_new, x2_new, y2_new))
            
        w, h = self.pyautogui.size
#        h = int(h*0.75)
#        im_new = Image.new(mode = "RGB", size = (h*4, h*1))
        im_new = None
        ratios = [0.35, 0.08, 0.78, 0.85]
        for i_state, state in enumerate(['tech_index', 'W', 'zch', 'institutional_invest', 'main_force', 'main_force_5', 'main_force_10', 'share_holder']):
            if state == 'D':
#                ratios = [0.4, 0.2, 0.8, 0.9]
                url = 'http://jsjustweb.jihsun.com.tw/z/zc/zcw/zcw1_{}.djhtm'.format(stock_num)
            elif state == 'W':
#                ratios = [0.4, 0.2, 0.8, 0.9]
                url = f'http://jsjustweb.jihsun.com.tw/Z/ZC/ZCW/ZCW_{stock_num}_{state}.djhtm'
            elif state == 'zcr':
#                ratios = [0.4, 0.2, 0.6, 0.8]
                url = f'http://jsjustweb.jihsun.com.tw/z/zc/zcr/zcr_{stock_num}.djhtm'
            elif state == 'zch':
#                ratios = [0.4, 0.2, 0.6, 0.8]
                url = f'http://jsjustweb.jihsun.com.tw/z/zc/zch/zch_{stock_num}.djhtm'
            elif state == 'news':
#                ratios = [0.4, 0.2, 0.6, 0.8]
                url = f'http://jsjustweb.jihsun.com.tw/z/zc/zcv/zcv_{stock_num}_E_1.djhtm'
            elif state == 'main_force':
#                ratios = [0.4, 0.2, 0.6, 0.8]
                url = f'http://jsjustweb.jihsun.com.tw/z/zc/zco/zco_{stock_num}.djhtm'
            elif state == 'main_force_5':
#                ratios = [0.4, 0.2, 0.6, 0.8]
                url = f'http://jsjustweb.jihsun.com.tw/z/zc/zco/zco_{stock_num}_2.djhtm'
            elif state == 'main_force_10':
#                ratios = [0.4, 0.2, 0.6, 0.8]
                url = f'http://jsjustweb.jihsun.com.tw/z/zc/zco/zco_{stock_num}_3.djhtm'
            elif state == 'institutional_invest':
#                ratios = [0.4, 0.2, 0.6, 0.8]
                url = f'http://jsjustweb.jihsun.com.tw/z/zc/zcl/zcl.djhtm?a={stock_num}&b=4'
            elif state == 'tech_index':
#                ratios = [0.5, 0.0, 1.0, 0.8]
                url = f'https://www.wantgoo.com/stock/{stock_num}/technical-chart'
            elif state == 'share_holder':
                url = f'https://norway.twsthr.info/StockHolders.aspx?stock={stock_num}'
            else:
                pass   
            if state == 'tech_index':
                soup = self.get_soup_5(url)
            elif state == 'share_holder':
                soup = self.get_soup_4(url)
                self.driver.find_element_by_xpath('//*[@id="liC3"]').click()
                time.sleep(1)
            else:
                soup = self.get_soup_4(url)
            myScreenshot = pyautogui.screenshot()
            myScreenshot_crop = center_crop(myScreenshot, w, h, ratios)
            new_w, new_h = myScreenshot_crop.size
            if im_new == None:
                im_new = Image.new(mode = "RGB", size = (new_w*4, new_h*2))
                im_new.paste(myScreenshot_crop, (new_w*int(i_state%4), new_h*int(i_state/4)))
            else:
                im_new.paste(myScreenshot_crop, (new_w*int(i_state%4), new_h*int(i_state/4)))
            
#            myScreenshot.save(os.path.join(os.path.dirname(p), f'{state}.png')
        im_new.save(p)


        


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
    for stock_num in [4152]:
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
        
