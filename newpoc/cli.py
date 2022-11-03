#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import signal
from newpoc.api import os, re, importlib, Path, Output
from multiprocessing.dummy import Pool as MPD_POOL
from multiprocessing.dummy import Queue
from newpoc.utils.dicter import Dicter

from newpoc.core.result import ResultPOC

# POC_RPATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'pocs')
POC_RPATH = os.path.abspath(os.path.dirname(__file__))
POC_QUEUE = Queue(maxsize=0)

PATH = Dicter()
PATH.SCRIPT_PATH = ''
PATH.ROOT_PATH = POC_RPATH


class NEWPOC:
    output = Output()

    def __init__(self):
        self.ret = []  # 使用类属性的方式，用来回收全部执行结果
        self.TARGET = dict()

    def init_options(self, conf):
        """
        初始化配置
        :param conf:
        :return:
        """
        with open('newpoc/data/sign/pocs.txt', 'r', encoding='UTF-8') as f:
            self.output.check(f.read())
        self.output.check("初始化配置中...")
        self.TARGET = conf


        try:
            # poc路径获取
            PATH.SCRIPT_PATH = os.path.join(PATH.ROOT_PATH, self.TARGET['poc'])

            # 选择脚本远行方式，不填默认verify
            self.TARGET['flag'] = "_shell" if conf['command'] else "_attack" \
                if conf['attack'] else "_verify"

            # 加载payload
            self.TARGET['payload'] = self.TARGET['payload'].read() if self.TARGET['payload'] else None

            # 动态加载poc模块

            self.TARGET['poc_list'] = self.get_all_poc() if self.get_all_poc() else None
            self.TARGET['poc_models'] = [self.import_poc(poc) for poc in self.TARGET['poc_list']]



            # 显示poc信息

            if self.TARGET['pocdetail']:
                self.poc_detail()
        except TypeError as err:
            self.output.error("请输入正确poc路径 -t pocs/.../...{}".format(err))
            os._exit(0)
    def show_result(self):
        recv = ResultPOC()
        res = recv.result_table(POC_QUEUE)
        self.output.success(res)
        recv.wirtedown()


    def CtrlC(self,num ,*args):
        """
        如果用sys.exit()在上层有try的情况下达不到直接结束程序的效果
        :return:
        """
        os._exit(0)

    def _mpd_pool(self, func, datas, max_workers):
        """
        启动线程池
        :param func:
        :param datas:
        :param max_workers:
        :return:
        """
        try:
            signal.signal(signal.SIGINT, self.CtrlC)
            signal.signal(signal.SIGTERM, self.CtrlC)
            pool = MPD_POOL(max_workers)
            pool.map(func, datas)
            pool.close()
            pool.join()  # 等待全部结束
            self.show_result()
        except Exception as err:
            self.output.error(err)

    def start(self, poc_task):
        try:
            url, models = poc_task
            self.TARGET['url'] = url
            poc_obj = models.POC()
            func = getattr(poc_obj, self.TARGET['flag'])
            self.output.check("{0} to {1}...".format(self.TARGET['flag'].replace('_', ''), url))
            func(self.TARGET)
        except KeyboardInterrupt as err:
            self.output.error(err)

    def import_poc(self, tmp_files):
        """
        动态导入poc模块
        :param tmp_files:
        :return:
        """
        cms, poc_model = tmp_files
        cms = re.split(r'[/\\]', str(cms))[-1]
        poc_model = poc_model.replace('.py', '')
        return importlib.import_module("newpoc.pocs.{0}.{1}".format(cms, poc_model))

    def start_pool(self, urls, max_worker=10):
        task_list = self.make_tasks(urls)
        self._mpd_pool(self.start, task_list, max_worker)

    def make_tasks(self, url):
        return [(_url.strip(), poc) for _url in url for poc in self.TARGET['poc_models']]

    def get_all_poc(self):
        """
        获取所有poc
        :return:
        """
        path = Path(PATH.SCRIPT_PATH)
        if PATH.SCRIPT_PATH.endswith('.py'):
            return [(str(path.parent), os.path.basename(path))]
        return [(str(Path(tmp_path).parent), os.path.basename(tmp_path)) for tmp_path in path.rglob('*.py') \
                if "__init__" not in str(tmp_path)]

    def poc_detail(self):
        """
        查看poc详细信息
        """
        try:
            task_detail = [getattr(model.POC(), "parse_detail")() for model in self.TARGET['poc_models']]
            report_poc = ResultPOC()
            self.output.check(report_poc.poc_detail_table(task_detail))
        except KeyboardInterrupt as err:
            self.output.error(err)

if __name__ == "__main__":
    s = NEWPOC()
    print(s.import_poc(('F:\\python\\porkpocs\\newpoc\\pocs\\Redis', 'redisnone.py')))
    print(POC_RPATH)
    from newpoc.core.get_poc import POC_RPATH
    print(POC_RPATH)