import requests
import re
import io


IFile = open("C:\\Users\\Ranjith\\Desktop\\NSE Scripts\\NewsFile.txt", 'r')
for line in IFile:
	News = re.findall(r'news.*?cms">(.*?)</a>', line)
	#print (News)
	for i in News:        	
		if "img class" in i:
			continue
		print(i)
