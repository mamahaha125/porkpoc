#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
import threading
import colorlog


class Output:
    # 记录器
    logger = logging.getLogger('mama')
    logger.setLevel(logging.DEBUG)

    # 处理器
    # console handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)

    # file handler
    fileHandler = logging.FileHandler(filename='tmp.log')
    fileHandler.setLevel(logging.DEBUG)

    # formatter格式(通用)
    # %()-8s  -8可以设置8位左对其， ---字符串输出
    log_color = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'black,bg_white',
    }
    fmt = "%(log_color)s【*】|%(asctime)s|%(levelname)-8s|%(message)s"
    datetime = "%Y-%m-%d %H:%M:%S"
    formatter = colorlog.ColoredFormatter(fmt=fmt, datefmt=datetime,
                                          reset=True,
                                          style='%',
                                          log_colors=log_color)
    # 处理器设置格式
    consoleHandler.setFormatter(formatter)

    # 记录器设置处理器
    logger.addHandler(consoleHandler)

    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    # 定义过滤器  只输出a.c开头的,加过滤器后无法输出在文件里
    # fil = logging.Filter('a.c')

    # 关联过滤器
    # logger.addFilter(fil)
    # fileHandler.addFilter(fil)
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Output, "_instance"):
            with Output._instance_lock:
                if not hasattr(Output, "_instance"):
                    Output._instance = object.__new__(cls)
        return Output._instance

    def check(self, cherk_flag):
        self.logger.debug(cherk_flag)

    def success(self, message):
        self.logger.info(message)

    def fail(self, error=""):
        self.logger.warning(error)

    def error(self, error=""):
        self.logger.error(error)




