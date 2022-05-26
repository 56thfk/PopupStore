from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://www.sweetspot.co.kr/market/schedule?")
bsObject = BeautifulSoup(html, "html.parser")

findData = bsObject.find('div', {"class":"Schedule__MarketIcon-sc-4pxoi0-14 kiRTjS"})
findLocation = bsObject.find_all('div', {"class":"Schedule__MarketAddressDiv-sc-4pxoi0-17 heakNE"})

print(findLocation)