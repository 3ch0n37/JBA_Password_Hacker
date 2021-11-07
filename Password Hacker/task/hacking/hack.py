import argparse
import itertools
import sys
import socket
import string


def password_gen(chars):
    for r in range(1, len(chars)):
        for item in itertools.product(chars, repeat=r):
            yield "".join(item)


def crack(hostname, port):
    with socket.socket() as sock:
        sock.connect((hostname, port))
        for p in password_gen(list(string.ascii_lowercase + string.digits)):
            sock.send(p.encode())
            res = sock.recv(1024)
            if res.decode() == "Connection success!":
                return p
            elif res.decode() == "Too many attempts":
                return False


def main():
    parser = argparse.ArgumentParser(description="Program that cracks passwords")
    parser.add_argument("hostname", type=str)
    parser.add_argument("port", type=int)
    args = parser.parse_args(sys.argv[1:])
    if args.hostname and args.port:
        print(crack(args.hostname, args.port))
    else:
        print("Incorrect parameters")


if __name__ == '__main__':
    main()
