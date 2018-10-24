import os
from collections import defaultdict
from Possible_Stock_Names import Nifty50

Cleaned_News_File = os.path.join(os.path.dirname(__file__), 'Cleaned_News_File.txt')

class Prepare_News_Stat():

    def __init__(self):
        self.opened_news_file = open(Cleaned_News_File, 'r+')
        self.words_count = defaultdict(int)

    def get_each_words_count(self):
        for line in self.opened_news_file.readlines():
            if len(line.split()) < 1:
                continue
            for word in line.split():
                self.words_count[word] += 1

    def map_news_to_stock(self):
        for news in self.opened_news_file.readlines():
            self.stock_specific_news(news_line=news)

    def stock_specific_news(self, news_line):
        for stock_code, stock_names in Nifty50.items():
            for stock_name in stock_names:
                if stock_name in news_line:
                    print(stock_code , "-->" , news_line)

    def summa(self):
        pass


obj = Prepare_News_Stat()
# obj.get_each_words_count()
# print(obj.words_count)
obj.map_news_to_stock()