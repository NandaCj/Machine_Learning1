import requests
import re
import io
from itertools import islice

response = requests.get("https://economictimes.indiatimes.com/archivelist/year-2018,month-4,starttime-43224.cms")
OFile = "NewsFile.txt"

# NewsFile = open("NewsFile.txt", 'r')
# NewsFileOutput = open("NseNewsText.txt", 'w+')

#StocksFile = open("CompleteList.txt", 'r')

# StockList = [x.rstrip('\n') for x in list(islice(StocksFile, 2000))] ; StocksFile.close()
#print (StockList[:5])


txt = response.text
#print (txt)
class GetNews ():
	def __init__(self):
		self.WriteNews()
		# self.FilterNews()
		# for News in open("NseNewsText.txt", 'r'):
		# 	News = News.rstrip("\n")
		# 	Match = self.FilterNewsPerStock(News)
		# 	#print (Match, "--->", News)
		# 	if Match == "True":
		# 		continue
		# 	if Match == "False" :
		#
		# 			NewsLower = News.lower()
		# 			if "profit" in NewsLower or "loss" in NewsLower or "bags" in NewsLower:
		# 				print ("\n****",Match,"-->",News.lower(),"\n")
		# 				continue
		
			
	
	def WriteNews(self):
		with io.open(OFile, "w") as F:
			for line in txt:
				try:
					F.write(str(line))
					print (line)
				except UnicodeEncodeError:
					continue
	def FilterNews (self):
		for line in NewsFile:
			News = re.findall(r'<a.*?[markets|news|industry].*?cms">(.*?)</a>', line)
			#print (News)
			for i in News[:-2]:        	
				if "img class" in i or "img height" in i or "input class" in i:
					continue
				if len (i) < 10:
					continue
				NewsFileOutput.write(i)
				NewsFileOutput.write("\n")
				#print(i)
		NewsFileOutput.close()
		NewsFile.close()

	def FilterNewsPerStock (self, News):
		
		for Stock in StockList:
			#print (Stock)
			Match = "False"
			StockCodeLower = re.sub("'","",Stock.split(':')[0]).lower()
			CompanyNameLower = re.sub("'","",Stock.split(':')[1]).lower()
			NewsLower = News.lower().split()

			CompanyName = "".join(CompanyNameLower.split())

			NewsFull = "".join(NewsLower)
			#print (CompanyName,"--->",NewsFull)
			CompanyName = re.sub(",","",CompanyName).rstrip().lstrip()
			
			if StockCodeLower in NewsLower:
				
				Match = "True"
				print ("Matched Stock Code",Match, "--->",StockCodeLower,"--->", CompanyNameLower,"--->",News.lower())
				
				pass

			

			if CompanyName in NewsFull:
				
				Match = "True"
				print ("Matched Company Name",Match, "--->",StockCodeLower,"--->", CompanyNameLower,"--->",News.lower())
				
				pass
		
			
			if "limited" in CompanyNameLower:

				CompanyName = "".join(re.sub(" limited","",CompanyNameLower).split())
				CompanyName = re.sub(",","",CompanyName).rstrip().lstrip()
				#print (CompanyName)
				if CompanyName in NewsFull and (CompanyName not in ["itc","iti","tt","ttl","til","hil","bs"]):
					
					Match = "True"
					print ("Without Limited Matched Company Name",Match, "--->",StockCodeLower,"--->", CompanyName,"--->",News.lower())
					
					return Match

				
				

		return Match	



obj = GetNews()



