#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from newpoc.core.hookrequests import requests, urljoin


class PocBase(object):
    def __init__(self):
        # PoC attributes
        self.cnvd_cve = getattr(self, 'cnvd_cve', '0')
        self.version = getattr(self, 'version', '1')
        self.author = getattr(self, 'author', '')
        self.vulDate = getattr(self, 'vulDate', '')
        self.createDate = getattr(self, 'createDate', '')
        self.updateDate = getattr(self, 'updateDate', '')
        self.references = getattr(self, 'references', [])
        self.name = getattr(self, 'name', '')
        self.appPowerLink = getattr(self, 'appPowerLink', '')
        self.appName = getattr(self, 'appName', '')
        self.appVersion = getattr(self, 'appVersion', '')
        self.vulType = getattr(self, 'vulType', '')
        self.desc = getattr(self, 'desc', '')
        self.samples = getattr(self, 'samples', [])
        self.install_requires = getattr(self, 'install_requires', [])
        self.pocDesc = getattr(self, 'pocDesc', "")

    def _shell(self):
        raise NotImplementedError

    def _attack(self):
        raise NotImplementedError

    def _verify(self):
        raise NotImplementedError

    def parse_detail(self):
        return self.__dict__


# class Output_Result(object):
#     def __init__(self, poc=None):
#         self.error_msg = tuple()
#         self.result = {}
#         self.params = {}
#         self.status = ''
#         if poc:
#             self.url = poc.url
#             self.mode = poc.mode
#             self.vul_id = poc.vulID
#             self.name = poc.name
#             self.app_name = poc.appName
#             self.app_version = poc.appVersion
#             self.error_msg = poc.expt
#             self.poc_attrs = {}
#             # for i in inspect.getmembers(poc):
#             #     if not i[0].startswith('_') and type(i[1]) in [str, list, dict]:
#             #         self.poc_attrs[i[0]] = i[1]
#
#     def success(self, result):
#         # assert isinstance(result, dict)
#         # self.status = OUTPUT_STATUS.SUCCESS
#         # self.result = result
#         pass
#
#     def fail(self, error=""):
#         # assert isinstance(error, str)
#         # self.status = OUTPUT_STATUS.FAILED
#         # self.error_msg = (0, error)
#         pass
