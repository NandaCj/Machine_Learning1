import csv
from datetime import date
from nsepy.history import get_price_list
script_data = get_price_list(dt=date(2018,5,8))

script_data.to_csv('out.csv')
csv_out = csv.DictReader(open('out.csv', 'r'))
script_dict = []

for line in csv_out:
    script_dict.append(line)

data_list = ['SYMBOL','HIGH','LOW','CLOSE','R1','R2','PIVOT','S1','S2','%','>.6%','TOTTRDQTY','TOTTRDVAL', 'BUY', 'SELL']
list_200_500 = []

for i in script_dict:
    dummy_dict = {}
    if 100 < float(i['CLOSE']) < 700:
        for j in data_list:
            try:
                dummy_dict[j] = i[j]
            except:
                dummy_dict[j] = ""
        dummy_dict['PIVOT'] = (float(dummy_dict['HIGH'])+float(dummy_dict['LOW'])+float(dummy_dict['CLOSE']))/float(3)
        dummy_dict['R1'] = (float(dummy_dict['PIVOT'])*float(2))-float(dummy_dict['LOW'])
        dummy_dict['R2'] = float(dummy_dict['PIVOT'])+(float(dummy_dict['HIGH'])-float(dummy_dict['LOW']))
        dummy_dict['S1'] = (float(dummy_dict['PIVOT'])*float(2))-float(dummy_dict['HIGH'])
        dummy_dict['S2'] = float(dummy_dict['PIVOT'])-(float(dummy_dict['HIGH'])-float(dummy_dict['LOW']))
        dummy_dict['%'] = ((float(dummy_dict['CLOSE'])-float(dummy_dict['PIVOT']))/float(dummy_dict['PIVOT']))*100
        dummy_dict['BUY'] = (float(dummy_dict['CLOSE'])) + 1
        dummy_dict['SELL'] = (float(dummy_dict['PIVOT'])) -1
        if 0.6 < dummy_dict['%'] < 1.5:
            dummy_dict['>.6%'] = 'BUY'
        elif -0.6 > dummy_dict['%'] > -1.5:
            dummy_dict['>.6%'] = 'SELL'
        else:
            dummy_dict['>.6%'] = 'SKIP'
        list_200_500.append(dummy_dict)

def WriteDictToCSV(csv_file,csv_columns,dict_data):
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)

csv_file = "20180508.csv"
WriteDictToCSV(csv_file,data_list,list_200_500)