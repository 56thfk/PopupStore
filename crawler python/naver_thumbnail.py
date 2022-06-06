from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request

def getThumbnail(getUrl):
    url = getUrl
    html = urlopen(url)
    bsObject = BeautifulSoup(html, "html.parser")

    try:
        getImageUrl = bsObject.select_one('div > img')
        src = getImageUrl.get('src')
        #savePath = str(src.replace("https:\\", "").replace("/", "").replace(":", ""))

        print(src)
    except:
        print("이미지 불러올 수 없음")
        #print(savePath)

        #이미지 다운
        #urllib.request.urlretrieve(src, savePath)

    return src

    

#테스트#
# url = "http://www.pinpointnews.co.kr/news/articleView.html?idxno=120847"
# html = urlopen(url)
# bsObject = BeautifulSoup(html, "html.parser")

# getImageUrl = bsObject.select_one('div > img')
# src = getImageUrl.get('src')
# savePath = str(src.replace("https:\\", "").replace("/", "").replace(":", ""))

# urllib.request.urlretrieve(src, savePath)

# print(src)
# print(savePath)