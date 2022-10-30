#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import prettytable as pt


class ResultPOC(pt.PrettyTable):
    def __init__(self, field_names=None, **kwargs):
        super().__init__(field_names, **kwargs)

    def result_table(self, result_queue):
        self.field_names = ["target-url", "poc-name", "poc-id", "component", "version", "status"]
        while True:
            if result_queue.empty():
                break
            tmp_poc_result = result_queue.get()
            data = [
                tmp_poc_result['target-url'],
                tmp_poc_result['poc-name'],
                tmp_poc_result['poc-id'],
                tmp_poc_result['component'],
                tmp_poc_result['version'],
                tmp_poc_result['status'],
            ]
            self.add_row(data)
        return self



if __name__ == "__main__":
    x = ResultPOC()
    x.field_names = ["target-url", "poc-name", "poc-id", "component", "version", "status"]
    x.align["target-url"] = "l"
    x.padding_width = 1
    for i in range(10):
        x.add_row(["Adelaide", i, i,i, i, i])
    print(x)