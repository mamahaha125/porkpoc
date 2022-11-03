#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import functools
import json

def read_json(filename):
     with open(filename, 'r', encoding='utf-8') as f:
          return f.readlines()

def write(fine_detail):
    with open("NC.txt", 'w') as f:
        [f.write(i+'\n') for i in fine_detail]


# 通达
class Tongda:
    def __init__(self):
        pass

    def tongda_rce(self):
        payload = read_json('data/Tongda/tongda.json')
        payload = [(json.loads(pay)['title'], json.loads(pay)['id']) for pay in payload if
                   '医院' not in json.loads(pay)['title'] and '政府' not in json.loads(pay)['title']]
        for i in payload:
            print(i)

    def mongoDB(self):
        payload = read_json('data/MongoDB/MongoDB.json')
        payload = [json.loads(pay)['id'] for pay in payload]
        return payload[-500:]

    def redis(self):
        payload = read_json('data/Redis/redis.json')
        payload = [json.loads(pay)['id'] for pay in payload]
        return payload[500:1000]

    def nc(self):
        payload = read_json('data/NC/用友.json')
        payload = [json.loads(pay)['id'] for pay in payload if '.edu' in json.loads(pay)['id']]
        return payload[500:550]

    def nc(self):
        payload = read_json('data/NC/用友.json')
        payload = [json.loads(pay)['id'] for pay in payload if '.edu' in json.loads(pay)['id']]
        return payload[500:550]


A = Tongda()
tmp = A.nc()
write(tmp)