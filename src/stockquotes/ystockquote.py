#!/usr/bin/env python
#
#  Copyright (c) 2007-2008, Corey Goldberg (corey@goldb.org)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.

import urllib
from BeautifulSoup import BeautifulSoup

"""
This is the "ystockquote" module.

This module provides a Python API for retrieving stock data from Yahoo Finance.

sample usage:
>>> import ystockquote
>>> print ystockquote.get_price('GOOG')
529.46
"""

def __request(symbol, stat):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    return urllib.urlopen(url).read().strip().strip('"')

def get_all(symbol):
  
	values = __request(symbol, 'l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7').split(',')
	data = {}
	data['price'] = values[0]
	data['change'] = values[1]
	data['volume'] = values[2]
	data['avg_daily_volume'] = values[3]
	data['stock_exchange'] = values[4]
	data['market_cap'] = values[5]
	data['book_value'] = values[6]
	data['ebitda'] = values[7]
	data['dividend_per_share'] = values[8]
	data['dividend_yield'] = values[9]
	data['earnings_per_share'] = values[10]
	data['52_week_high'] = values[11]
	data['52_week_low'] = values[12]
	data['50day_moving_avg'] = values[13]
	data['200day_moving_avg'] = values[14]
	data['price_earnings_ratio'] = values[15]
	data['price_earnings_growth_ratio'] = values[16]
	data['price_sales_ratio'] = values[17]
	data['price_book_ratio'] = values[18]
	data['short_ratio'] = values[19]
	return data

def get_price(symbol):
    return __request(symbol, 'l1')

def get_change(symbol):
    return __request(symbol, 'c1')

def get_volume(symbol):
    return __request(symbol, 'v')

def get_avg_daily_volume(symbol):
    return __request(symbol, 'a2')

def get_stock_exchange(symbol):
    return __request(symbol, 'x')

def get_market_cap(symbol):
    return __request(symbol, 'j1')

def get_book_value(symbol):
    return __request(symbol, 'b4')

def get_ebitda(symbol):
    return __request(symbol, 'j4')

def get_dividend_per_share(symbol):
    return __request(symbol, 'd')

def get_dividend_yield(symbol):
    return __request(symbol, 'y')

def get_earnings_per_share(symbol):
    return __request(symbol, 'e')

def get_52_week_high(symbol):
    return __request(symbol, 'k')

def get_52_week_low(symbol):
    return __request(symbol, 'j')

def get_50day_moving_avg(symbol):
    return __request(symbol, 'm3')

def get_200day_moving_avg(symbol):
    return __request(symbol, 'm4')

def get_price_earnings_ratio(symbol):
    return __request(symbol, 'r')

def get_price_earnings_growth_ratio(symbol):
    return __request(symbol, 'r5')

def get_price_sales_ratio(symbol):
    return __request(symbol, 'p5')

def get_price_book_ratio(symbol):
    return __request(symbol, 'p6')

def get_short_ratio(symbol):
    return __request(symbol, 's7')

def get_historical_prices(symbol, start_date, end_date):

	url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
	'd=%s&' % str(int(end_date[4:6]) - 1) + \
	'e=%s&' % str(int(end_date[6:8])) + \
	'f=%s&' % str(int(end_date[0:4])) + \
	'g=d&' + \
	'a=%s&' % str(int(start_date[4:6]) - 1) + \
	'b=%s&' % str(int(start_date[6:8])) + \
	'c=%s&' % str(int(start_date[0:4])) + \
	'ignore=.csv'

	#print url
	days = urllib.urlopen(url).readlines()
    
	data = [day[:-2].split(',') for day in days]
	return data
	
def get_asx_dividends(symbol):


	
	f = urllib.urlopen("http://www.asx.com.au/asx/markets/dividends.do?by=asxCodes&asxCodes=%s&view=all" % symbol)
	html = f.read()

	soup = BeautifulSoup(''.join(html))

	table = soup.find('table',id="dividends")
	data = []
	rows = table.findAll('tr')
	i=-1
	for tr in rows:
	  
	  cols = tr.findAll('td')
	  j=0
	  if len(cols)>0:
	  	data.append([])
	  
	  for td in cols:
	
		data[i].append(''.join(td.find(text=True).strip()))
	  	j=j+1
	 
	  i=i+1
	
	return data
	
def get_historical_dividends(symbol, start_date, end_date):

	url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
	'd=%s&' % str(int(end_date[4:6]) - 1) + \
	'e=%s&' % str(int(end_date[6:8])) + \
	'f=%s&' % str(int(end_date[0:4])) + \
	'g=v&' + \
	'a=%s&' % str(int(start_date[4:6]) - 1) + \
	'b=%s&' % str(int(start_date[6:8])) + \
	'c=%s&' % str(int(start_date[0:4])) + \
	'ignore=.csv'

	#print url
	days = urllib.urlopen(url).readlines()

	data = [day[:-2].split(',') for day in days]
	return data
	

