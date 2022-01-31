from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

siteURL = "https://www.investing.com/funds/allan-gray-balanced-fund-c-chart"
request = Request(siteURL, headers={'User-Agent': 'Mozilla/5.0'})
webPage = urlopen(request).read()
pageSoup = BeautifulSoup(webPage, "lxml")


def getExtractedData(soup):
    currentData = soup.find('div', class_="overViewBox instrument")
    fundName = soup.find('h1', class_='float_lang_base_1 relativeAttr').text.replace('\t', '')
    # Extracting group of data from the left general infor Div
    generalInforLeft = currentData.find('div', class_="left current-data")
    fundPrice = generalInforLeft.find('span', class_='arial_26 inlineblock pid-1030835-last').text.replace('\t', '')
    dailyMovement = generalInforLeft.find('span', class_='bold pid-1030835-time').text
    # Extracting group of data from the right general infor Div
    generalInforRight = currentData.find('div', class_="right general-info")

    fundData = generalInforRight.find_all('div')

    fundDetails = {"name": fundName}
    extractDataFromDIV(fundData, fundDetails)

    fundDetails['price'] = fundPrice
    fundDetails['daily_movement'] = dailyMovement
    fundDetails['morning_star_rating'] = "{} stars".format(calculateRating(currentData))
    return fundDetails


def extractDataFromDIV(fundData, fundDetails):
    for item in fundData:
        spans = item.find_all('span')
        itemKey = spans[0].text.replace(':', '')
        itemValue = spans[1].text

        if itemKey.lower() == 'market':
            continue
        if itemKey == "ISIN":
            itemValue = itemValue[:12]
        if itemKey == 'Asset Class':
            itemKey = 'class'
        fundDetails[itemKey.lower()] = itemValue


def calculateRating(currentData):
    starRating = currentData.find('span', class_='morningStarsWrap')
    darkStarRating = starRating.find_all('i', class_='morningStarDark')
    return len(darkStarRating)


if __name__ == '__main__':
    [print(key, ':', value) for key, value in getExtractedData(pageSoup).items()]
