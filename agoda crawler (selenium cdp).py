from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
import csv

checkin = input('請輸入入住日期:  ex:2023-11-20 \n')
checkout = input('請輸入退房日期:  ex:2023-11-20 \n')
adults = input('請問有幾位? \n')
rooms = input('請問需要幾間房間? \n')

mcheckin = datetime.strptime(checkin, '%Y-%m-%d')   #為了算出los(住幾天) 日期轉換
mcheckout = datetime.strptime(checkout, '%Y-%m-%d')
los = mcheckout-mcheckin
los = los.days

url= f'https://www.agoda.com/zh-tw/search?city=12080&locale=zh-tw&checkIn={checkin}&checkOut={checkout}&rooms={rooms}&adults={adults}&children=0&priceCur=TWD'
urlfront = 'https://www.agoda.com/zh-tw'
urlback= f'?finalPriceView=1&isShowMobileAppPrice=false&cid=-1&numberOfBedrooms=&familyMode=false&adults={adults}&children=0&rooms={rooms}&maxRooms=0&isCalendarCallout=false&childAges=&numberOfGuest=0&missingChildAges=false&travellerType=3&showReviewSubmissionEntry=false&currencyCode=TWD&isFreeOccSearch=false&isCityHaveAsq=false&los={los}&checkin={checkin}'

options = Options()
caps = {                          #開啟日誌監聽
        "browserName": "chrome",
        'goog:loggingPrefs': {'performance': 'ALL'}
        }

for key, value in caps.items():  # 將caps添加到options中
    options.set_capability(key, value)
 
browser = webdriver.Chrome(options=options)
browser.get(url)
browser.implicitly_wait(5)
time.sleep(3)

while True:    #滾動頁面 並且切換到下一頁
    for i in range(17):
        browser.execute_script('window.scrollBy(0,2000)')
        time.sleep(0.6)
    soup = BeautifulSoup(browser.page_source,'html.parser')
    topbutton = soup.find(id = 'paginationContainer')
    if topbutton.find(id = 'paginationNext') != None:   #下一頁按鈕
        browser.execute_script("document.getElementById('paginationNext').click()")
        time.sleep(3)
    else:
        break

def filter_type(_type: str):   #設定要過濾的type
    types = [
        'application/javascript', 'application/x-javascript', 'text/css', 'webp', 'image/png', 'image/gif',
        'image/jpeg', 'image/x-icon', 'application/octet-stream', 'image/svg+xml', 'image/webp', 'text/html',
        'font/x-woff2','text/plain'
        ]
    if _type not in types:
        return True
    return False

with open('agoda_search_result.csv', 'w', newline='') as f:   #清空輸出的檔案
    f.close()

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
    if url != 'https://www.agoda.com/graphql/search':
        continue
    
    try:
        resp = browser.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId}) #使用 cdp
        respstr = str(resp).replace("{'base64Encoded': False, 'body': '{", '{').replace("}}}'}", '}}}').replace('\\', '')
        
        if '{"data":{"citySearch":{"featuredPulseProperties":' in respstr:
            agoda = json.loads(respstr)
            special = agoda['data']['citySearch']['featuredPulseProperties']
            for s in special:
                name = s['content']['informationSummary']['displayName']
                area = s['content']['informationSummary']['address']['area']['name']
                rating = s['content']['informationSummary']['rating']
                link = urlfront + s['content']['informationSummary']['propertyLinks']['propertyPage'] + urlback
                price = s['pricing']['offers'][0]['roomOffers'][0]['room']['pricing'][0]['price']['perRoomPerNight']['exclusive']['display']
                    
                with open('agoda_search_result.csv', 'a', encoding='UTF-8-sig',newline='') as f:
                    writer = csv.writer(f)
                    
                    fObj = open("agoda_search_result.csv", "r",encoding='UTF-8-sig')   #檢查csv檔案內是否有重複 若有則略過
                    allLines = fObj.readlines()
                    fObj.close()
                    
                    if not '飯店名稱:,'+name+'\n' in allLines:
                        writer.writerow(['飯店名稱:',name])
                        writer.writerow(['位置:',area])
                        writer.writerow(['星級:',rating])
                        writer.writerow(['連結:',link])
                        writer.writerow(['價格:',price])
                        writer.writerow([' '])
        
            normal = agoda['data']['citySearch']['properties']
            for n in normal:
                name = n['content']['informationSummary']['displayName']
                area = n['content']['informationSummary']['address']['area']['name']
                rating = n['content']['informationSummary']['rating']
                if n['content']['informationSummary'].get('propertyLinks') != None:
                    link = urlfront + n['content']['informationSummary']['propertyLinks']['propertyPage'] + urlback
                else:
                    link='沒有連結！'
                if n['pricing']['isAvailable'] == False:
                    price = '這天已經沒有空房了！'
                else:
                    price = n['pricing']['offers'][0]['roomOffers'][0]['room']['pricing'][0]['price']['perRoomPerNight']['exclusive']['display']
                    
                with open('agoda_search_result.csv', 'a', encoding='UTF-8-sig',newline='') as f:
                    writer = csv.writer(f)
                    
                    fObj = open("agoda_search_result.csv", "r",encoding='UTF-8-sig')
                    allLines = fObj.readlines()
                    fObj.close()
                    
                    if not '飯店名稱:,'+name+'\n' in allLines:
                        writer.writerow(['飯店名稱:',name])
                        writer.writerow(['位置:',area])
                        writer.writerow(['星級:',rating])
                        writer.writerow(['連結:',link])
                        writer.writerow(['價格:',price])
                        writer.writerow([' '])
                        
    #網頁可能在程式執行cdp之後還有請求，會導致出現這個錯誤，因為要抓的<search> json 在執行cdp前就已讀取完畢，可以忽略這個錯誤
    except WebDriverException:    
        pass
browser.close()    
print('搜尋結果已匯出至本檔同資料夾。')
