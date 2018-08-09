import requests
from bs4 import BeautifulSoup
from Helpers.Logging import *
import re

Q_Regex = r'[Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec].{5}'

class Parse:
    def __init__(self):
        pass

    def Get_Soup(self, Url):
        Upage = requests.get(Url).text
        Usoup = BeautifulSoup(Upage, 'html.parser')
        return Usoup

    def Get_Qly_Total_Years(self, Soup):
        Total_Years = len(Soup.find_all('tr')[2]) - 1
        Info("Quarterly Details Available for {} Quarters".format(Total_Years))
        return Total_Years

    def Get_Qly_Months(self, Soup):
        Qly_Months = re.findall(Q_Regex, Soup.find_all('tr')[2].get_text())
        Info(Qly_Months)
        return Qly_Months




