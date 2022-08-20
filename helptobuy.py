import requests
from bs4 import BeautifulSoup as bs

def validate_cookie(yourAuthCookie, url):
    cookies = {
        "yourAuthCookie": yourAuthCookie
    }
    s = requests.Session()
    r = s.get(url, cookies=cookies)
    s2 = requests.Session()
    r2 = s2.get("https://helptobuyagent3.org.uk", cookies=cookies)
    if "You need to login or register with Help to Buy Agent for the South before you can express interest in a property" in r.text:
        return False
    if not ("My Homepage" in r2.text and "Logout" in r2.text):
        print("Second one")
        return False
    return True

def register_interest(yourAuthCookie, url, address):
    if not validate_cookie(yourAuthCookie, url):
        raise ValueError("Invalid Authorization Cookie")

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

def dummy_request(url, yourAuthCookie, Title):
    cookies = {
        "yourAuthCookie": yourAuthCookie
    }
    s = requests.Session()
    r = s.get(url, cookies=cookies)

    pos = url.find("id")
    id_ = url[pos+3:pos+8]
    address = Title.replace(" ", "+")
    params = {
        "id": id_,
        "address": address
    }
    r2 = s.post("https://helptobuyagent3.org.uk/umbraco/surface/htbapi/registerinterest", cookies=cookies, params=params)
    return str(params) + " - " + str(r2)

def findNewest():
    # extract dataLine from HTML
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    page = requests.get("https://helptobuyagent3.org.uk/find-a-home/?loc=Bristol+BS7%2C+UK&dst=20&Tenure=b&Type=0&PropertyDeveloper=0&Garden=0&DaysAdded=0&Sort=dateadded-desc&BedroomsMin=0&BedroomsMax=6&lat=51.48144689999999&lng=-2.5797458&sloc=Bristol+BS7%2C+UK&setnum=0&pagenum=1&maxrows=0&numresults=12&initialpaging=initialpaging&g-recaptcha-response=03AGdBq24p5n56Re7FHPdRf7g--VysBQqximLORl1hXHZBha31fW3sBFqo1qOI3imNQTDOfujxD9n1dUUs7w5P2y36TYAXQoHlhAhCbuZ-t69xke9MRuV0h1m6Ne280yUlEPgZRqdrE6xN0hdZo3mJLPe2FNPBvPpssaTnhbU678Wj2W9VJlDRT2pQ5yG64tRzV--y7VtdrCmXi0VSU97aimM9ZlmKxR30UwiCuztypfboY1UNYNqaAIvwMP0WkVH2BaFNNZB8GcGVWbU5osXn-VXSz3rP-0CBvbX9JLno9g3M5LpnchpCCwCzUyqtyr4m2nP_u5SR3-Toupjg4XqfwZWk573_pgOZRtuJlesLQHIjJBCoKYffUyijf7b29TeH64pJq_kKhGXCFL9ORcxt20vfpv8eFmiduZHtQszgHP_yNihsdXBrcWeQuuFF130OPCtJ_gzVz6l2w0ZemHj5O6uU0_WdQRUk6w", headers=headers)
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
