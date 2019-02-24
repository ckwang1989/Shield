#20190223 讀取現在的年份，好比是2019，就要跑2019.4Q~2017.1Q，先跑2019.4Q，如果資料夾內沒有，就可以爬，爬了以後發現沒有找到字串，
#就變成2019.3Q以此類推，......一直跑到2017.1Q

#分點

from urllib import request
from bs4 import BeautifulSoup
#import MySQLdb
import requests
import re
import smtplib
from email.header import Header
import datetime
import os

#gross_sales 營業收入毛額
#operating_income 營業利益 
#pre_tax_income 稅前淨利
#earning_per_share 每股盈餘
#cash_flow_operating 來自營運之現金流量
#cash_flow_investment 投資活動之現金流量
#price_book 股價淨值

import xml.etree.cElementTree as ET

def get_date():
	x = datetime.datetime.now()
	return [x.year,x.month,x.day]

class XMLGenerator:
    def xml_writer(self, save_full_path, item_list, value_list):
        annotation = ET.Element("annotation")
        for item_count in range(len(item_list)):
            obj = ET.SubElement(annotation,item_list[item_count])
            ET.SubElement(obj, "value").text = str(value_list[item_count])
        tree = ET.ElementTree(annotation)
        tree.write(save_full_path)

class Stock(XMLGenerator):
	def __init__(self):
		#naming rule：self.m_(想要的資料長度)_(項目名稱)_(絕對值還是成長率)_(count)_(thre)_(list)
		self.m_stock_number = 0
		self.m_price_list = [-1]

		self.m_gross_sales_month_growth_list = [-1] #月營收成長率
		self.m_want_gross_sales_month_growth_thre = -1
		self.m_want_gross_sales_month_growth_count_thre = -1

		self.m_operating_income_rate_list = [-1] #營利率
		self.m_want_operating_income_rate_growth_thre = -1
		self.m_want_operating_income_rate_growth_count_thre = -1

		self.m_operating_income_growth_list = [-1] #營業利益成長率
		self.m_want_operating_income_growth_growth_thre = -1
		self.m_want_operating_income_growth_growth_count_thre = -1

		self.m_pre_tax_income_rate_list = [-1] #稅前淨利率
		self.m_want_pre_tax_income_rate_growth_thre = -1
		self.m_want_pre_tax_income_rate_growth_count_thre = -1

		self.m_pre_tax_income_growth_list = [-1] #稅前淨利成長率
		self.m_want_pre_tax_income_growth_growth_thre = -1
		self.m_want_pre_tax_income_growth_growth_count_thre = -1

		self.m_earning_per_share_list = [-1] #EPS
		self.m_want_earning_per_share_growth_thre = -1
		self.m_want_earning_per_share_growth_count_thre = -1

		# 現金流量表
		self.m_cash_flow_lasted_quaurter = ""
		self.m_cash_flow_operating_list = [-1]
		self.m_cash_flow_investment_list = [-1]
		self.m_cash_flow_free_list = [-1]*8


		self.m_ROE1_list = [-1]
		self.m_ROE2_list = [-1]
		self.m_want_ROE_year_thre = -1

		self.m_url = 0
		self.m_soup = 0
		#Price-Book Ratio
	def set_initial(self,a_want_gross_sales_month):
		self.m_want_gross_sales_month = a_want_gross_sales_month

		self.m_want_gross_sales_month_growth_thre = -1
		self.m_want_gross_sales_month_growth_count_thre = -1

		self.m_operating_income_rate_list = [-1] #營利率
		self.m_want_operating_income_rate_growth_thre = -1
		self.m_want_operating_income_rate_growth_count_thre = -1

		self.m_operating_income_growth_list = [-1] #營業利益成長率
		self.m_want_operating_income_growth_growth_thre = -1
		self.m_want_operating_income_growth_growth_count_thre = -1

		self.m_pre_tax_income_rate_list = [-1] #稅前淨利率
		self.m_want_pre_tax_income_rate_growth_thre = -1
		self.m_want_pre_tax_income_rate_growth_count_thre = -1

		self.m_pre_tax_income_growth_list = [-1] #稅前淨利成長率
		self.m_want_pre_tax_income_growth_growth_thre = -1
		self.m_want_pre_tax_income_growth_growth_count_thre = -1

		self.m_earning_per_share_list = [-1] #EPS
		self.m_want_earning_per_share_growth_thre = -1
		self.m_want_earning_per_share_growth_count_thre = -1

		# 現金流量表
		self.m_cash_flow_lasted_quaurter = ""
		self.m_cash_flow_operating_list = [-1]
		self.m_cash_flow_investment_list = [-1]
		self.m_cash_flow_free_list = [-1]*8

		self.m_ROE1_list = [-1]
		self.m_ROE2_list = [-1]
		self.m_want_ROE_year_thre = -1

	def cancel_point(self, number_point):
		while(',' in number_point):
			number_point = number_point + '!'
			index = number_point.find(',')
			index_end = number_point.find('!')
			number_before = number_point[0:index].strip()
			number_after = number_point[(index+1):index_end].strip()
			number_point = number_before + number_after
		return int(number_point)

	def set_soup_from_url(self):
		response = request.urlopen(self.m_url)
		html = response.read()
		html = html.decode("Big5")
		self.m_soup = BeautifulSoup(html,'lxml')

	def get_all_item_count_from_soup(self,select_item,update_item):
		all_p=self.m_soup.select(select_item)
		p_count = 0
		for p in all_p:
			if p.get_text().find(update_item) != -1:
				p_count_temp = p_count
			p_count += 1
		return p_count_temp

	def get_lasted_quaurter_num(self, now_year):
		for quaurter_num in range(8,0,-1): #如果是年初，最新的財報有可能是去年底的，所以需要掃兩年
			quaurter_str = "{}.{}Q".format(now_year + (quaurter_num // 5)-1, (quaurter_num - 1) % 4 + 1)
			if quaurter_str in str(self.m_soup):
				return quaurter_str
				break
		return ""

	def update_income_statement(self):
		self.m_url = "http://jsjustweb.jihsun.com.tw/z/zc/zcq/zcq_{}.djhtm".format(self.m_stock_number)
		self.set_soup_from_url()
		select_item = 'td'
		update_item_list = ["營業利益","稅前淨利","每股盈餘"]
		for update_item in update_item_list:
			count = self.get_all_item_count_from_soup(select_item,update_item)
			all_p=self.m_soup.select('td')
			value_list = [all_p[count+1].get_text(),all_p[count+2].get_text(),all_p[count+3].get_text(),\
			all_p[count+4].get_text(),all_p[count+5].get_text(),all_p[count+6].get_text(),\
			all_p[count+7].get_text(),all_p[count+8].get_text()]
			if update_item == "營業利益":
				self.m_operating_income_list = value_list
			if update_item == "稅前淨利":
				self.m_pre_tax_income = value_list
			if update_item == "每股盈餘":
				self.m_earning_per_share_list = value_list

	def update_cash_flows_statement(self, now_year):
		self.m_url = "http://jsjustweb.jihsun.com.tw/z/zc/zc3/zc3_{}.djhtm".format(self.m_stock_number)
		self.set_soup_from_url()
		self.m_cash_flow_quaurter = self.get_lasted_quaurter_num(now_year)
		select_item = 'td'
		update_item_list = ["來自營運之現金流量","投資活動之現金流量"]
		for update_item in update_item_list:
			value_list = list()
			count = self.get_all_item_count_from_soup(select_item,update_item)
			all_p=self.m_soup.select('td')
			for i in range(1,9):
				value_list.append(self.cancel_point(all_p[count+i].get_text()))
			if update_item == "來自營運之現金流量":
				self.m_cash_flow_operating_list = value_list
			if update_item == "投資活動之現金流量":
				self.m_cash_flow_investment_list = value_list
		for count in range(len(self.m_cash_flow_investment_list)):
			self.m_cash_flow_free_list[count] = self.m_cash_flow_operating_list[count] + self.m_cash_flow_investment_list[count]

	def update_inventory_ratio_statement(self):
		self.m_url = "http://jsjustweb.jihsun.com.tw/z/zc/zcr/zcr_{}.djhtm".format(self.m_stock_number)
		self.set_soup_from_url()
		select_item = 'td'
		update_item_list = ["ROE(A)─稅後","ROE(B)─常續利益","營業利益率","稅前淨利率"]
		for update_item in update_item_list:
			count = self.get_all_item_count_from_soup(select_item,update_item)
			all_p=self.m_soup.select('td')
			value_list = [all_p[count+1].get_text(),all_p[count+2].get_text(),all_p[count+3].get_text(),\
			all_p[count+4].get_text(),all_p[count+5].get_text(),all_p[count+6].get_text(),\
			all_p[count+7].get_text(),all_p[count+8].get_text()]
			if update_item == "ROE(A)─稅後":
				self.m_ROE1_list = value_list
			if update_item == "ROE(B)─常續利益":
				self.m_ROE2_list = value_list
			if update_item == "營業利益率":
				self.m_operating_income_ratio_list = value_list
			if update_item == "稅前淨利率":
				self.m_pre_tax_income_ratio_list = value_list

	def update_gross_sales_month_statement(self):
		self.m_url = "http://jsjustweb.jihsun.com.tw/z/zc/zch/zch_{}.djhtm".format(self.m_stock_number)
		self.set_soup_from_url()
		select_item = 'td'
		update_item_list = ["107/04"]
		for update_item in update_item_list:
			count = self.get_all_item_count_from_soup(select_item,update_item)
			all_p=self.m_soup.select('td')
			value_list = [all_p[count+4].get_text()]
			print (value_list)



# 2018.3Q
stock_number_list = [2330]
now_year,now_month,now_day = get_date()

task_list = list()
if now_month in [4,5,8,10]:
	task_list.append("update_quaurter")
if 5 <= now_day <= 15:
	task_list.append("update_month")
task_list.append("update_day")

stock = Stock()
stock.set_initial(1)

base_path = "/Users/Wiz/Desktop/future2/database/"

for stock_num in stock_number_list:
	stock.m_stock_number = stock_num
	#stock.update_income_statement()  		#損益表
	stock.update_cash_flows_statement(now_year)  	#現金流量表
	#stock.update_inventory_ratio_statement()#財務比率表
	#stock.update_gross_sales_month_statement() #月營收
	#要確認是不是lasted q是統一的，然後看是不是都有缺，建立quaurter_num_list
	quaurter_num_list = ["2018.3Q", "2018.2Q"]
	for task in ["Cash Flow Statement"]:
		for quaurter_count in range(len(quaurter_num_list)):
			quaurter_num = quaurter_num_list[quaurter_count]
			path = os.path.join(base_path, task, str(stock_num), quaurter_num+'.xml')
			print (path, quaurter_count)
			stock.xml_writer(path, quaurter_num_list[quaurter_count:quaurter_count+1], \
				stock.m_cash_flow_free_list[quaurter_count:quaurter_count+1])



#for quaurter_num in range(8,0,-1):
#	quaurter_str = "{}.{}Q".format(now_year + (quaurter_num // 5)-1, (quaurter_num - 1) % 4 + 1)







assert False














def sent_email(msg):
	print ("sent")
	#server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("catlikesiyas@gmail.com", "b27678352")
	sent_to_receiver(msg)
	server.quit()

def sent_to_receiver(msg):
	f_receivers = open(r'/home/ckwang/stock/fs_receivers')
	for fs_receivers in f_receivers.readlines():
		receivers = str(fs_receivers.strip())
		server.sendmail("catlikesiyas@gmail.com", receivers, msg)

def get_eight_quaurter(financial_statement):
	####################get the eight quaurter####################
	index = financial_statement.find(fs_item)	#the index of value
	sub_financial_statement = financial_statement[index:index+400]
	sub_start = sub_financial_statement.find('<td class')
	sub_end = sub_financial_statement.find('</tr>')
	sub_sub_fs = sub_financial_statement[sub_start:sub_end].strip()
	value = ""
	value_list = []
	flag_break = 0
	a = sub_sub_fs.split('\n')
	for i in range(0,8):
		try:
			info = a[i]
			relink = '<td class="(.*)">(.*)</td>'
			cinfo = re.findall(relink,info)
			for mm in cinfo:
				pass
			if((mm[1].find(',')) >= 0):
				number_no_point = cancel_point(mm[1])
				value_list.append(number_no_point)
				value = value + str(number_no_point) + " "
			elif((mm[1].find('/')) >= 0):
				flag_break = 1							#if the value is N/A
			elif(mm[1] == '0'):
				value_list.append('0.001')
				value = value + ('0.001') + " "				
			else:
				value_list.append(mm[1])
				value = value + str(mm[1]) + " "
		except:
			flag_break = 1	# if only have seven quaurter
	return value_list,value,flag_break

def cancel_point(number_point):
	number_point = number_point + '!'
	index = number_point.find(',')
	index_end = number_point.find('!')
	number_before = number_point[0:index].strip()
	number_after = number_point[(index+1):index_end].strip()
	number_point = number_before + number_after
	return number_point

def get_sales_growth(financial_statement,sales_progress_times):
	index = financial_statement.find(fs_item)	#the index of value
	sub_financial_statement = financial_statement[index:index+11000]
	#print sub_financial_statement
	sub_start = sub_financial_statement.find('<tr><td class=')
	sub_end = sub_financial_statement.find('</table>')
	sub_sub_fs = sub_financial_statement[sub_start:sub_end].strip()
	value = ""
	value_list = []
	flag_break = 0
	a = sub_sub_fs.split('\n')	
	for count in range(0,sales_progress_times):
		try:
			info = a[count]

			relink = '<tr><td class="(.*)">(.*)</td><td class="(.*)">(.*)</td><td class="(.*)">(.*)%</td><td class="(.*)">(.*)</td><td class="(.*)">(.*)%</td><td class="(.*)">(.*)</td><td class="(.*)">(.*)%</td></tr>'
			cinfo = re.findall(relink,info)
			for mm in cinfo:
				pass
			if(mm[1] == '0'):
				value_list.append('0.001')
				value = value + ('0.001') + " "	
			else:	
				value_list.append(mm[9])
				value = value + str(mm[9]) + " "
		except:
			flag_break = 1	# if the web have something wrong
	return value_list,value,flag_break

def get_per(financial_statement,flag_getprice_price_or_amount,price_amount):
	flag_break = 0
	index = financial_statement.find(fs_item)	#the index of value
	sub_financial_statement = financial_statement[index+10:index+3000] 
	sub_start = sub_financial_statement.find('<td class')	
	sub_end = sub_financial_statement.find('<tr><td class="cr">')
	if((sub_start == -1) | (sub_end == -1) ):
		#print "error"
		flag_break = 1
	else :
		sub_fs = sub_financial_statement[sub_start:sub_end].strip()	
		relink = '<td class="(.*)">(.*)</td><td class="(.*)">(.*)</td><td class="(.*)">(.*)</td><td class="(.*)">(.*)</td><td class="(.*)">(.*)</td><td class="(.*)">(.*)</td><td class="(.*)">(.*)</td><td class="(.*)">(.*)</td>'
		cinfo = re.findall(relink,sub_fs)
		try:
			for mm in cinfo:
				#print mm
				pass
		except:
			flag_break = 1	# if the web have something wrong
		if(flag_getprice_price_or_amount == 0):
			price_amount.append(float(mm[1]))
			price_amount.append(float(mm[3]))
		elif(flag_getprice_price_or_amount == 1):
			price_amount.append(float(mm[1]))
			price_amount.append(float(mm[3]))
		else:
			#print "error"
			flag_break = 1
		flag_getprice_price_or_amount = flag_getprice_price_or_amount + 1
		if(flag_getprice_price_or_amount < 2):
			get_per(sub_financial_statement,flag_getprice_price_or_amount,price_amount)
	return price_amount,flag_break			#price_amount [0] = price, [1] = three_day_average_price, [2] = amount, [3] = three_day_average_amount

def get_yields(financial_statement,flag_break,yields_list):
	#print financial_statement
	index = financial_statement.find(fs_item)	#the index of value
	#print index
	sub_financial_statement = financial_statement[index+10:index+3000]
	sub_start = sub_financial_statement.find('<td class')	
	sub_end = sub_financial_statement.find('</td>')
	sub_fs = sub_financial_statement[sub_start:sub_end].strip()
	#print sub_fs
	#relink = '<td class="(.*)">(.*)</td><td class="(.*)">(.*)</td><td class="(.*)">(.*)</td><td class="(.*)">(.*)</td><td class="(.*)">(.*)</td><td class="(.*)">(.*)</td><td class="(.*)">(.*)</td><td class="(.*)">(.*)</td>'
	relink = '<td class="(.*)">(.*)%'
	#<td class="t3n1">3.81%
	cinfo = re.findall(relink,sub_fs)
	try:
		for mm in cinfo:
			pass
	except:
		flag_break = 1	# if the web have something wrong
	yields_list.append(float(mm[1]))
	#print yields_list
	return yields_list,flag_break			#price_amount [0] = price, [1] = three_day_average_price, [2] = amount, [3] = three_day_average_amount
	    
	
how_many_item = 12###################################################################################################################################################################################
print_error_flag = 0##################################################################


#1
roe = 15
#2
after_duty_growth = 1  ###1
#3
work_money_after_duty = 1 ###2		#at least two q 
work_money_after_duty_percet = 0.8
#4 sales_progress
sales_progress_times = 2   ###2
sales_progress_percet = 0

#5
afterduty_rate_times = 1
afterduty_rate_growth_percet = 1   ###1

free_money_number = 4
original_income_percet = 0.7
original_income_times = 2
#10 eps_progress
eps_progress_times = 1		###1
eps_progress_percet = 1

#12 per
per = 12
amount_three_day_average = 100			###3  1000


server = smtplib.SMTP('smtp.gmail.com', 587)			#for sent e-mail
msg = ''
item_count = 1
fs_number_last = ""
flag_full = 0 #0->don't have eight item, 1->have eight item
#1=ROE 2=after_duty_growth 3=workmoney 4=after_duty 5=free_money 6=income 7=extern_income
########################################which stock########################################
f_number = open(r'/home/ckwang/stock/fs_number')
for fs_number in f_number.readlines():
	#item_count = 1
	fs_number = fs_number.strip()
	fs_number = str(fs_number)
	fs_number = fs_number[0:4]
	#print fs_number
	write_string = fs_number + "\n"
	if(item_count >= 8):
		print (fs_number_last + " " + str(item_count) +"\n\n\n")
	fs_number_last = fs_number
	item_count = 1
	f = open(r'/home/ckwang/stock/fs_item')
	########################################whick item########################################
	for fs_item in f.readlines():
		fs_item = fs_item.strip()
		#financial_statement = str(BeautifulSoup(urllib2.urlopen('http://jsjustweb.jihsun.com.tw/z/zc/zca/zca_1513.djhtm').read()))
		try:
			if ((item_count == 3) | (item_count == 4) | (item_count == 5)):								#ROE,after_duty_growth
				financial_statement = str(BeautifulSoup(urllib2.urlopen('http://jsjustweb.jihsun.com.tw/z/zc/zcr/zcr_' + str(fs_number) +'.djhtm').read()))
			elif((item_count == 1)):							#original_industry
				financial_statement = str(BeautifulSoup(urllib2.urlopen('http://jsjustweb.jihsun.com.tw/z/zc/zcq/zcq_' + str(fs_number) +'.djhtm').read()))
			elif(item_count == 6):													#sales
				financial_statement = str(BeautifulSoup(urllib2.urlopen('http://jsjustweb.jihsun.com.tw/z/zc/zch/zch_' + str(fs_number) +'.djhtm').read()))
			elif((item_count == 7) | (item_count == 8) | (item_count == 9)):		#workmoney,after_duty,free_money,eight_freemoney
				financial_statement = str(BeautifulSoup(urllib2.urlopen('http://jsjustweb.jihsun.com.tw/z/zc/zc3/zc3_' + str(fs_number) +'.djhtm').read()))
			elif((item_count == 10) | (item_count == 11)):							#original_industry
				financial_statement = str(BeautifulSoup(urllib2.urlopen('http://jsjustweb.jihsun.com.tw/z/zc/zcq/zcq_' + str(fs_number) +'.djhtm').read()))
			elif(item_count == 2):													#per
				financial_statement = str(BeautifulSoup(urllib2.urlopen('http://www.cnyes.com/twstock/Technical/' + str(fs_number) +'.htm').read()))											
			elif(item_count == 12):												
				financial_statement = str(BeautifulSoup(urllib2.urlopen('http://jsjustweb.jihsun.com.tw/z/zc/zca/zca_' + str(fs_number) +'.djhtm').read()))
																		#https://tw.stock.yahoo.com/d/s/company_1215.html
			else:														#'http://www.cnyes.com/twstock/Technical/1215.htm
				break
		except:
			if(print_error_flag == 1):
				print ("script is crashed in loading website")
			break 	#sometimes script will be crash in loading website
		####################if this stock don't have complete fs, break####################
		if(len(financial_statement)<7000):
			if(print_error_flag == 1):
				print ("error in item_count = " + str(item_count) + "because website has some error")
			break
		####################get the eight quaurter####################
		if(item_count == 6):
			value_list,value,flag_break = get_sales_growth(financial_statement,sales_progress_times)
		elif(item_count == 12):
			yields_list = []
			yields_list,flag_break = get_yields(financial_statement,0,yields_list)
		elif(item_count == 2):
			price_amount_list = []
			price_amount_list,flag_break = get_per(financial_statement,0,price_amount_list)
		else:
			value_list,value,flag_break = get_eight_quaurter(financial_statement)
		if(flag_break == 1):
			if(print_error_flag == 1):
				print ("error in item_count = " + str(item_count) + "because this financial statement is not release finish")
			flag_break ==0
			break
		####################calculate of the eight quaurter item####################
		#eps_progress
		if(item_count == 1):
			item_count_9_counter = 0
			eps = []
			eps_growth_rate = []
			for i in range(0,8):
				eps.append(float(value_list[i]))
				if(i >= 4):
					if(float(value_list[i]) == 0):
						value_list[i] = 0.001
					#print (value_list)
					eps_growth_rate.append(float(value_list[i-4]) / float(value_list[i]))		#afterduty_rate_growth_rate < 1 in normal case
			for i in range(0,eps_progress_times):
				if(((value_list[i] > 0)&(value_list[i+4] <0))|((eps_growth_rate[i] > eps_progress_percet)&(value_list[i] > 0))):    #(positive v.s negitive) or (positive_high v.s positive_low)
					item_count_9_counter = item_count_9_counter + 1
		#	print item_count_9_counter
			#print "eps_progress_times:" + str(item_count_9_counter)  ######################## 
			if(item_count_9_counter < eps_progress_times):
				break
		#per
		elif(item_count == 2):
			per_cal = (price_amount_list[0] / (eps[0] + eps[1] + eps[2] + eps[3]))
			#print "per_cal:" + str(per_cal)  ######################## 
			amount_three_day_average_cal = price_amount_list[3]
			#print "amount_three_day_average_cal:" + str(amount_three_day_average_cal)  ######################## 
			today_price = price_amount_list[0]
			if(per_cal > per):
				break
			elif(price_amount_list[3] < amount_three_day_average):
				break
		#ROE
		elif(item_count == 3):
			if((float(value_list[0])+float(value_list[1])+float(value_list[2])+float(value_list[3]))<roe):
				break
		#After duty
		elif(item_count == 4):
			if(after_duty_growth == 1):
				if(float(value_list[0])<0):
					break
			elif(after_duty_growth == 2):
				if((float(value_list[0])<0) | (float(value_list[1])<0)):
					break
			elif(after_duty_growth == 3):
				if((float(value_list[0])<0) | (float(value_list[1])<0) | (float(value_list[2])<0)):
					break
			else:
				if((float(value_list[0])<0) | (float(value_list[1])<0) | (float(value_list[2])<0) | (float(value_list[3])<0)):
					break
		#afterduty_rate
		elif(item_count == 5):
			item_count_3_counter = 0
			afterduty_rate = []
			afterduty_rate_growth_rate = []
			for i in range(0,8):
				afterduty_rate.append(float(value_list[i]))
				if(i >= 4):
					afterduty_rate_growth_rate.append(float(value_list[i-4]) / float(value_list[i]))		#afterduty_rate_growth_rate < 1 in normal case
			for i in range(0,afterduty_rate_times):
				if(((value_list[i] > 0)&(value_list[i+4] <0))|((afterduty_rate_growth_rate[i] > afterduty_rate_growth_percet)&(value_list[i] > 0))):    #(positive v.s negitive) or (positive_high v.s positive_low)
					item_count_3_counter = item_count_3_counter + 1
		#	print item_count_3_counter
			if(item_count_3_counter < afterduty_rate_times):
				break
				#sales
		elif(item_count == 6):
			sales_progress = ""
			flag_break_count = 0
			#print "month_sales_progress:"
			for i in range(0,sales_progress_times):
				#print (float(value_list[i]))
				if(float(value_list[i]) < sales_progress_percet):
					flag_break_count = 1
			if(flag_break_count == 1):
				flag_break_count = 0
				#print "month_sales_progress:" + str(value_list)
				break
			sales_progress = value
		#workmoney_divide_afterduty_1
		elif(item_count == 7):
			work_money = []
			for i in range(0,8):
				work_money.append(float(value_list[i]))
		#workmoney_divide_afterduty_2
		elif(item_count == 8):
			work_money_divide_after_duty = []
			#work_money_divide_after_duty = work_money / after_duty
			for i in range(0,8):
				work_money_divide_after_duty.append((work_money[0]) / (float(value_list[i])))
			if(work_money_after_duty == 1):
				if((work_money_divide_after_duty[0]) < work_money_after_duty_percet):
					print ("work_money_divide_after_duty:" + str(work_money_divide_after_duty))
					break
			elif(work_money_after_duty == 2):
				if(((work_money_divide_after_duty[0]) < work_money_after_duty_percet)|((work_money_divide_after_duty[1]) < work_money_after_duty_percet)):
					print ("work_money_divide_after_duty:" + str(work_money_divide_after_duty))
					break
			elif(work_money_after_duty == 3):
				if(((work_money_divide_after_duty[0]) < work_money_after_duty_percet)|((work_money_divide_after_duty[1]) < work_money_after_duty_percet)|((work_money_divide_after_duty[2]) < work_money_after_duty_percet)):
					break
			elif(work_money_after_duty == 0):
				item_count = item_count + 1
				continue
			else:
				if(((work_money_divide_after_duty[0]) < work_money_after_duty_percet)|((work_money_divide_after_duty[1]) < work_money_after_duty_percet)|((work_money_divide_after_duty[2]) < work_money_after_duty_percet)|((work_money_divide_after_duty[3]) < work_money_after_duty_percet)):
					break
		#free money
		elif(item_count == 9):
			free_money = []
			#free_money = work_money - invenst_money
			for i in range(0,8):
				free_money.append((work_money[i]) - (float(value_list[i])))
			#print fs_number + " free_money:" + str(free_money) ###################################################
			if(not((((free_money[0]>0)+(free_money[1]>0)+(free_money[2]>0)+(free_money[3]>0)+(free_money[4]>0)+(free_money[5]>0)+(free_money[6]>0)+(free_money[7]>0))>free_money_number)and(free_money[0]+free_money[1]+free_money[2]+free_money[3])and(free_money[0]>0))):
				break
		#operating_income
		elif(item_count == 10):
			operating_income = []
			for i in range(0,8):
				operating_income.append(float(value_list[i]))
		#external_income
		elif(item_count == 11):
			#print "enter 9"
			original_income = []
			external_income = []
			#original_income = operating_income / (operating_income + external_income)
			for i in range(0,8):
				if((float(value_list[i])) < 0):
					original_income.append("external_income loss money")
				else:
					original_income.append(operating_income[i] / (operating_income[i] + (float(value_list[i]))))
			if(original_income_times == 1):
				if((original_income[0]) < original_income_percet):
					print ("original_income1:" + str(original_income[0])) ###################################
					break
			elif(original_income_times == 2):
				if(((original_income[0]) < original_income_percet)|((original_income[1]) < original_income_percet)):
					print ("original_income2:" + str(original_income[0]) + " " + str(original_income[1])) ###################################
					break
			elif(original_income_times == 3):
				if(((original_income[0]) < original_income_percet)|((original_income[1]) < original_income_percet)|((original_income[2]) < original_income_percet)):
					break
			else:
				if(((original_income[0]) < original_income_percet)|((original_income[1]) < original_income_percet)|((original_income[2]) < original_income_percet)|((original_income[3]) < original_income_percet)):
					break
		#yield
		elif(item_count == 12):
			print ("sales_progress:" + str(sales_progress))
			print ("yield_list:" + str(yields_list[0]) + "%")
			print ("amount_three_day_average_cal:" + str(amount_three_day_average_cal))  ########################
			print ("per_cal:" + str(per_cal))  ######################## 

		else:
			print ("error" + "\n" + "\n" + "\n")
		####################calculate of the eight quaurter item####################
		if((item_count == 3)|(item_count == 4)|(item_count == 6)):
			write_string = write_string + str(fs_item) + value + "\n"
		item_count = item_count + 1
	f.close()
	########################################whick item########################################
	ff = open("/home/ckwang/stock/fs_result","a")
	#print item_count
	if(item_count > how_many_item):
		write_string = write_string + "wm_ad: " + str(work_money_divide_after_duty) + "\n" + "original: " + str(original_income) \
		+ "\n" + "sales_progress: " + sales_progress + "\n" + "per_cal: " + str(per_cal) + "\n" + "amount_three_day_average_cal: " + str(amount_three_day_average_cal) \
		+ "\n" + "today_price: " + str(today_price) + "\n\n" 
		ff.write(write_string)
		print (write_string)
		msg = msg + write_string
	flag_full = 0
	ff.close()
f_number.close()
sent_email(msg)
print ("end")

