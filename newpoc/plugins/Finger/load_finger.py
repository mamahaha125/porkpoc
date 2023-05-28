import sqlite3

from newpoc.api import Output, requests
import re
from bs4 import BeautifulSoup
import time

rtitle, rheader, rbody, rbracket = re.compile(r'title="(.*)"'), re.compile(r'header="(.*)"'), re.compile(r'body="(.*)"'), re.compile(r'\((.*)\)')


class WebScanner:
    ouput = Output()

    def __init__(self, target):
        self.target = target
        self.start = time.time()

    def get_info(self):
        """获取web的信息"""
        # try:
        # 	r = requests.get(url=self.target, headers=agent, timeout=3, verify=False)
        # 	content = r.text
        # 	try:
        # 		title = BeautifulSoup(content, 'lxml').title.text.strip()
        #
        # 		return str(r.headers), content, title.strip('\n')
        # 	except:
        # 		return str(r.headers), content, ''
        # except Exception as e:
        # 	pass

        r = requests.get(self.target)
        content = r.text
        title = BeautifulSoup(content, 'lxml').title.text.strip()

        return str(r.headers), content, title.strip('\n')

    def check_rule(self, key, header, body, title):
        """指纹识别"""
        try:
            if 'title="' in key:
                return re.findall(rtitle, key)[0].lower() in title.lower()
            elif 'body="' in key:
                return re.findall(rbody, key)[0] in body
            else:
                return re.findall(rheader, key)[0] in header
        except Exception as e:
            pass

    def handle(self, _id, header, body, title):
        """取出数据库的key进行匹配"""
        name, key = check(_id)

        # 满足一个条件即可的情况
        if '||' in key and '&&' not in key and '(' not in key:
            for rule in key.split('||'):
                if self.check_rule(rule, header, body, title):
                    self.ouput.success(f'{self.target}   {name}')
                    break

        # 只有一个条件的情况
        elif '||' not in key and '&&' not in key and '(' not in key:
            if self.check_rule(key, header, body, title):
                self.ouput.success(f'{self.target}   {name}')

        # 需要同时满足条件的情况
        elif '&&' in key and '||' not in key and '(' not in key:
            num = 0
            for rule in key.split('&&'):
                if self.check_rule(rule, header, body, title):
                    num += 1
            if num == len(key.split('&&')):
                self.ouput.success(f'{self.target}   {name}')

        else:
            # 与条件下存在并条件: 1||2||(3&&4)
            if '&&' in re.findall(rbracket, key)[0]:
                for rule in key.split('||'):
                    if '&&' in rule:
                        num = 0
                        for _rule in rule.split('&&'):
                            if self.check_rule(_rule, header, body, title):
                                num += 1
                        if num == len(rule.split('&&')):
                            self.ouput.success(f'{self.target}   {name}')
                            break
                    else:
                        if self.check_rule(rule, header, body, title):
                            self.ouput.success(f'{self.target}   {name}')
                            break
            else:
                # 并条件下存在与条件： 1&&2&&(3||4)
                for rule in key.split('&&'):
                    num = 0
                    if '||' in rule:
                        for _rule in rule.split('||'):
                            if self.check_rule(_rule, title, body, header):
                                num += 1
                                break
                    else:
                        if self.check_rule(rule, title, body, header):
                            num += 1
                if num == len(key.split('&&')):
                    self.ouput.success(f'[+] {self.target}   {name}')

    def run(self):
        try:
            header, body, title = self.get_info()
            for _id in range(1, int(count())):
                try:
                    self.handle(_id, header, body, title)
                except Exception as e:
                    pass
        except Exception as e:
            self.ouput.error(e)
        finally:
            self.ouput.success(f"指纹识别成功, 耗时 {time.time() - self.start} 秒.")


def check(_id):
    with sqlite3.connect('./newpoc/plugins/Finger/porkfinger.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT name, keys FROM `pork_finger` WHERE id=\'{}\''.format(_id))
        for row in result:
            return row[0], row[1]


def count():
    with sqlite3.connect('./newpoc/plugins/Finger/porkfinger.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT COUNT(id) FROM `pork_finger`')
        for row in result:
            return row[0]