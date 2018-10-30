import os, re
from itertools import islice
from collections import defaultdict
from Possible_Stock_Names import Nifty50
from Helpers.Helpers import Stock_Price
from datetime import datetime as dt
from datetime import timedelta
# from Market.Nse_Modules.Get_ET_Archieved_News import *


NEUTRAL = 'NEUTRAL'
GOOD = 'GOOD'
VERY_GOOD = 'VERY_GOOD'
SUPER_GOOD = 'SUPER_GOOD'
BAD = 'BAD'
VERY_BAD = 'VERY_BAD'
SUPER_BAD = 'SUPER_BAD'
News_Class_File = os.path.join(os.path.dirname(__file__), 'News_Files/Cleaned_News_File.txt')
class Prepare_News_Stat():

    def __init__(self, Date):
        self.Date = Date
        self.Stock_Specific_News_Dict = {}
        Cleaned_News_File = os.path.join(os.path.dirname(__file__)+'/Cleaned_Files/'+Date+'_Cleaned_News.txt')

        self.cleaned_news_file = open(Cleaned_News_File, 'r+')
        self.words_count = defaultdict(int)
        self.Map_Stock_Specific_News()

    def Map_Stock_Specific_News(self):
        for stock_code, stock_names in Nifty50.items():
            self.Stock_Specific_News_Dict[stock_code] = []
        for news_line in self.cleaned_news_file.readlines():
            for stock_code, stock_names in Nifty50.items():
                for stock_name in stock_names:
                    if re.search('\\b{}\\b'.format(stock_name), news_line):
                        self.Stock_Specific_News_Dict[stock_code].append(news_line)
                        break

    def get_each_words_count(self):
        for line in self.cleaned_news_file.readlines():
            if len(line.split()) < 1:
                continue
            for word in line.split():
                self.words_count[word] += 1

class Map_News_To_Stock_Next_Day_Change():

    def __init__(self, Date, Parse_News=False):

        self.Date = Date
        News_Class_File = os.path.join(os.path.dirname(__file__) + '/Cleaned_Files/' + Date + '_News_Class_File.csv')
        # if Parse_News:
        #     Get_ET_News(self.Date)
        self.News_Class_File = open(News_Class_File, 'w+')
        OBJ = Prepare_News_Stat(Date=self.Date)
        self.Stock_News_Dict = OBJ.Stock_Specific_News_Dict
        self.Map_News_To_Class()

    def Stock_Pchg_To_Class(self, PChg):
        if 0 < PChg < 1.5:
            return NEUTRAL
        if 1.5 < PChg < 3.0 :
            return GOOD
        if 3.0< PChg < 5.0:
            return VERY_GOOD
        if PChg > 5.0:
            return SUPER_GOOD

        if 0 > PChg > -1.5:
            return NEUTRAL
        if -1.5 > PChg > -3:
            return BAD
        if -3 < PChg < -5:
            return VERY_BAD
        if PChg < -5.0:
            return SUPER_BAD

    def Get_Stock_Next_Day_Close_Price(self, Stock_Id):
        Date_Obj = dt.strptime(self.Date , '%Y%m%d')
        Next_Date = Date_Obj + timedelta(days=1)
        Close_Price, Prev_Close_Price = Stock_Price().Get_Close_Price_On_Date(Stock_Id=Stock_Id, Date=Next_Date)
        Price_PChg = (Close_Price - Prev_Close_Price) / Prev_Close_Price * 100
        return Price_PChg

    def Map_News_To_Class(self):
        self.News_Class_File.write('Date'+','+'Stock'+','+'News'+','+'Class'+'\n')
        for Stock_Code , News_List in self.Stock_News_Dict.items():
            if len(News_List) < 1:
                continue
            PChg = self.Get_Stock_Next_Day_Close_Price(Stock_Id=Stock_Code)
            Class = self.Stock_Pchg_To_Class(PChg)
            for news in News_List:
                try:

                    self.News_Class_File.write(self.Date+","+
                                                Stock_Code+","+
                                               news.strip("\n")+
                                               ","+Class+"\n")
                except Exception as err:
                    print(news)
                    print(Class)
                    print(err)


# obj = Map_News_To_Stock_Next_Day_Change('20181023', Parse_News=False)
# obj.Get_Stock_Next_Day_Close_Price()


