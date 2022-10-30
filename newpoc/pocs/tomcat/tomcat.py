#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import random
from collections import OrderedDict
from hashlib import md5
from newpoc.api import PocBase, Output
from newpoc.cli import POC_QUEUE

class POC(PocBase):
    vulID = "14444444"  # ssvid ID 如果是提交漏洞的同时提交 PoC,则写成 0
    version = "1"  # 默认为1
    author = "seebug"  # PoC作者的大名
    vulDate = "2022-10-17"  # 漏洞公开的时间,不知道就写今天
    createDate = "2022-10-17"  # 编写 PoC 的日期
    updateDate = "2022-10-17"  # PoC 更新的时间,默认和编写时间一样
    references = ["https://xxx.xx.com.cn"]  # 漏洞地址来源,0day不用写
    name = "Flask jinja2"  # PoC 名称
    appPowerLink = "https://www.drupal.org/"  # 漏洞厂商主页地址
    appName = "Drupal"  # 漏洞应用名称
    appVersion = "7.x"  # 漏洞影响版本
    vulType = 'VUL_TYPE.UNAUTHORIZED_ACCESS'  # 漏洞类型,类型参考见 漏洞类型规范表
    category = 'POC_CATEGORY.EXPLOITS.WEBAPP'
    samples = []  # 测试样列,就是用 PoC 测试成功的网站
    install_requires = []  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写
    desc = """
            Drupal 在处理 IN 语句时，展开数组时 key 带入 SQL 语句导致 SQL 注入，
            可以添加管理员、造成信息泄露。
        """  # 漏洞简要描述
    pocDesc = """
            poc的用法描述
        """  # POC用法描述
    output = Output()


    # TODO 需要用户交互的POC方法
    # def _options(self):
    #     opt = OrderedDict()  # value = self.get_option('key')
    #     opt["string"] = OptString("", description="这个poc需要用户登录，请输入登录账号", require=False)
    #     opt["integer"] = OptInteger(
    #         "", description="这个poc需要用户密码，请输出用户密码", require=False
    #     )
    #     return opt

    def _verify(self, url):
        # import time
        # time.sleep(2)
        # self.output.check("tomcat_verify:{}".format(id(self.output)))
        self.output.error('{} 日志id '.format(id(POC_QUEUE)))

    def _attack(self, url):
        self.output.check("tomcat_attack:{}".format(url))

    def _shell(self, url):
        """
        shell模式下，只能运行单个PoC脚本，控制台会进入shell交互模式执行命令及输出
        """
        # cmd = REVERSE_PAYLOAD.BASH.format(get_listener_ip(), get_listener_port())
        # 攻击代码 execute cmd
        self.output.check("tomcat_verify:{}".format(url))


def other_fuc():
    pass

def other_utils_func():
    pass




