import requests
import configparser
import re
import datetime as Dt

ET_Config = configparser.ConfigParser()
ET_Config.read("ET_Config.ini")
# print (type(ET_Config), ET_Config)
# print (ET_Config.get("ET_Urls", "News_Archieve_Url"))
ET_News_Archieve_General_Url = ET_Config.get("ET_Urls", "News_Archieve_Url")
RAW_NEWS_FILE = ET_Config.get("ET_News_Archieve_Code", "RAW_NEWS_FILE")
Filtered_News_File = ET_Config.get("ET_News_Archieve_Code", "Filtered_News_File")
re_industry = r'<a.*?[markets|news|industry].*?cms">(.*?)</a>'





class Get_ET_News:
    """
    Gets the News from Economic Times Archieve folders
    """
    def __init__(self, Date=''):
        """
        :param Date:
        RAW_NEWS_FILE - stores the html elements from url
        Filtered_News_File - stores only text from the Html - all in small

        """
        self.Date = Date
        print (self.Date)

    def Form_News_Archieve_Url_From_Date(self, Date):
        """
        Date Format yyyymmdd ex: 20181203
        Forms the ET archieve url page by
            gets the 1_jan_2005 code from config
            calculates the days between 1_jan_2005 and user data
            adds diff date with 1_jan_2005 date to get new datecode and forms url
        """
        Jan_1_2015_Code = ET_Config.get("ET_News_Archieve_Code", "1_Jan_2015")
        Days_Between = (Dt.datetime.strptime(Date, '%Y%m%d') - Dt.datetime.strptime('20150101', '%Y%m%d')).days
        Required_ET_Archieve_Code = int(Jan_1_2015_Code) + int(Days_Between)
        News_Archieve_Url = re.sub(Jan_1_2015_Code, str(Required_ET_Archieve_Code), ET_News_Archieve_General_Url)
        print (News_Archieve_Url)
        return News_Archieve_Url

    def Save_Raw_News(self, News_Archieve_Url):
        """
        :param News_Archieve_Url:
        :return: saves html elements from the given url in a file
        """
        News = requests.get(News_Archieve_Url)
        News_File = open(RAW_NEWS_FILE, 'w+')

        for line in News.text:
            try:
                News_File.write(line)
            except UnicodeEncodeError:
                continue

    def Get_All_News(self):
        pass

    def Filter_News(self):
        News_File = open(RAW_NEWS_FILE, 'r')
        Filtered_File = open(Filtered_News_File, 'w+')
        for line in News_File:
            News = re.findall(re_industry, line)
            for i in News[:-2]:
                if "img class" in i or "img height" in i or "input class" in i:
                    continue
                if len(i) < 10:
                    continue
                Filtered_File.write(i.lower())
                Filtered_File.write("\n")
            # print(i)
        Filtered_File.close()
        News_File.close()


    def Get_News_Sepcific_Scrip(self, Scrip):
        News_Archieve_Url = self.Form_News_Archieve_Url_From_Date(self.Date)
        self.Save_Raw_News(News_Archieve_Url)
        self.Filter_News()
        Filtered_File = open(Filtered_News_File, 'r')
        for line in Filtered_File:
            if Scrip in line:
                print (Scrip, line)
                

ET_News = Get_ET_News('20181017')
ET_News.Get_News_Sepcific_Scrip('hero motocorp')
# ET_News.Filter_News()
