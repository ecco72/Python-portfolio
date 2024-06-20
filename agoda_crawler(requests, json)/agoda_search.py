import requests
import json
from datetime import datetime, timedelta
import csv

def minus_one_day(x):    #減一天
    x = datetime.strptime(x, '%Y-%m-%d')
    y = x + timedelta(days=-1)
    y = datetime.strftime(y, '%Y-%m-%d')
    return y

checkin = input('請輸入Check In 日期:  ex:2023-11-20 \n')
checkout = input('請輸入Check out 日期:  ex:2023-11-20 \n')
adults = input('請問有幾位? \n')
rooms = input('請問需要幾間房間? \n')

mcheckin = datetime.strptime(checkin, '%Y-%m-%d')   #為了算出los(住幾天) 日期轉換
mcheckout = datetime.strptime(checkout, '%Y-%m-%d')
los = mcheckout-mcheckin
los = los.days

with open('payload.json', 'r') as file:   #將原先payload參數改掉
    data = json.load(file)
    data["variables"]["CitySearchRequest"]["searchRequest"]["searchCriteria"]["checkInDate"] = minus_one_day(checkin) +'T16:00:00.000Z'
    data["variables"]["CitySearchRequest"]["searchRequest"]["searchCriteria"]["localCheckInDate"] = checkin
    data["variables"]["ContentSummaryRequest"]["context"]["occupancy"]["checkIn"] = minus_one_day(checkin)+'T16:00:00.000Z'
    data["variables"]["PricingSummaryRequest"]["pricing"]["checkIn"] = minus_one_day(checkin)+'T16:00:00.000Z'
    data["variables"]["PricingSummaryRequest"]["pricing"]["checkout"] = minus_one_day(checkout) +'T16:00:00.000Z'
    data["variables"]["PricingSummaryRequest"]["pricing"]["localCheckInDate"] = checkin
    data["variables"]["PricingSummaryRequest"]["pricing"]["localCheckoutDate"] = checkout
    data["variables"]["CitySearchRequest"]["searchRequest"]["searchCriteria"]["los"] = los
    data["variables"]["CitySearchRequest"]["searchRequest"]["searchCriteria"]["rooms"] = int(rooms)
    data["variables"]["CitySearchRequest"]["searchRequest"]["searchCriteria"]["adults"] = int(adults)
    data["variables"]["PricingSummaryRequest"]["pricing"]["occupancy"]["adults"] = int(adults)
    data["variables"]["PricingSummaryRequest"]["pricing"]["occupancy"]["rooms"] = int(rooms)
    data["variables"]["ContentSummaryRequest"]["context"]["occupancy"]["numberOfAdults"] = int(adults)
    
    newData = json.dumps(data, indent=4)

with open('search_payload.json', 'w') as file:  #寫入到另一個檔案
    file.write(newData)


url='https://www.agoda.com/graphql/search'
urlfront = 'https://www.agoda.com/zh-tw'
urlback= f'?finalPriceView=1&isShowMobileAppPrice=false&cid=-1&numberOfBedrooms=&familyMode=false&adults={adults}&children=0&rooms={rooms}&maxRooms=0&isCalendarCallout=false&childAges=&numberOfGuest=0&missingChildAges=false&travellerType=3&showReviewSubmissionEntry=false&currencyCode=TWD&isFreeOccSearch=false&isCityHaveAsq=false&los=10&checkin={checkin}'

header={'Content-Type': 'application/json',
        'Ag-Language-Locale': 'zh-tw',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }

f = open('payload.json')
data = json.load(f)
f.close()

agoda = requests.post(url, headers=header, json=data).text
result = json.loads(agoda)

special = result['data']['citySearch']['featuredPulseProperties']
for s in special:
    name = s['content']['informationSummary']['displayName']
    area = s['content']['informationSummary']['address']['area']['name']
    rating = s['content']['informationSummary']['rating']
    link = urlfront+ s['content']['informationSummary']['propertyLinks']['propertyPage']+urlback
    price = s['pricing']['offers'][0]['roomOffers'][0]['room']['pricing'][0]['price']['perRoomPerNight']['inclusive']['display']

    with open('agoda_search_result.csv', 'w', encoding='UTF-8-sig',newline='') as f:
        writer = csv.writer(f)
    
        writer.writerow(['飯店名稱:',name])
        writer.writerow(['位置:',area])
        writer.writerow(['星級:',rating])
        writer.writerow(['連結:',link])
        writer.writerow(['價格:',price])
        writer.writerow([' '])

normal = result['data']['citySearch']['properties']
for n in normal:
    name = n['content']['informationSummary']['displayName']
    area = n['content']['informationSummary']['address']['area']['name']
    rating = n['content']['informationSummary']['rating']
    link = urlfront+ n['content']['informationSummary']['propertyLinks']['propertyPage'] +urlback
    if n['pricing']['isAvailable'] == False:
        price = '這天已經沒有空房了！'
    else:
        price = n['pricing']['offers'][0]['roomOffers'][0]['room']['pricing'][0]['price']['perRoomPerNight']['inclusive']['display']

    with open('agoda_search_result.csv', 'a', encoding='UTF-8-sig',newline='') as f:
        writer = csv.writer(f)
    
        writer.writerow(['飯店名稱:',name])
        writer.writerow(['位置:',area])
        writer.writerow(['星級:',rating])
        writer.writerow(['連結:',link])
        writer.writerow(['價格:',price])
        writer.writerow([' '])
        
print('搜尋結果已匯出至本檔同資料夾。')