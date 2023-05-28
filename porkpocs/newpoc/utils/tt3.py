#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing.dummy import Pool

import requests
import time

def burp(a):

    s = requests.get(url="http://1.14.140.155:14444/?rid=4rlSWEK")
    print(s.text)


if __name__ == "__main__":
    # list = [i for i in range(2000)]
    test = Pool(50)
    for i in range(2000):
        test.imap(burp, [i, ])
    test.close()
    test.join()
