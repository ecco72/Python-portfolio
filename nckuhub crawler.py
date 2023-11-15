import requests
import json

header ={'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
url = 'https://nckuhub.com/course/'

choose = {}
data = requests.get(url, headers = header).text
allc = json.loads(data)
courses = allc['courses']
for course in courses:
    choose[course['課程名稱']] = course['id']

which_class = input('請輸入要查詢課程名稱(不輸入則查詢全部): \n')
if which_class == '':
    courses = allc['courses']
    for course in courses:
        choose[course['課程名稱']] = course['id']
        classid = course['id']
        url = f'https://nckuhub.com/course/{classid}'
        data = requests.get(url, headers = header).text
        chooseclass = json.loads(data)
        
        got = int(float(chooseclass['got']))
        cold = int(float(chooseclass['cold']))
        sweet = int(float(chooseclass['sweet']))
        teacher = chooseclass['courseInfo']['老師']
        name = chooseclass['courseInfo']['課程名稱']
        time = chooseclass['courseInfo']['時間']
        print(f'收穫:{got},甜度:{sweet},涼度:{cold},課程名稱:{name},老師:{teacher},上課時間:{time}')
else:
    classid = choose[which_class]
    url = f'https://nckuhub.com/course/{classid}'
    data = requests.get(url, headers = header).text
    chooseclass = json.loads(data)
    
    got = int(float(chooseclass['got']))
    cold = int(float(chooseclass['cold']))
    sweet = int(float(chooseclass['sweet']))
    teacher = chooseclass['courseInfo']['老師']
    name = chooseclass['courseInfo']['課程名稱']
    time = chooseclass['courseInfo']['時間']
    print(f'收穫:{got},甜度:{sweet},涼度:{cold},課程名稱:{name},老師:{teacher},上課時間:{time}')