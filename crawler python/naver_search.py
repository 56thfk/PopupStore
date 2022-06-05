import os
import sys
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



encText = urllib.parse.quote("팝업스토어")
naverUrl = "https://openapi.naver.com/v1/search/news?query=" + encText + "&display=10&sort=date"

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
    url = list.get('link')
    thumbnail = naver_thumbnail.getThumbnail(url)
    city = db.collection(u'POPUP').document()
    city.set({
        u'TITLE' : title,
        u'URL' : url,
        u'THUMBNAIL' : thumbnail 
    })


