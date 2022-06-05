import urllib3
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#파이어베이스 연동
cred = credentials.Certificate("test-89e6b-firebase-adminsdk-eanky-f05e3ec9e6.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


name = "Tokyo"
dt_duration = "123"
address = "asdasd"

city = db.collection(u'POPUP').document()
city.set({
    u'TITLE' : name,
    u'URL' : dt_duration,
    u'THUMBNAIL' : address 
})



openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU_spoken"

accessKey = 'fa776eba-2bca-4bed-84b9-2a2f9df8e111'
analysisCode = 'ner'
text = "팝업스토어 참가 조건 안내팝업스토어 컨셉 및 주요사항5월 가정의 달 특집전, 옥상정원 피크닉 이벤트 기간패션잡화 / 쥬얼리 / 1020타겟의류 / 아웃도어 / 캠핑 카테고리 우선 선정동기간 동장소에서 피크닉 이벤트 (솜사탕 및 프리드링크, 돗자리 제공) 진행 예정팝업일정 및 영업시간공간: 수원 AK 백화점 7층 옥상 정원일정: 5/5(목) ~ 5/15(일), 11일간영업시간: 10:30 ~ 20:00 (단, 금~일은 10:30 ~ 20:30)팝업공간 안내참여 브랜드 규모 : 5 ~ 6개 브랜드주요 고객층 : 102030 젊은 층 고객팝업자 준비사항판매사원(필수)연출소품 및 간이의자제공사항판매용 테이블/매대(무상)결제 단말기(공용)전기참가비용 및 정산수수료 조건(총매출액의 계약 수수료율 적용)정산일정 : 계약서 맨 마지막 장 확인모집마감04월 24일셀러발표04월 25일참가신청 취소신청기간 내 자진 취소셀러발표 후 취소 불가"

requestJson = {
    "access_key": accessKey,
    "argument": {
        "text": text,
        "analysis_code": analysisCode
    }
}

http = urllib3.PoolManager()
response = http.request(
    "POST",
    openApiURL,
    headers={"Content-Type": "application/json; charset=UTF-8"},
    body=json.dumps(requestJson)
)
 
#print("[responseCode] " + str(response.status))
#print("[responBody]")
#print(str(response.data,"utf-8"))


with open("result.json", "w", encoding="utf-8") as json_file:
    json_data = json.loads(response.data)
    json.dump(json_data, json_file, indent=2, ensure_ascii=False)



jsonArray = json_data['return_object']['sentence']

for i in jsonArray:
    jsonArray2 = i['NE']

for j in jsonArray2:
    jsonArray3 = j['type'] + j['text']
    if j['type'] == "DT_DURATION":
        print("\n[기간] : ", end='')
        print(j['text'])
    elif j['type'] == "TI_DURATION":
        print("\n[운영시간] : ", end='')
        print(j['text'])


