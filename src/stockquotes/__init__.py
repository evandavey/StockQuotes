import ystockquote
from datetime import datetime, date, time
from decimal import *
import csv
import sys, os
import getopt

def main(argv=None):
    if argv is None:
    	argv=sys.argv

  	startdate=argv[1]
	enddate=argv[2]
	outpath=argv[3]

	Stocks = ['BHP.AX','CBA.AX','TLS.AX','NAB.AX', \
			 'BSL.AX','SGT.AX','WES.AX','WOW.AX', \
			 'WESN.AX','AWC.AX']
	Prices = {}
	Divs={}

	StartDate = datetime.strptime(startdate,'%Y%m%d')
	EndDate = datetime.strptime(enddate,'%Y%m%d')

	print 'Will load data for %d stocks ' % len(Stocks)
	print 'Start date %s' % startdate 
	print 'End date %s' % enddate
	
	
	for j in range(0,len(Stocks)):
		prices=[]
		divs=[]
	
		stock=Stocks[j]
	
		print 'Loading prices for ' + stock
		prices = ystockquote.get_historical_prices(stock,datetime.strftime(StartDate,'%Y%m%d'),datetime.strftime(EndDate,'%Y%m%d'))
	
		# get dividend data from ASX as yahoo is unreliable
		# note data is only available for current financial year
		print 'Loading dividends for ' + stock
		divs = ystockquote.get_asx_dividends(stock[:-3])
	

		adj_close={}
		div={}


		# Populate lists from downloaded data
		for i in range(1,len(prices)):
	
			dt=prices[i][0]
			adj_close=prices[i][6]
			dt=datetime.strptime(dt,'%Y-%m-%d')
		
			try:
				 Prices[dt.strftime('%Y%m%d')]
			except KeyError:
				Prices[dt.strftime('%Y%m%d')]={stock:{'adj_close':adj_close}}
			else:
				Prices[dt.strftime('%Y%m%d')][stock] = {'adj_close':adj_close}
	
	
	
		# Populate lists from downloaded data
		for i in range(1,len(divs)):

			getcontext().prec = 6
			dt=divs[i][4]
			val=float(Decimal(divs[i][1][:-1])/100)
			franking=float(Decimal(divs[i][5][:-1])/100)
			dt=datetime.strptime(dt,'%d/%m/%Y')

			#filter dividend data for relevant data range
			if (dt >= StartDate and dt <= EndDate):
				try:
				 	Divs[dt.strftime('%Y%m%d')]
				except KeyError:
					Divs[dt.strftime('%Y%m%d')]={stock:{'dividend':val,'franking':franking}}
				else:
					Divs[dt.strftime('%Y%m%d')][stock] ={'dividend':val,'franking':franking}
				



	output_matrix(Prices,outpath + '/' + datetime.strftime(EndDate,'%Y%m%d')+'_prices.csv')
	output_matrix(Divs,outpath + '/' + datetime.strftime(EndDate,'%Y%m%d')+'_dividends.csv')
	return 0

def output_matrix(data,path):
	ofile  = open(path, "w")
	writer = csv.writer(ofile,quoting=csv.QUOTE_NONNUMERIC)

	
	header=''
	txt=''
	print 'outputing matrix...'
	for dt, stockdata in data.iteritems():
		for stock,dataitems in stockdata.iteritems():
			if header=='':
				header='date,stock'
				for k in dataitems.keys():
					header=header+','+k
				writer.writerow(header.split(','))
				header=header+'\n'
				
			r=''.join(dt+','+stock)
			for label,item in dataitems.iteritems():
				#loses data type here, might need rewrite
				r=r+''.join(','+ str(item))
				
			writer.writerow(r.split(','))
			txt=txt+r+'\n'
		
	txt=header+txt	
	print txt

