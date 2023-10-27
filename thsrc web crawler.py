import requests
import json
from datetime import datetime   #為了將時間格式與字串與int之間做轉換

url = 'https://www.thsrc.com.tw/TimeTable/Search'

header ={'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

location ={
    '南港':'NanGang',
    '台北':'TaiPei',
    '板橋':'BanQiao',
    '桃園':'TaoYuan',
    '新竹':'XinZhu',
    '苗栗':'MiaoLi',
    '台中':'TaiZhong',
    '彰化':'ZhangHua',
    '雲林':'YunLin',
    '嘉義':'JiaYi',
    '台南':'TaiNan',
    '左營':'ZuoYing',
    }

print(list(location.keys()))   #先印出所有站名
depart = input('請問要從哪裡出發? \n')
arrive = input('請問要到哪裡? \n')
timedate = input('請問出發日期? ex:2023/11/01:\n')
timehour = input('請問出發時間? ex:10:00:\n')

start = location[depart]  #從location字典抓出value
end = location[arrive]  #從location字典抓出value
timehour = datetime.strptime(timehour, '%H:%M').strftime('%H:%M')   #函數會將輸入的字串比對strptime的格式，正確後會再轉換為strftime我所指定的格式
print()

param = {     #從network 內 search的 payload抓
    'SearchType': 'S',
    'Lang': 'TW',
    'StartStation': start,
    'EndStation': end,
    'OutWardSearchDate': timedate,
    'OutWardSearchTime': timehour,
    'ReturnSearchDate': '2023/10/27',
    'ReturnSearchTime': '21:00',
    'DiscountType': ''
    }

data = requests.post(url, data=param, headers=header).text   #因為是post 參數使用是用data
# print(data)   發現抓下來的檔案是json  可以用這個網站http://json.parser.online.fr/
thsrc = json.loads(data)
inttime = datetime.strptime(timehour, '%H:%M').strftime('%H%M')  #將使用者輸入的時間轉換為int以利後續比較大小
items = thsrc['data']['DepartureTable']['TrainItem']
for row in items:
    row['DepartureTime'] = datetime.strptime(row['DepartureTime'], '%H:%M').strftime('%H%M')  #將json檔案內離站時間轉換為int以利後續比較大小
    if row['DepartureTime'] >= inttime:
        print('車次:',row['TrainNumber'])
        row['DepartureTime'] = str(datetime.strptime(row['DepartureTime'], '%H%M').strftime('%H:%M'))  #將離站時間轉換原本格式
        print('出發時間:',row['DepartureTime'])
        print('抵達時間:',row['DestinationTime'])
        print('車程:',row['Duration'])
        stops = row['StationInfo']
        for stop in stops:
            if stop['Show'] == True:   #判斷停站的布林值為True代表有停靠 才會印出站名
                print(stop['StationName'])
        print()

    
