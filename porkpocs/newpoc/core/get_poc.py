#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
from newpoc.api import Path
from newpoc.utils.dicter import Dicter

POC_RPATH = os.path.abspath(os.path.dirname(__file__))

PATH = Dicter()
PATH.SCRIPT_PATH = ''
PATH.ROOT_PATH = POC_RPATH


class GetPath:
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


if __name__ == "__main__":
    print(__file__)
    # print(path)
    print(POC_RPATH)
    # print(get_all_poc())
    """
    ('F:\\python\\porkpocs\\newpoc\\pocs\\Redis', 'redisnone.py')
    """
