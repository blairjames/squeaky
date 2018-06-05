#!/usr/bin/env python3

import requests

def get_ip_address():
    res = requests.get("https://ifconfig.co/")
    print(res.text)


def main():
    get_ip_address()


if __name__ == '__main__':
    main()