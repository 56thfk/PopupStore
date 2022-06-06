import re
import json
import urllib.request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import naver_thumbnail

#파이어베이스 연동
cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

#client 아이디, 시크릿
client_id = "rWDfDdzRuHWK3UE3vkMZ"
client_secret = "TJEkpxfkrw"

def cleanText(text):
    cleanText = re.sub('</b>|<b>|&quot;|','', text)
    removeBracket = re.sub(r'\[[^)]*\].', '',cleanText)

    return removeBracket


encText = urllib.parse.quote("팝업스토어 오픈")
naverUrl = "https://openapi.naver.com/v1/search/news?query=" + encText + "&display=30&sort=date"

request = urllib.request.Request(naverUrl)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()

if(rescode==200):
    response_body = response.read()
    #print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)

with open("naver_result.json", "w", encoding="utf-8") as json_file:
    json_data = json.loads(response_body)
    json.dump(json_data, json_file, indent=2, ensure_ascii=False)


jsonArray = json_data.get('items')
for list in jsonArray:
    title = list.get('title')
    title = cleanText(title)
    url = list.get('originallink')
    try:
        thumbnail = naver_thumbnail.getThumbnail(url)
    except:
        print("이미지 불러올 수 없음")
    date = list.get('pubDate')
    
    #News 컬렉션
    popup = db.collection(u'News').document()
    popup.set({
        u'Title' : title,
        u'Url' : url,
        u'Thumbnail' : thumbnail,
        u'Date' : date 
    }, merge=True)


