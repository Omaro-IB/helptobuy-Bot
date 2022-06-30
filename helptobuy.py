import requests
from bs4 import BeautifulSoup as bs

def register_interest(yourAuthCookie, url, address):
    cookies = {
        "yourAuthCookie": yourAuthCookie
    }
    s = requests.Session()
    r = s.get(url, cookies=cookies)
    if "You need to login or register with Help to Buy Agent for the South before you can express interest in a property" in r.text:
        raise ValueError("Invalid Authorization Cookie")

    pos = url.find("id")
    id_ = url[pos+3:pos+8]
    params = {
        "id": id_,
        "address": address
    }
    r2 = s.post("https://helptobuyagent3.org.uk/umbraco/surface/htbapi/registerinterest", cookies=cookies, params=params)
    print("posted request with params "+"id="+id_+", address="+address)

def findNewest():
    # extract dataLine from HTML
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    page = requests.get("https://helptobuyagent3.org.uk/find-a-home/", headers=headers)
    soup = bs(page.content, 'html.parser')
    html = str(list(soup.children))
    begin = html.find('<div class="container-fluid search-page')
    end = html[11088:].find(">")
    dataLine = html[begin:end]

    # find ID,PTypeID_loc,Bedrooms, and Title
    ID_loc = dataLine.find(',"ID":')
    ID = dataLine[ID_loc+6:ID_loc+11]

    PTypeID_loc = dataLine.find(',"PTypeID":')
    PTypeID = dataLine[PTypeID_loc+11]

    Bedrooms_loc = dataLine.find(',"Bedrooms":')
    Bedrooms = dataLine[Bedrooms_loc+12]

    Title_loc = dataLine.find(',"Title":')
    Title = ""
    for i in dataLine[Title_loc+10:]:
        if i == '"':
            break
        Title = Title+i

    url = "https://helptobuyagent3.org.uk/find-a-home/property-details?id={}&bedrooms={}&IDType={}".format(ID, Bedrooms, PTypeID)
    return url, Title
