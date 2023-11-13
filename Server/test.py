import urllib.request
import ssl
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def ClearBaseUrl(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    cleanUrl=domain
    # .replace("www.", "")
    return cleanUrl


def checkUrl(href,base_url):

        notALink=["#","javascript:void(0)","\\'javascript:void(0);\\'","javascript:void(0);","None",None,base_url]
        if(href not in notALink):
            if (href.startswith("/") or href.startswith("./")):
                if(href.startswith("./")):
                    newurl=base_url+href[2:]
                else:
                    newurl=base_url+href[1:]
                return newurl
            else:
                if(href.startswith("#")):
                    return False
                else:
                    if(not href.startswith("http")):
                        return False
                    else:
                        return href
        else:
            return False

def valiadteSameUrl(Url,BaseUrl,cleanUrl)->bool:
    if cleanUrl=="www."+BaseUrl:
        return True
    else:
        switchUrl={
            f"http://{BaseUrl}/":True,
            f"https://{BaseUrl}/":True,
            f"http://{BaseUrl}":True,
            f"https://{BaseUrl}":True
        }
        return switchUrl.get(Url,False);
        
    


def testing_url():
    context = ssl._create_unverified_context()
    base_url="https://www.w3schools.com/"
    # base_url="https://ramsol.in/"
    weburl = urllib.request.urlopen(base_url, context=context)
    html_page=str(weburl.read())
    soup=BeautifulSoup(html_page,'lxml')
    links=soup.findAll("a")
    myset=set()
    for link in links:
        href=link.get("href")
        ThisUrl=checkUrl(href,base_url)
        if ThisUrl:
            cleanUrl=ClearBaseUrl(ThisUrl)
            BaseUrl=ClearBaseUrl(base_url)
            if (cleanUrl in base_url) or (BaseUrl in cleanUrl):
                if valiadteSameUrl(ThisUrl,BaseUrl,cleanUrl):
                    print("Not in Url1: ",ThisUrl)
                elif "?" in ThisUrl:
                    myset.add(ThisUrl.split("?")[0])
                else:
                    myset.add(ThisUrl)

testing_url()
