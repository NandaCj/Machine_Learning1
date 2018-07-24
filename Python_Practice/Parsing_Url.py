import requests
from lxml.html import fromstring
from bs4 import BeautifulSoup
import re
url = "https://economictimes.indiatimes.com/tvs-motor-company-ltd/balancesheet/companyid-12940.cms"
Response = requests.get(url)
soup = BeautifulSoup(Response.text, 'html.parser')

print(soup.find_all('tr')[2])

print (re.findall(r'Months',soup.find_all('tr')[3].get_text()))

i = 0
for td in soup.find_all('td'):
    print(i,"--->" ,td)
    i += 1
for td in soup.find_all('td')[14:50:6]:
    print(td.get_text())

for td in soup.find_all('td')[51::6]:
    print(td.get_text())
