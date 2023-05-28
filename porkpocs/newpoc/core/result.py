#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import prettytable as pt
from newpoc.core.writedown import Report


class ResultPOC(pt.PrettyTable):
    def __init__(self, field_names=None, **kwargs):
        super().__init__(field_names, **kwargs)
        self.write_list = []

    def result_table(self, result_queue):
        self.field_names = ["target-url", "poc-name", "poc-id", "component", "version", "status", "payload"]
        while True:
            if result_queue.empty():
                break
            tmp_poc_result = result_queue.get()
            self.write_list.append(tmp_poc_result)
            data = [tmp_poc_result[detail] for detail in self.field_names]
            self.add_row(data)
        return self

    def poc_detail_table(self, poc_detail):
        self.field_names = ["cnvd_cve", "createDate", "name", "appVersion", "vulType", "version", "pocDesc"]
        for poc in poc_detail:
            self.add_row([poc['cnvd_cve'], poc['createDate'], poc['name'], poc['appVersion'], poc['vulType'], poc['version'], poc["pocDesc"]])
        # 细节左对齐
        self.align['pocDesc'] = 'l'
        return self

    def result_api(self, arg):
        """
        打印 json 格式
        """

        if arg[0] == 'FOFA':
            self.field_names = ["域名", "IP", "端口"]
            for i in arg[1:]:
                self.add_row(i)

        elif arg[0] == 'CEYE':
            self.field_names = ["id", "name", "remote_addr", "created_at"]
            for i in arg[1:]:
                    self.add_row(list(i.values()))


        return self
    def wirtedown(self):
        Report.write_json(self.write_list)


if __name__ == "__main__":
    x = ResultPOC()
    x.field_names = ["target-url", "poc-name", "poc-id", "component", "version", "status"]
    x.align["target-url"] = "l"
    x.padding_width = 1
    for i in range(10):
        x.add_row(["Adelaide", i, i, i, i, i])
    print(x)
