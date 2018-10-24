from pymongo import MongoClient as MG
import re
import datetime

client = MG("mongodb://127.0.0.1:27017")
db = client.NseDb
#db.NseCodesCollection.insert({"_id":"NseCodes","Codes":[]})

NseCodesFile = open("C:\\Users\\Ranjith\\Desktop\\NSE Scripts\\CompleteList.txt")
NseHistoryFile = open("C:\\Users\\Ranjith\\Desktop\\NSE Scripts\\NseHistory.txt")

class InsertNseData :
	
	def __init__(self):
		self.InsertData()

	def InsertData(self):

		for Line in NseHistoryFile.readlines()[:1]:
			
			Code = re.sub("'","",Line.split(':')[0]); print (Code)
			CodeLen = len(Code)
			History = Line[CodeLen+2:-2]
			History = History.split("datetime.date")
			print (History)
			for Data in History[1:]:
				#print (Data)
				if "'" in Data:
					continue
				
				Date, ClosePrice = Data.split(':')
				ClosePrice = ClosePrice.strip().replace(",","")
				print (Date, "--->" ,ClosePrice)

			
			#	print (Date, ClosePrice)
				self.InsertHistory(Code, Date, ClosePrice)

			#db.PriceHistory.insert({"_id":Code, "Code":Code})
	def InsertHistory(self, Code, Date, ClosePrice):
		#for History in NseHistoryFile.readlines():
			#db.PriceHistory.update({"_id":"History"},{'$push':{Code:{"_id":Date,"ClosePrice":ClosePrice}}})
			db.PriceHistory.update({"_id":"History"},{'$set':{Code.0.Date:ClosePrice}})


InsertNseData()