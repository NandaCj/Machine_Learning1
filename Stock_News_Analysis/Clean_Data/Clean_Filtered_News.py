import os, nltk, re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
import timeit
from Helpers.Logging import Critical, Info, Debug
import string
from Stock_News_Analysis.Clean_Data.Possible_Stock_Names import get_all_stocks_possible_names

Porter_Stemmer = PorterStemmer()
Lancaster_Stemmer = LancasterStemmer()
WordNet_Lemmatizer = WordNetLemmatizer()
Root_Dir = "C:/Users/nandpara/PycharmProjects/Machine_Learning1"
Filtered_News_File_Dir = Root_Dir + '/Market/Nse_Modules/News_Files/'
Cleaned_News_File = os.path.join(os.path.dirname(__file__), 'Cleaned_News_File.txt')
Debug(Filtered_News_File_Dir)
From_Line = 0
To_Line = 999999

class Clean_News_Data():
    """
    Below Steps are followed to clean data
    1.Each word
    2.lowercase - already stored in lower case
    3.remove punctuations
    4.filter stopwords
    5.lemmatize - map to root word
    """
    def __init__(self, Date):
        self.Date = Date
        Filtered_News_File = Filtered_News_File_Dir + Date + "_filtered_news_file.txt"
        self.News_File_Opened = open(Filtered_News_File, 'r+')
        News = self.Make_News_File_generator(self.News_File_Opened)
        Cleaned_News_list = self.Remove_Punctuations_and_If_Alpha(News)
        Filtered_News = self.Filter_Stop_words(Cleaned_News_list)
        Stem_Words_News_List = self.Get_Stem_Words(Filtered_News)
        Lemmatize_News_Words_List = self.Lemmatize_News_Words(Stem_Words_News_List)
        Cleaned_News = self.Remove_Stock_Names_From_News(Lemmatize_News_Words_List)
        self.Store_Cleaned_News(set(Lemmatize_News_Words_List))

    def Log_It(self, *args):
        for arg in args:
            Debug(arg)

    def Store_Cleaned_News(self, Lemmatize_News_Words_List):
        Cleaned_News_File = os.path.join(os.path.dirname(__file__), "Cleaned_Files/" + self.Date + "_Cleaned_News.txt")
        clean_news_file = open(Cleaned_News_File, 'w+')
        for clean_news in Lemmatize_News_Words_List:
            clean_news_file.write(clean_news +'\n')
        clean_news_file.close()

    def Make_News_File_generator(self, New_File_Opened):
        """
        Reads File and make a list of all lines with removing "\n" in each line end
        :param File_Path:
        :return: generator of file list
        """

        yield [line.strip() for line in New_File_Opened.readlines()]


    def Remove_Punctuations_and_If_Alpha(self, News):
        """
        splits each news line into words
        removes punctuations
        :param News:
        :return:
        """
        Cleaned_News_list = []
        for each_line in News.next()[From_Line:To_Line]:

            list_of_alpha_words = [word for word in word_tokenize(each_line)
                                   if word not in string.punctuation]
            Cleaned_News = " ".join([word.strip("'") for word in list_of_alpha_words])
            Cleaned_News_list.append(Cleaned_News)
            self.Log_It("Remove_Punctuations_and_If_Alpha",
                        each_line, list_of_alpha_words, Cleaned_News)
        return Cleaned_News_list

    def Filter_Stop_words(self, Cleaned_News_list):
        """
        Filters the stop words using nltk stopwords
        removes numbers as well
        :param Cleaned_News_list:
        :return:
        """
        Filtered_News_List = []
        for each_news in Cleaned_News_list:
            each_news = re.sub('-', " ", each_news)
            each_word_list = [word for word in word_tokenize(each_news)
                              if len(word) > 1 ]
            removed_stop_words = [word for word in each_word_list
                                  if word not in stopwords.words('english')
                                  if word.isalpha()]
            Filtered_News = " ".join(removed_stop_words)
            Filtered_News_List.append(Filtered_News)
            self.Log_It("Filter_Stop_words", each_news, each_word_list, Filtered_News)
        return Filtered_News_List

    def Get_Stem_Words(self, Filtered_News_List):
        Stem_Words_News_List = []
        for each_news in Filtered_News_List:
            tmp_news = each_news
            news_words = word_tokenize(each_news)
            self.Log_It("Get_Stem_Words", each_news, news_words)
            for each_word in news_words:
                stem_word = Porter_Stemmer.stem(each_word)
                tmp_news = re.sub(each_word, stem_word, tmp_news)
            Stem_Words_News_List.append(tmp_news)
            self.Log_It(tmp_news)

        return Stem_Words_News_List

    def Lemmatize_News_Words(self, Stem_Words_News_List):
        Lemmatize_News_Words_List = []
        for each_news in Stem_Words_News_List:
            tmp_news = each_news
            news_words = word_tokenize(each_news)
            self.Log_It("Lemmatize_News_Words",each_news, news_words)
            for each_word in news_words:
                lemma_word = WordNet_Lemmatizer.lemmatize(each_word)
                tmp_news = re.sub(each_word, lemma_word, tmp_news)
            Lemmatize_News_Words_List.append(tmp_news)
            self.Log_It(tmp_news)
        return Lemmatize_News_Words_List

    def Remove_Stock_Names_From_News(self, Lemmatize_News_Words_List):
        all_stocks_possible_names = get_all_stocks_possible_names()
        Cleaned_News = []
        for each_news in Lemmatize_News_Words_List:
            tmp_news = each_news
            news_words = word_tokenize(each_news)
            for each_word in news_words:
                if each_word in all_stocks_possible_names:
                    each_news = re.sub(r'\\b{}\\b'.format(each_news), '', each_news)
            self.Log_It(tmp_news, each_news)






    def __del__(self):
        self.News_File_Opened.close()

# Clean_News_Data(Date='20181023')

