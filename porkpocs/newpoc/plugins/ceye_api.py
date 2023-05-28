from newpoc.api import requests
from newpoc.utils.load_conf import ini_to_dict

def ceye_search(inputs):
    conf = ini_to_dict()
    res = requests.get("http://api.ceye.io/v1/records?token={0}&type={1}&filter={2}".format(conf.ceye.token, inputs, 's')).json()
    if (res['meta']['code']) == 200:
        return list(['CEYE'] + res['data'])

    else:
        return None