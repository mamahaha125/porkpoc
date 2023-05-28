# !/usr/bin/env python3
# -*- coding:utf-8 -*-


from newpoc.api import argparse, textwrap, Output
from newpoc.cli import NEWPOC
from newpoc.plugins import fofa_api, ceye_api
from newpoc.plugins.portscan import load_scan
from newpoc.plugins.Finger import load_finger
from newpoc.core.result import ResultPOC

class Input:
    output = Output()
    result = ResultPOC()
    def __init__(self, arg):
        self.arg = arg

    def run_core(self):
        """
        接收命令
        :return:
        """
        poc = NEWPOC()

        if self.arg.FOFA:
            self._run_fofa(poc)

        if self.arg.CEYE:
            self._run_ceye(poc)

        if self.arg.port:
            self._run_port_scan(poc)

        if self.arg.finger:
            self._run_finger_scan(poc)

        if self.arg.poc:
            poc.init_options(self.arg.__dict__)
            self._run_poc(poc)

        if self.arg.file:
            self._run_poc_from_file(poc)

    def _run_fofa(self, poc):
        self.output.check(self.result.result_api(fofa_api.fofa_search(self.arg.FOFA)))

    def _run_ceye(self, poc):
        self.output.check(self.result.result_api(ceye_api.ceye_search(self.arg.CEYE)))

    def _run_port_scan(self, poc):
        port = self.arg.port.split(',')
        self.output.check("正在端口扫描...")
        scan_results = load_scan.scan_ports(self.arg.url, int(port[0]), int(port[1]), 100)
        self.output.success("Open ports:{}".format(scan_results))

        self.output.check("是否选择探测指纹y/n")
        if input() == "y":
            self.output.check("正在探测指纹信息...")
            for i in scan_results:
                a = load_finger.WebScanner('{0}:{1}'.format(self.arg.url, i))
                a.run()

    def _run_finger_scan(self, poc):
        self.output.check("正在探测指纹信息...")
        a = load_finger.WebScanner(self.arg.finger)
        a.run()

    def _run_poc(self, poc):
        if self.arg.url:
            poc.start_pool([self.arg.url])

    def _run_poc_from_file(self, poc):
        poc.start_pool(self.arg.file.read().strip('\n').split('\n'))


def main():
    parse = argparse.ArgumentParser(description="PORKPOCS !!!",
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    epilog=textwrap.dedent('''Example:
        run.py -u example.com  -t pocs/Redis  -v           #verify
        run.py -r url file     -t pocs/Redis  -a           #load file to get url
        run.py -F api(FOFA...) -t pocs/Redis  -s           #get fofa api to get url
        '''))

    parse.add_argument('-c', '--command', action='store_true', help='command shell')
    parse.add_argument('-l', '--pocdetail', action='store_true', help='poc detail')
    parse.add_argument('-v', '--verify', action='store_true', help='verify')
    parse.add_argument('-a', '--attack', action='store_true', help='attack')

    # 插件参数
    parse.add_argument('-s', '--port', help='PORT SCAN')
    parse.add_argument('-e', '--CEYE', help='CEYE API')
    parse.add_argument('-F', '--FOFA', help='fofa API')
    parse.add_argument('-f', '--finger', help='finger')

    ##
    parse.add_argument('-u', '--url', help='target url')
    parse.add_argument('-t', '--poc', help='choose poc nginx poc.py')
    parse.add_argument('-P', '--proxy', help='proxy')
    parse.add_argument('-k', '--Cookie', help='Cookie')

    # 接收文件和payload参数
    parse.add_argument('-r', '--file', help='url file', type=argparse.FileType('r'))
    parse.add_argument('-p', '--payload', help='payload file', type=argparse.FileType('r'))



    args = parse.parse_args()
    Input(args).run_core()


if __name__ == "__main__":
    main()

