#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from newpoc.api import json, Output

log = Output()
class Report:
    @staticmethod
    def write_json(result):
        try:
            with open("result.json", 'w', encoding='utf-8') as f:
                for tmp in result:
                    f.write(json.dumps(tmp)+'\n')
                log.check("结果写入result.json")
        except:
            log.error("结果导出失败！！！")

