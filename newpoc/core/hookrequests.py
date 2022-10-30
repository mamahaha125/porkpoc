'''hook requests'''
# from urllib.parse import urlparse as parse_urlparse
from urllib.parse import urljoin as parse_urljoin
import requests

# 忽略requests警告
requests.packages.urllib3.disable_warnings()

requests_get = requests.get
requests_post = requests.post
requests_options = requests.options
requests_put = requests.put
requests_delete = requests.delete

User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
Timeout = 6
proxies_ip = ''
# proxies_ip = '127.0.0.1:8888'

def http(url_path: str, ssl=False) -> str:
    '''添加http协议头 不改变原来地址路由大小写'''
    new_url_path = url_path.strip('/').lower()
    if not new_url_path.startswith(("https://", "http://", "socks5://", "socks4://", "socks://")):
        if ssl:
            return r'https://' + url_path
        return r'http://' + url_path

    return url_path


def urljoin(host, rpath):
    host = http(host)
    url = parse_urljoin(host, rpath)
    return url
    

def hook_kwarg(arg, kwarg):

    # 给url类型添加http请求协议
    arg = list(arg)
    arg[0] = http(arg[0])

    # 修改默认ua
    if 'headers' not in kwarg:
        kwarg['headers'] = {'User-Agent': User_Agent}

    if 'User-Agent' not in kwarg['headers']:
        kwarg['headers']['User-Agent'] = User_Agent
    
    # 修改默认超时
    if 'timeout' not in kwarg:
        kwarg['timeout'] = Timeout

    # 修改verify
    if 'verify' not in kwarg:
        kwarg['verify'] = False

    if proxies_ip:
        kwarg['proxies'] = {"http": proxies_ip,"https": proxies_ip}

    return arg, kwarg


def filter_error_page(resp):
    '''过滤一些错误页面'''
    filter_list = [
        '阿里云404页面',
        '阿里云万网虚机IP访问报错提示',
        '网防G01'
    ]

    try:
        resp.encoding = resp.apparent_encoding
        resp_text = resp.text
        for tmp in filter_list:
            if tmp in resp_text:
                return None
    except:
        pass
    return resp


def get(*arg, **kwarg):
    arg, kwarg = hook_kwarg(arg, kwarg)
    resp = requests_get(*arg, **kwarg)
    resp = filter_error_page(resp)
    return resp


def post(*arg, **kwarg):
    arg, kwarg = hook_kwarg(arg, kwarg)
    resp = requests_post(*arg, **kwarg)
    resp = filter_error_page(resp)
    return resp


def options(*arg, **kwarg):
    arg, kwarg = hook_kwarg(arg, kwarg)
    resp = requests_options(*arg, **kwarg)
    return resp


def put(*arg, **kwarg):
    arg, kwarg = hook_kwarg(arg, kwarg)
    resp = requests_put(*arg, **kwarg)
    return resp


def delete(*arg, **kwarg):
    arg, kwarg = hook_kwarg(arg, kwarg)
    resp = requests_delete(*arg, **kwarg)
    return resp


requests.get = get
requests.post = post
requests.options = options
requests.put = put
requests.delete = delete
