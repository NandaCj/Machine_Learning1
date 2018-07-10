import pymongo
from pymongo import MongoClient
import re

client = MongoClient('mongodb://localhost:27017/')


class InsertETDetails():

	def __init__(self):
		self.InsertCompanyCodes()

	def InsertCompanyCodes(self):
		db = client.ET.ETCompanyCodes

		File = open("C:\\Users\\n.gopal.paramasivam\\Desktop\\NSEScripts\\ETCompanyID.txt", 'r')
		for line in File.readlines()[1:]:

			StockID = line.split(':')[0]
			try :

				ETCompanyID = re.findall(r'(\d+).cms',line)[0]
			except IndexError:
				print (StockID, "Inside Exception has no ETCompanyID")
				db.update({"_id":"ETCompanyIDs"},{'$set':{StockID:"NA"}})
				continue
			print (StockID, "-->" ,ETCompanyID)
			db.update({"_id":"ETCompanyIDs"},{'$set':{StockID:ETCompanyID}})


InsertETDetails()