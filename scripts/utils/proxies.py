import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent
import goslate
import urllib.request as urllib2

def get_proxies(link):   
    response = requests.get(link)
    soup = BeautifulSoup(response.text,"html.parser")
    proxies = [':'.join([item.select_one("td").text,item.select_one("td:nth-of-type(2)").text]) for item in soup.select("table.table tr") if "yes" in item.text]
    return proxies

def filter_proxies():
    items = []
    for link in ['https://www.us-proxy.org/','https://free-proxy-list.net/uk-proxy.html','https://www.sslproxies.org/','https://free-proxy-list.net/']:
        proxies = get_proxies(link)
        items.extend(proxies)
        random.shuffle(items)
    return items

# Produce random user agent
ua = UserAgent()

proxies = filter_proxies()
index = 0

def get_proxy():
    global index
    if(index > len(proxies)):
        index = 0
    returnVal = {"https": f'http://{proxies[index]}'}
    index += 1
    return returnVal

if __name__ == '__main__':

    text = "Καλημέρα με λένε Μιχάλη."
    print(get_proxy())
    proxy_handler = urllib2.ProxyHandler(get_proxy())
    proxy_opener = urllib2.build_opener(urllib2.HTTPHandler(proxy_handler), 
                                        urllib2.HTTPSHandler(proxy_handler))
    gs_with_proxy = goslate.Goslate(opener=proxy_opener)
    translation = gs_with_proxy.translate(text, "el")

    
