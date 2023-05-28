#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import random
from _md5 import md5


def generate_random_str():
    randomlength = 16
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return md5(random_str.encode()).hexdigest()

