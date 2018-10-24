File = open("C:\\Users\\Ranjith\\Downloads\\18-08-2017-TO-15-11-2017_bulk.csv", 'r')
from collections import defaultdict
import re
from itertools import islice

IFile = list(islice(File, 999999))


Deals = {'Code':defaultdict(int)};
BuyCount = defaultdict(int)
i=1
try:
	for line in IFile[1:]:
		line = re.sub('["|,]','',line)
		
		Code = line.split(":")[1]
		
		Quant = int(line.split(":")[-3])
		Action = line.split(":")[-4]
		Client = line.split(":")[-5]
	
		if Action == "BUY":
			BuyCount[Code] += Quant
			try :
				Deals[Code][Client] = +Quant
			except KeyError:
				Deals[Code] = {Client:Quant}

	
		if Action == "SELL":
			BuyCount[Code] -= Quant
			try:
				Deals[Code][Client] -= Quant
			except KeyError:
				Deals[Code] = {Client:Quant}
		i +=1

except IndexError:
	print (Code)

for Count in sorted(BuyCount.values(), reverse=True):
	print ({Code:Value for Code , Value in BuyCount.items() if Value == Count})

"""
	for Code , Value in {Code:Value for Code , Value in BuyCount.items() if Value == Count}.items():
		print (Code)
		for Key , Value in { Key:Value for Key, Value in Deals[Code].items() if Value != 0}.items() :
			print ("--->",Key ,"-->", Value)


for Code in Deals:
	print ("--->",Code)
	for Value in sorted(Deals[Code].values(), reverse=True):
		
		print ("--->",{Client:Count for Client , Count in Deals[Code].items() if Count == Value and Count !=0})
"""

File.close()
