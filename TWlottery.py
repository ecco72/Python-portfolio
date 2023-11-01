import requests
from bs4 import BeautifulSoup

header ={'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    
url ='https://www.taiwanlottery.com.tw/index_new.aspx'

data = requests.get(url, headers = header).text

soup = BeautifulSoup(data, 'html.parser')

bigarea = soup.find(id = 'rightdown')

#抓取bingo bingo---------------------------------------------------
bingo = bigarea.find('div',class_ = 'ball_box01')
print('bingo bingo')
print('開出獎號:')
print(bingo.text)

superb = bigarea.find_all('div', class_='ball_red')[0].text
bigorsmall = bigarea.find('div', class_='ball_blue_BB1').text
single = bigarea.find('div', class_='ball_blue_BB2').text
print('超級獎號:',superb)
print('猜大小:',bigorsmall)
print('猜單雙:',single)
print()

#抓取雙贏彩---------------------------------------------------------
double = bigarea.find_all('div', class_='ball_tx ball_blue')[:12]
print('雙贏彩')
print('開出順序:')
for d in double:
    print(d.text, end='')
print()

double = bigarea.find_all('div', class_='ball_tx ball_blue')[12:]
print('大小順序:')
for d in double:
    print(d.text, end='')
print()
print()

#抓取威力彩---------------------------------------------------------
msg=''
msg1=''
power = bigarea.find_all('div', class_= 'contents_box02')[0]
powerball = power.find_all('div', class_= 'ball_tx ball_green')[:6]
print('威力彩')
print('開出順序:')
for po in powerball:
    msg += po.text
print(msg, end='')
print()

powerball = power.find_all('div', class_= 'ball_tx ball_green')[6:]
print('大小順序:')
for p in powerball:
    msg1 += p.text
print(msg1, end='')
print()
print('第二區')
second = bigarea.find_all('div', class_='ball_red')[1]
print(second.text)
print()

#抓取樂合彩---------------------------------------------------------
print('38樂合彩')
print('開出順序:')
print(msg, end='\n')
print('大小順序:')
print(msg1, end='\n')
print()

#抓取大樂透---------------------------------------------------------
bigmsg = ''
bigmsg1= ''
big = bigarea.find_all('div', class_= 'contents_box02')[2]
bigball = big.find_all('div', class_= 'ball_tx ball_yellow')[:6]
print('大樂透')
print('開出順序:')
for po in bigball:
    bigmsg += po.text
print(bigmsg, end='\n')

bigball = big.find_all('div', class_= 'ball_tx ball_yellow')[6:]
print('大小順序:')
for p in bigball:
    bigmsg1 += p.text
print(bigmsg1, end='\n')

print('第二區')
second = bigarea.find_all('div', class_='ball_red')[2]
print(second.text)
print()

#抓取樂合彩---------------------------------------------------------
print('49樂合彩')
print('開出順序:')
print(bigmsg, end='\n')
print('大小順序:')
print(bigmsg1, end='\n')
print()

#抓取今彩539--------------------------------------------------------
fivemsg=''
fivemsg1=''
five = bigarea.find_all('div', class_= 'contents_box03')[0]
fiveball = five.find_all('div', class_='ball_tx ball_lemon')[:5]
print('今彩539')
print('開出順序:')
for po in fiveball:
    fivemsg += po.text
print(fivemsg, end='\n')

fiveball = five.find_all('div', class_='ball_tx ball_lemon')[5:]
print('大小順序:')
for p in fiveball:
    fivemsg1 += p.text
print(fivemsg1, end='\n')
print()

#抓取樂合彩---------------------------------------------------------
print('39樂合彩')
print('開出順序:')
print(fivemsg, end='\n')
print('大小順序:')
print(fivemsg1, end='\n')
print()

#抓取3星彩----------------------------------------------------------
threestar = bigarea.find_all('div', class_= 'contents_box04')[0]
tball = threestar.find_all('div', class_= 'ball_tx ball_purple')
print('3星彩')
for t in tball:
    print(t.text, end=' ')
print()
print()

#抓取4星彩----------------------------------------------------------
fourstar = bigarea.find_all('div', class_= 'contents_box04')[1]
fball = fourstar.find_all('div', class_= 'ball_tx ball_purple')
print('4星彩')
for f in fball:
    print(f.text, end=' ')
