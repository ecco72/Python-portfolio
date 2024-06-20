#cmd: 先cd 到google chrome 目錄 然後再輸入: chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\chromedriver_win32\data
import json
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
# import subprocess
# import os
# os.system("cd C:\Program Files\Google\Chrome\Application & chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\chromedriver_win32\data")
# # # subprocess.run(["cd C:\Program Files\Google\Chrome\Application", "", "chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\chromedriver_win32\data"]) 
# time.sleep(5)


chrome_options = Options()
caps = {                          #開啟日誌監聽
        "browserName": "chrome",
        'goog:loggingPrefs': {'performance': 'ALL'}
        }
for key, value in caps.items():  # 將caps添加到options中
    chrome_options.set_capability(key, value)
    
chrome_options.add_experimental_option('debuggerAddress', 'localhost:9222')
browser = webdriver.Chrome(options=chrome_options)

urllogin = 'https://shopee.tw/buyer/login?next=https%3A%2F%2Fshopee.tw%2F'
urlsearch= 'https://shopee.tw/search?keyword=soundbar'


browser.get(urllogin)
loginstatus = input('登入了嗎? 已登入請輸入Y: \n')
while True:
    if loginstatus == 'y' or 'Y':
        break
    
browser.get(urlsearch)
browser.implicitly_wait(5)
time.sleep(2)

searchstatus = input('進到搜尋頁面了嗎? 已進入請輸入Y: \n')
while True:
    if loginstatus == 'y' or 'Y':
        break


soup = BeautifulSoup(browser.page_source,'html.parser')
total_page = soup.find('span', class_='shopee-mini-page-controller__total').text
print(total_page)

for i in range(1,int(total_page)):
    page = i
    urlnextpage= f'https://shopee.tw/search?keyword=soundbar&page={page}'
    browser.get(urlnextpage)
    browser.implicitly_wait(5)
    time.sleep(2)

    def filter_type(_type: str):   #設定要過濾的type
        types = [
            'application/javascript', 'application/x-javascript', 'text/css', 'webp', 'image/png', 'image/gif',
            'image/jpeg', 'image/x-icon', 'application/octet-stream', 'image/svg+xml', 'image/webp', 'text/html',
            'font/x-woff2','text/plain'
            ]
        if _type not in types:
            return True
        return False
    
    
    performance_log = browser.get_log('performance') #獲取名稱為 performance 的日誌
    for packet in performance_log:
        message = json.loads(packet.get('message')).get('message') #獲取message的數據
        if message.get('method') != 'Network.responseReceived': #如果method 不是 responseReceived 就不往下執行
            continue
        packet_type = message.get('params').get('response').get('mimeType') #獲取response的type
        if not filter_type(_type=packet_type): # 過濾type
            continue
        requestId = message.get('params').get('requestId')
        
        url = message.get('params').get('response').get('url') #獲取response的url
        if url[:45] != 'https://shopee.tw/api/v4/search/search_items?':
            continue
        
        try:
            resp = browser.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId}) #使用 cdp
            respstr = str(resp).replace("{'base64Encoded': False, 'body': '{", '{').replace('\\\\', '\\').replace("'}", "")
            cleaned_string = re.sub(r'\\xa0', '',respstr)

            with open('jsonre.txt','a',encoding='utf-8') as jj:
                jj.write(cleaned_string)
            result = json.loads(cleaned_string)
            
            items = result['items']
            for item in items:
                name = item['item_basic']['name']
                price_min = item['item_basic']['price_min'] / 100000
                price_max = item['item_basic']['price_max'] / 100000
                historical_sold = item['item_basic']['historical_sold']
                rating_star = item['item_basic']['item_rating']['rating_star']
                shop_location = item['item_basic']['shop_location']
                
                with open('result.txt' ,'a', encoding='utf-8') as f:
                    f.write('商品名稱: '+name+'\n')
                    f.write('最低價: '+str(price_min)+'\n')
                    f.write('最高價: '+str(price_max)+'\n')
                    f.write('售出數量: '+str(historical_sold)+'\n')
                    f.write('評分: '+str(rating_star)+'\n')
                    f.write('商品位置: '+shop_location+'\n')
                    f.write('\n')
                
            
        
        except WebDriverException:    
            pass