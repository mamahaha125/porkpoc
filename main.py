# !/usr/bin/env python3
# -*- coding:utf-8 -*-


from newpoc.api import argparse, textwrap
from newpoc.cli import NEWPOC

class Input:
    def __init__(self, arg):
        self.arg = arg

    def run_core(self):
        """
        接收命令
        :return:
        """
        # TODO shell模块

        flag = "command" if self.arg.command else "attack"\
            if self.arg.attack else "verify"

        # TODO fofa模块
        poc = NEWPOC()
        poc.init_options(self.arg.__dict__)

        if self.arg.pocdetail:
            pass

        if self.arg.url:
            poc.start_pool([self.arg.url])

        if self.arg.file:
            poc.start_pool(self.arg.file)

        if self.arg.FOFA:   # TODO 实现FOFA接口调用
            pass



def main():
    parse = argparse.ArgumentParser(description="PORKPOCS !!!",
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    epilog=textwrap.dedent('''Example:
        run.py -u example.com  -t pocs/Redis  -v           #verify
        run.py -r url file     -t pocs/Redis  -a           #load file to get url
        run.py -F api(FOFA...) -t pocs/Redis  -s           #get fofa api to get url
        '''))

    parse.add_argument('-c', '--command', action='store_true', help='command shell')
    parse.add_argument('-v', '--verify', action='store_true', help='verify')
    parse.add_argument('-a', '--attack', action='store_true', help='attack')
    parse.add_argument('-u', '--url', help='target url')
    parse.add_argument('-r', '--file', help='url file', type=argparse.FileType('r'))
    parse.add_argument('-p', '--payload', help='payload file', type=argparse.FileType('r'))
    parse.add_argument('-t', '--poc', help='choose poc nginx poc.py')
    parse.add_argument('-F', '--FOFA', action='store_true', help='fofa url')
    parse.add_argument('-l', '--pocdetail', action='store_true', help='poc detail')

    args = parse.parse_args()
    Input(args).run_core()


if __name__ == "__main__":
    main()


