from bs4 import BeautifulSoup
import requests

url = 'https://www.esunbank.com/zh-tw/personal/deposit/rate/forex/foreign-exchange-rates'

header={'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

data = requests.get(url,headers=header).text
# print(data)


soup = BeautifulSoup(data,'html.parser')

idtable = soup.find(id='exchangeRate')

table = idtable.find('table')

tbody = table.find('tbody')

trs = tbody.find_all('tr', recursive=False)[1:]  #只找直接子節點而不遞歸查找  [1:] 代表略過第一筆資料

for row in trs:
    
    rate = row.text.strip()
    rate = rate.split()
    for item in rate:
        print(item)
    print()