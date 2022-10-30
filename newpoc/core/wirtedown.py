#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import xml


class RePort:
    def __init__(self):
        pass


    def write_json(self, reuslt):
        with open("{}.json".format(), 'w') as f:
            [f.write(i + '\n') for i in json.dumps(reuslt)]


