import requests
import configparser
import re, os
import datetime as Dt
from Helpers.Logging import Info, Critical, Debug
ET_Config = configparser.ConfigParser()
ET_Config.read("ET_Config.ini")
ET_News_Archieve_General_Url = "https://economictimes.indiatimes.com/archivelist/year-2018,month-4,starttime-42005.cms"
RAW_NEWS_FILE = "RAW_NEWS_FILE.txt"
Filtered_News_File = "Filtered_News_File.txt"
re_industry = r'<a.*?[markets|news|industry|!recos].*?cms">(.*?)</a>'
Un_wanted_News_File = "C:\Users\nandpara\PycharmProjects\Machine_Learning1\Stock_News_Analysis\Clean_Data\Cleaned_Files\UnWanted_News.txt"

News_Files_dir = os.path.join(os.path.dirname(__file__), "News_Files")



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
        Info("Parsing ET news for date :{}".format(Date))
        self.Date = Date
        self.Raw_News_File = os.path.join(News_Files_dir,  self.Date+"_"+"raw_news_file.txt")
        self.Filtered_News_File = os.path.join(News_Files_dir,  self.Date+"_"+"filtered_news_file.txt")
        self.Un_wanted_News_File = os.path.join(News_Files_dir, "UnWanted_News.txt")
        News_Archieve_Url = self.Form_News_Archieve_Url_From_Date(self.Date)
        self.Save_Raw_News(News_Archieve_Url)
        self.Filter_News()

    def Form_News_Archieve_Url_From_Date(self, Date):
        """
        Date Format yyyymmdd ex: 20181203
        Forms the ET archieve url page by
            gets the 1_jan_2005 code from config
            calculates the days between 1_jan_2005 and user data
            adds diff date with 1_jan_2005 date to get new datecode and forms url
        """
        Jan_1_2015_Code = '42005'#ET_Config.get("ET_News_Archieve_Code", "1_Jan_2015")
        Days_Between = (Dt.datetime.strptime(Date, '%Y%m%d') - Dt.datetime.strptime('20150101', '%Y%m%d')).days
        Required_ET_Archieve_Code = int(Jan_1_2015_Code) + int(Days_Between)
        News_Archieve_Url = re.sub(Jan_1_2015_Code, str(Required_ET_Archieve_Code), ET_News_Archieve_General_Url)
        Info("Parsing Url: {}".format(News_Archieve_Url))
        return News_Archieve_Url

    def Save_Raw_News(self, News_Archieve_Url):
        """
        :param News_Archieve_Url:
        :return: saves html elements from the given url in a file
        """
        News = requests.get(News_Archieve_Url)
        News_File = open(self.Raw_News_File, 'w+')

        for line in News.text:
            try:
                News_File.write(line)
            except UnicodeEncodeError:
                continue

    def Filter_News(self):
        News_File = open(self.Raw_News_File, 'r')
        Filtered_File = open(self.Filtered_News_File, 'w+')
        NoNews_File = open(self.Un_wanted_News_File, 'w+')
        for line in News_File:
            News = re.findall(re_industry, line)
            for i in News[:-2]:
                if "img class" in i or "img height" in i or "input class" in i:
                    continue
                if len(i) < 10 or len(i.split()) <= 5:
                    NoNews_File.write(i)
                    NoNews_File.write("\n")
                    continue
                if re.search(r'^[Buy|Sel].*target.*:', i):
                    NoNews_File.write("Recos-->"+ i)
                    NoNews_File.write("\n")
                    continue
                if re.search(r'^[Share|Stock|share|stock].*[m|M]arket.*[u|U]pdate', i):
                    NoNews_File.write("Updates-->"+ i)
                    NoNews_File.write("\n")
                    continue
                if re.search(r'^[Buzzing stocks]', i):
                    NoNews_File.write("Buzzing stocks-->"+ i)
                    NoNews_File.write("\n")
                    continue

                if re.search(r'^[Stocks in the news]', i):
                    NoNews_File.write("Stocks in News-->" + i)
                    NoNews_File.write("\n")
                    continue

                Filtered_File.write(i.lower())
                Filtered_File.write("\n")
            # print(i)
        Filtered_File.close()
        News_File.close()
        NoNews_File.close()
        Info("Filtered News is stored in : {}".format(self.Filtered_News_File))


    def Get_News_Sepcific_Scrip(self, Scrip):
        News_Archieve_Url = self.Form_News_Archieve_Url_From_Date(self.Date)
        self.Save_Raw_News(News_Archieve_Url)
        self.Filter_News()
        Filtered_File = open(Filtered_News_File, 'r')
        for line in Filtered_File:
            if Scrip in line:
                print (Scrip, line)

    def __del__(self):
        pass

# ET_News = Get_ET_News('20181023')
# ET_News.Get_News_Sepcific_Scrip('hero motocorp')
# ET_News.Filter_News()
