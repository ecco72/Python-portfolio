from selenium import webdriver
from bs4 import BeautifulSoup
import time

adults = input('請問幾名大人?\n')
rooms = input('請問需要幾間房間?\n')
checkIn = input('請問入住日期? ex:2023-11-20 \n')
checkOut = input('請問退房日期? ex:2023-12-01 \n')

url = f'https://www.agoda.com/zh-tw/search?city=12080&checkIn={checkIn}&los=1&rooms={rooms}&adults={adults}&children=0&checkOut={checkOut}'
driver = webdriver.Chrome()
driver.implicitly_wait(6) #設定一個秒數等待資料回傳 時間內沒有回傳就是timeout
time.sleep(2)
driver.get(url)

while True:
    for i in range(40):    #頁面較長 所以重複40次
        driver.execute_script('window.scrollBy(0,850)')
        time.sleep(0.8)  #為了避免網路速度跟不上 設定1.5秒
    soup = BeautifulSoup(driver.page_source,'html.parser')
    
    j=0   #j是串列索引值
    for j in range(2):
        tophotels = soup.find_all('ol',{'class':'hotel-list-container'})[j]
        toplis = tophotels.find_all('li')
        for li in toplis:
            if li.get('data-selenium') != None:
                hotel = li.find('a').get('aria-label')
                print('飯店名稱:',hotel)
                
                if li.find('a').get('href') != None:   #有時有些飯店會沒有連結，避免錯誤
                    link = 'https://www.agoda.com/'+li.find('a').get('href')
                    print('訂房連結:', link)
                    
                if li.find('div', class_='soldOut__content') !=None:    #此class為已售完飯店才有的class
                    print('這個日期沒有房間了！ \n')
                else:
                    rightprice = li.find('div', class_='Box-sc-kv6pi1-0 gDVubK')
                    twoprice = rightprice.find('ul', class_='List__List List__List--Vertical')                                 
                    prices = twoprice.find_all('li')
                    
                    if len(prices) == 2:    #價格內的列表長度為2時有兩種狀況：1. 折扣前、折扣後 2.原價、會員價
                        prices = twoprice.find_all('li')[1]
                        if prices.find('span') != None:
                            prices = twoprice.find_all('li')[0]
                            bp = prices.find('div').text
                            print('折扣前價格:', bp)
                            
                            prices = twoprice.find_all('li')[1]
                            ap = prices.find_all('span')[2].text
                            print('折扣後價格:', ap)
                            
                        else:
                            prices = twoprice.find('li')
                            ap = prices.find_all('span')[2].text
                            print('原價:', ap)
                            
                            prices = twoprice.find_all('li')[1]
                            ap = prices.find_all('div')[3].text
                            print('會員價:', ap)
                        
                    elif len(prices) == 3:
                        prices = twoprice.find_all('li')[0]
                        bp = prices.find('div').text
                        print('折扣前價格:', bp)
                        
                        prices = twoprice.find_all('li')[1]
                        ap = prices.find_all('span')[2].text
                        print('折扣後價格:', ap)
                        
                        prices = twoprice.find_all('li')[2]
                        ap = prices.find_all('div')[3].text
                        print('會員價:', ap)
                        
                    elif twoprice.find('span') == None:
                        print('這個日期沒有房間了！')
                    else:
                        prices = twoprice.find('li')
                        ap = prices.find_all('span')[2].text
                        print('原價:', ap)
                    print()   

    topbutton = soup.find(id = 'paginationContainer')
    if topbutton.find(id = 'paginationNext') != None:   #下一頁按鈕
        driver.execute_script("document.getElementById('paginationNext').click()")
        time.sleep(3)
    else:
        break
