import pymongo
from pymongo import MongoClient
import re
import requests
from lxml import html

client = MongoClient("mongodb://127.0.0.1:27017")

db = client.ET

class GetBalanceSheet():

	def __init__(self):
		self.GetBalanceSheetUrl()


	def GetBalanceSheetUrl (self):
		Urls = list(db.ETUrls.find({},{"_id":0, "BalanceSheet":1}))
		BalanceSheetUrl = Urls[0]['BalanceSheet']
		self.FormBalanceSheet(BalanceSheetUrl)

	def FormBalanceSheet(self, BalanceSheetUrl):
		ETdict = list(db.ETCompanyCodes.find({},{"_id":0}))
		ETdict = ETdict[0]
		for StockId, ETId in ETdict.items():
			if StockId == "BLUEBLENDS":
				continue

			if ETId == 'NA':
				continue
			BUrl = re.sub('Code', ETId, BalanceSheetUrl)
			print (StockId, BUrl)
			try:
				self.FilterBalanceSheet(StockId, BUrl)
			except :
				print (StockId,"Balance Sheet is not found")
	
	def FilterBalanceSheet(self, StockId, BUrl):
		Response = requests.get(BUrl)
		#Response = Response.text
		tree = html.fromstring(Response.text) 
		Data = tree.xpath('//td/text()')
		#BalanceSheet1 = tree.xpath('//td[@class="textR"]/text()')
		print (Data)
		NetWorth = Data.index('Net Worth'); #print (NetWorth)
		SecuredLoan = Data.index('Secured Loan');
		TotalYears = SecuredLoan - NetWorth
		TotalLiabilities = Data.index('TOTAL LIABILITIES') ; #print (TotalLiabilities)
		TotalCurrentAssests = Data.index('Total Current Assets'); #print (TotalCurrentAssests)
		TotalCurrentLiabilities = Data.index('Total Current Liabilities'); #print (TotalCurrentLiabilities)
		NETCURRENTASSETS = Data.index('NET CURRENT ASSETS') ;#print (NETCURRENTASSETS)
		TOTALASSETS = Data.index('TOTAL ASSETS(A+B+C+D+E)') ;# print (TOTALASSETS)
		
		if TotalYears == 6:
			db.BalanceSheets.insert({"_id":StockId,
									"Jun17":{'NetWorth':Data[NetWorth+1], 'TotalLiabilities':Data[TotalLiabilities+1], 'TotalCurrentAssests':Data[TotalCurrentAssests+1], 'NETCURRENTASSETS':Data[NETCURRENTASSETS+1], 'TOTALASSETS':Data[TOTALASSETS+1]},
									"Jun16":{'NetWorth':Data[NetWorth+2], 'TotalLiabilities':Data[TotalLiabilities+2], 'TotalCurrentAssests':Data[TotalCurrentAssests+2], 'NETCURRENTASSETS':Data[NETCURRENTASSETS+2], 'TOTALASSETS':Data[TOTALASSETS+2]},
									"Jun15":{'NetWorth':Data[NetWorth+3], 'TotalLiabilities':Data[TotalLiabilities+3], 'TotalCurrentAssests':Data[TotalCurrentAssests+3], 'NETCURRENTASSETS':Data[NETCURRENTASSETS+3], 'TOTALASSETS':Data[TOTALASSETS+3]},
									"Jun14":{'NetWorth':Data[NetWorth+4], 'TotalLiabilities':Data[TotalLiabilities+4], 'TotalCurrentAssests':Data[TotalCurrentAssests+4], 'NETCURRENTASSETS':Data[NETCURRENTASSETS+4], 'TOTALASSETS':Data[TOTALASSETS+4]},
									"Jun13":{'NetWorth':Data[NetWorth+5], 'TotalLiabilities':Data[TotalLiabilities+5], 'TotalCurrentAssests':Data[TotalCurrentAssests+5], 'NETCURRENTASSETS':Data[NETCURRENTASSETS+5], 'TOTALASSETS':Data[TOTALASSETS+5]},
									})
		
		if TotalYears == 5:
			db.BalanceSheets.insert({"_id":StockId,
									"Jun17":{'NetWorth':Data[NetWorth+1], 'TotalLiabilities':Data[TotalLiabilities+1], 'TotalCurrentAssests':Data[TotalCurrentAssests+1], 'NETCURRENTASSETS':Data[NETCURRENTASSETS+1], 'TOTALASSETS':Data[TOTALASSETS+1]},
									"Jun16":{'NetWorth':Data[NetWorth+2], 'TotalLiabilities':Data[TotalLiabilities+2], 'TotalCurrentAssests':Data[TotalCurrentAssests+2], 'NETCURRENTASSETS':Data[NETCURRENTASSETS+2], 'TOTALASSETS':Data[TOTALASSETS+2]},
									"Jun15":{'NetWorth':Data[NetWorth+3], 'TotalLiabilities':Data[TotalLiabilities+3], 'TotalCurrentAssests':Data[TotalCurrentAssests+3], 'NETCURRENTASSETS':Data[NETCURRENTASSETS+3], 'TOTALASSETS':Data[TOTALASSETS+3]},
									"Jun14":{'NetWorth':Data[NetWorth+4], 'TotalLiabilities':Data[TotalLiabilities+4], 'TotalCurrentAssests':Data[TotalCurrentAssests+4], 'NETCURRENTASSETS':Data[NETCURRENTASSETS+4], 'TOTALASSETS':Data[TOTALASSETS+4]},
									})
		
		if TotalYears == 4:
			db.BalanceSheets.insert({"_id":StockId,
									"Jun17":{'NetWorth':Data[NetWorth+1], 'TotalLiabilities':Data[TotalLiabilities+1], 'TotalCurrentAssests':Data[TotalCurrentAssests+1], 'NETCURRENTASSETS':Data[NETCURRENTASSETS+1], 'TOTALASSETS':Data[TOTALASSETS+1]},
									"Jun16":{'NetWorth':Data[NetWorth+2], 'TotalLiabilities':Data[TotalLiabilities+2], 'TotalCurrentAssests':Data[TotalCurrentAssests+2], 'NETCURRENTASSETS':Data[NETCURRENTASSETS+2], 'TOTALASSETS':Data[TOTALASSETS+2]},
									"Jun15":{'NetWorth':Data[NetWorth+3], 'TotalLiabilities':Data[TotalLiabilities+3], 'TotalCurrentAssests':Data[TotalCurrentAssests+3], 'NETCURRENTASSETS':Data[NETCURRENTASSETS+3], 'TOTALASSETS':Data[TOTALASSETS+3]},
									})
		if TotalYears == 3:
			db.BalanceSheets.insert({"_id":StockId,
									"Jun17":{'NetWorth':Data[NetWorth+1], 'TotalLiabilities':Data[TotalLiabilities+1], 'TotalCurrentAssests':Data[TotalCurrentAssests+1], 'NETCURRENTASSETS':Data[NETCURRENTASSETS+1], 'TOTALASSETS':Data[TOTALASSETS+1]},
									"Jun16":{'NetWorth':Data[NetWorth+2], 'TotalLiabilities':Data[TotalLiabilities+2], 'TotalCurrentAssests':Data[TotalCurrentAssests+2], 'NETCURRENTASSETS':Data[NETCURRENTASSETS+2], 'TOTALASSETS':Data[TOTALASSETS+2]},
									})
		
		if TotalYears == 2:
			db.BalanceSheets.insert({"_id":StockId,
									"Jun17":{'NetWorth':Data[NetWorth+1], 'TotalLiabilities':Data[TotalLiabilities+1], 'TotalCurrentAssests':Data[TotalCurrentAssests+1], 'NETCURRENTASSETS':Data[NETCURRENTASSETS+1], 'TOTALASSETS':Data[TOTALASSETS+1]},
									})
						
		
		

		#BalanceSheet = {'Net Worth' : {"Share Capital":{}}
						
						





		
		

	


GetBalanceSheet()