from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request

url = "https://www.cbnews.kr/news/articleView.html?idxno=211826"
html = urlopen(url)
bsObject = BeautifulSoup(html, "html.parser")

getImageUrl = bsObject.select_one('figure > img')
src = getImageUrl.get('src')

savePath = url + '.jpg'

print(src)
print(savePath)

urllib.request.urlretrieve(src, 01.jpg)