from nsepy import get_history
from datetime import date
from nsetools import Nse
nse = Nse()
import re

file = open("C:\\Users\\Ranjith\\Desktop\\NSE Scripts\\NSECodesList.txt", 'r')
OutputFile = open("C:\\Users\\Ranjith\\Desktop\\NSE Scripts\\NseHistory.txt", 'a+')
for line in file.readlines()[:1]:
        Code = re.sub("'","",line.split(':')[0])
        print (Code)
        data = get_history(symbol=Code, start=date(2017,11,1), end=date(2017,11,7))
        #OutputFile.write(Code+":"+str(data['Close'].to_dict())+"\n")
        print (data)


